import argparse
import calendar
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import transaction
from django.db.models import Exists, OuterRef, Q, QuerySet
from django.utils import timezone

import structlog

from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.klantinteracties.models.partijen import Partij

logger = structlog.stdlib.get_logger(__name__)

MINIMUM_MONTHS_IN_THE_PAST = 12


def _subtract_months(d: date, months: int) -> date:
    """
    `d` minus a number of calendar months, clamping the day to the last day
    of the resulting month (e.g. 2026-02-29 minus 12 months -> 2025-02-28).
    """
    month_index = d.month - 1 - months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _default_maximum_date() -> date:
    """
    Last day of the previous month, minus 1 year.
    """
    first_of_this_month = timezone.now().date().replace(day=1)
    last_day_of_previous_month = first_of_this_month - timedelta(days=1)
    return _subtract_months(last_day_of_previous_month, 12)


def _parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{value}' is geen geldige datum (verwacht formaat: YYYY-MM-DD)."
        )


class Command(BaseCommand):
    help = (
        "Tijdelijk opruimscript: verwijdert Klantcontacten (contactmomenten) die niet "
        "gerelateerd zijn aan een Zaak, samen met hun gerelateerde Betrokkenen, "
        "Onderwerpobjecten, Bijlagen, Interne taken (contactverzoeken) en eventuele "
        "Partijen die na verwijdering nergens anders meer bij betrokken zijn. Dit "
        "script bestaat in afwachting van ondersteuning hiervoor in Open "
        "Archiefbeheer."
    )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--dry-run",
            action=argparse.BooleanOptionalAction,
            default=True,
            help=(
                "Modus waarin het script draait. Indien ingeschakeld (standaard: "
                "previewmodus) wordt alleen een vernietigingslijst getoond zonder "
                "daadwerkelijk te verwijderen. Gebruik --no-dry-run voor de "
                "vernietigingsmodus, waarin de records daadwerkelijk verwijderd "
                "worden."
            ),
        )
        parser.add_argument(
            "--minimum-date",
            dest="minimum_date",
            type=_parse_date,
            default=None,
            metavar="YYYY-MM-DD",
            help=(
                "Sluitingsdatum minimum. Alleen Klantcontacten met een "
                "'plaatsgevondenOp' datum op of na deze datum komen in aanmerking "
                "voor verwijdering. Standaard is er geen ondergrens."
            ),
        )
        parser.add_argument(
            "--maximum-date",
            dest="maximum_date",
            type=_parse_date,
            default=None,
            metavar="YYYY-MM-DD",
            help=(
                "Sluitingsdatum maximum. Alleen Klantcontacten met een "
                "'plaatsgevondenOp' datum op of voor deze datum komen in "
                "aanmerking voor verwijdering. Moet minimaal 12 maanden in het "
                "verleden liggen. Standaard: de "
                "laatste dag van de vorige maand, min 1 jaar."
            ),
        )

    def handle(self, *args, **options) -> None:
        dry_run = options["dry_run"]
        minimum_date: date | None = options["minimum_date"]
        explicit_maximum_date: date | None = options["maximum_date"]

        if explicit_maximum_date is not None:
            earliest_allowed = _subtract_months(
                timezone.now().date(), MINIMUM_MONTHS_IN_THE_PAST
            )
            if explicit_maximum_date > earliest_allowed:
                raise CommandError(
                    "maximum-date moet minimaal 12 maanden in het verleden liggen "
                    f"(dus op of voor {earliest_allowed.isoformat()})."
                )

        maximum_date: date = explicit_maximum_date or _default_maximum_date()

        if minimum_date and minimum_date > maximum_date:
            raise CommandError("minimum-date kan niet na maximum-date liggen.")

        started_at = timezone.now()

        klantcontact_ids = list(
            self.get_eligible_klantcontacten(minimum_date, maximum_date)
            .order_by("plaatsgevonden_op", "pk")
            .values_list("pk", flat=True)
        )
        klantcontacten = Klantcontact.objects.filter(pk__in=klantcontact_ids).order_by(
            "plaatsgevonden_op", "pk"
        )

        records = self.build_records(klantcontacten)

        self.stdout.write("Vernietigingslijst contactmomenten en contactverzoeken")
        self.stdout.write("")
        self.stdout.write(
            f"Modus: {'previewmodus' if dry_run else 'vernietigingsmodus'}"
        )
        self.stdout.write(
            "Sluitingsdatum minimum: "
            f"{minimum_date.isoformat() if minimum_date else 'niet opgegeven'}"
        )
        self.stdout.write(f"Sluitingsdatum maximum: {maximum_date.isoformat()}")
        self.stdout.write("")
        self.stdout.write("Records:")
        for record in records:
            self.stdout.write(
                f"Record {record['identificatie']} {record['type']} "
                f"{record['aangemaakt']} {record['gesloten']}"
            )
        self.stdout.write("")
        self.stdout.write(f"Totaal aantal geselecteerde records: {len(records)}")
        self.stdout.write("")

        logger.info(
            "klantcontacten_not_related_to_zaken_selected",
            dry_run=dry_run,
            minimum_date=minimum_date.isoformat() if minimum_date else None,
            maximum_date=maximum_date.isoformat(),
            klantcontacten_count=len(klantcontact_ids),
            records_count=len(records),
        )

        if dry_run:
            return

        deleted_count = self.delete_klantcontacten(klantcontacten)
        finished_at = timezone.now()

        logger.info(
            "klantcontacten_not_related_to_zaken_deleted",
            started_at=started_at.isoformat(),
            finished_at=finished_at.isoformat(),
            deleted_count=deleted_count,
        )

        self.stdout.write(
            "Bewijs van vernietiging. Tussen "
            f"{started_at.isoformat()} en {finished_at.isoformat()} zijn "
            f"{deleted_count} records vernietigd overeenkomstig de "
            "vernietigingslijst."
        )

    def get_eligible_klantcontacten(
        self, minimum_date: date | None, maximum_date: date
    ) -> QuerySet[Klantcontact]:
        """Return Klantcontacten without a Zaak in the given date range."""

        onderwerpobject_zaak = Onderwerpobject.objects.filter(
            Q(klantcontact=OuterRef("pk")) | Q(was_klantcontact=OuterRef("pk")),
            onderwerpobjectidentificator_code_objecttype__iexact="zaak",
        )

        queryset = Klantcontact.objects.annotate(
            _heeft_zaak=Exists(onderwerpobject_zaak)
        ).filter(_heeft_zaak=False, plaatsgevonden_op__date__lte=maximum_date)

        if minimum_date:
            queryset = queryset.filter(plaatsgevonden_op__date__gte=minimum_date)

        return queryset

    def build_records(self, klantcontacten: QuerySet[Klantcontact]) -> list[dict]:
        interne_taken_by_klantcontact: dict[int, list[InterneTaak]] = {}
        interne_taken = (
            InterneTaak.objects.filter(klantcontact__in=klantcontacten)
            .select_related("klantcontact")
            .order_by("toegewezen_op", "pk")
        )
        for interne_taak in interne_taken:
            interne_taken_by_klantcontact.setdefault(
                interne_taak.klantcontact.pk, []
            ).append(interne_taak)

        records = []
        for klantcontact in klantcontacten:
            klantcontact_datum = klantcontact.plaatsgevonden_op.isoformat()
            records.append(
                {
                    "identificatie": klantcontact.nummer or str(klantcontact.uuid),
                    "type": "Contactmoment",
                    "aangemaakt": klantcontact_datum,
                    "gesloten": klantcontact_datum,
                }
            )
            for interne_taak in interne_taken_by_klantcontact.get(klantcontact.pk, []):
                records.append(
                    {
                        "identificatie": interne_taak.nummer or str(interne_taak.uuid),
                        "type": "Contactverzoek",
                        "aangemaakt": klantcontact_datum,
                        "gesloten": klantcontact_datum,
                    }
                )

        return records

    @transaction.atomic
    def delete_klantcontacten(self, klantcontacten: QuerySet[Klantcontact]) -> int:
        deleted_count = 0

        for klantcontact in klantcontacten:
            betrokkenen = Betrokkene.objects.filter(klantcontact=klantcontact)
            partij_ids = list(
                betrokkenen.filter(partij__isnull=False).values_list(
                    "partij_id", flat=True
                )
            )

            DigitaalAdres.objects.filter(
                betrokkene__in=betrokkenen, partij__isnull=True
            ).delete()

            record_count = (
                1 + InterneTaak.objects.filter(klantcontact=klantcontact).count()
            )

            klantcontact.delete()
            deleted_count += record_count

            for partij_id in partij_ids:
                if not Betrokkene.objects.filter(partij_id=partij_id).exists():
                    Partij.objects.filter(pk=partij_id).delete()

        return deleted_count
