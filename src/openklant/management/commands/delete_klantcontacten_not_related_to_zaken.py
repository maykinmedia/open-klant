import argparse
import calendar
import os
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.models import Exists, Model, OuterRef, Q, QuerySet
from django.db.models.deletion import Collector, ProtectedError
from django.utils import timezone
from django.utils.text import capfirst

import structlog

from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.klantinteracties.models.partijen import (
    Partij,
    PartijIdentificator,
)

logger = structlog.stdlib.get_logger(__name__)

MINIMUM_MONTHS_IN_THE_PAST = 12


def _record_type_label(model: type[Model]) -> str:
    return capfirst(model._meta.verbose_name)


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
        "gerelateerd zijn aan een Zaak, samen met werkelijk alles wat daardoor mee "
        "verwijderd wordt: onder andere Betrokkenen, Actor klantcontacten, "
        "Onderwerpobjecten, Bijlagen, Interne taken (contactverzoeken), Digitale "
        "adressen en eventuele Partijen die na verwijdering nergens anders meer bij "
        "betrokken zijn, met op hun beurt weer hun eigen gerelateerde records "
        "(Rekeningnummers, Partij identificatoren, Categorie relaties, "
        "Vertegenwoordigden, Organisaties, Personen en Contactpersonen). Alles wat "
        "daadwerkelijk verwijderd wordt, wordt expliciet op de vernietigingslijst "
        "vermeld. Dit script bestaat in afwachting van ondersteuning hiervoor in "
        "Open Archiefbeheer."
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

        klantcontacten = self.get_eligible_klantcontacten(
            minimum_date, maximum_date
        ).order_by("plaatsgevonden_op", "pk")

        collector, records = self.build_deletion(klantcontacten)

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
        if records:
            id_width = max(len(str(record["identificatie"])) for record in records)
            type_width = max(len(record["type"]) for record in records)
        else:
            id_width = type_width = 0
        for record in records:
            self.stdout.write(
                f"Record {record['identificatie']:>{id_width}} "
                f"{record['type']:<{type_width}} "
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
            klantcontacten_count=klantcontacten.count(),
            records_count=len(records),
        )

        if dry_run:
            return

        deleted_count = self.delete_klantcontacten(collector, len(records))
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

        zaak_objecttype = os.getenv("KLANTCONTACT_CLEANUP_ZAAK_OBJECTTYPE", "zaak")

        onderwerpobject_zaak = Onderwerpobject.objects.filter(
            Q(klantcontact=OuterRef("pk")) | Q(was_klantcontact=OuterRef("pk")),
            onderwerpobjectidentificator_code_objecttype__iexact=zaak_objecttype,
        )

        queryset = Klantcontact.objects.annotate(
            _heeft_zaak=Exists(onderwerpobject_zaak)
        ).filter(_heeft_zaak=False, plaatsgevonden_op__date__lte=maximum_date)

        if minimum_date:
            queryset = queryset.filter(plaatsgevonden_op__date__gte=minimum_date)

        return queryset

    def build_deletion(
        self, klantcontacten: QuerySet[Klantcontact]
    ) -> tuple[Collector, list[dict]]:
        collector = Collector(using=klantcontacten.db)

        try:
            collector.collect(klantcontacten)

            klantcontact_datums = {
                klantcontact.pk: klantcontact.plaatsgevonden_op.isoformat()
                for klantcontact in collector.data.get(Klantcontact, [])
            }
            klantcontact_ids = list(klantcontact_datums)
            betrokkenen = list(collector.data.get(Betrokkene, []))

            orphan_digitale_adressen = DigitaalAdres.objects.filter(
                betrokkene__in=betrokkenen, partij__isnull=True
            )
            collector.collect(orphan_digitale_adressen)

            partij_datums: dict[int, str] = {}
            for betrokkene in betrokkenen:
                if not betrokkene.partij_id:
                    continue
                datum = klantcontact_datums[betrokkene.klantcontact_id]
                if (
                    betrokkene.partij_id not in partij_datums
                    or datum > partij_datums[betrokkene.partij_id]
                ):
                    partij_datums[betrokkene.partij_id] = datum

            if partij_datums:
                orphaned_partijen = (
                    Partij.objects.filter(pk__in=partij_datums)
                    .annotate(
                        _heeft_andere_betrokkene=Exists(
                            Betrokkene.objects.filter(partij=OuterRef("pk")).exclude(
                                klantcontact_id__in=klantcontact_ids
                            )
                        )
                    )
                    .filter(_heeft_andere_betrokkene=False)
                )
                orphaned_partij_ids = list(
                    orphaned_partijen.values_list("pk", flat=True)
                )
                self._prevent_protected_error_for_self_contained_identificatoren(
                    collector, orphaned_partij_ids
                )
                collector.collect(orphaned_partijen)
        except ProtectedError as error:
            blocking = sorted(
                f"{_record_type_label(type(obj))} {obj.uuid}"
                for obj in error.protected_objects
            )
            raise CommandError(
                "Kan de vernietigingslijst niet opbouwen: het verwijderen wordt "
                "geblokkeerd door de volgende records die nog ergens naar "
                "verwijzen via een beschermde (PROTECT) relatie en dus niet "
                "automatisch vernietigd kunnen worden: "
                f"{', '.join(blocking)}. Los dit eerst handmatig op."
            ) from error

        records = self._build_records(collector, klantcontact_datums, partij_datums)
        return collector, records

    @staticmethod
    def _prevent_protected_error_for_self_contained_identificatoren(
        collector: Collector, orphaned_partij_ids: list[int]
    ) -> None:
        """
        Pre-collect PartijIdentificatoren that will be deleted with their Partij.

        The self-referencing `PROTECT` relation would otherwise block deletion
        even when all related identificatoren are part of the same deletion.
        Identificatoren referenced by a Partij outside the deletion are left
        untouched so the normal `ProtectedError` is raised.
        """
        if not orphaned_partij_ids:
            return

        identificatoren = list(
            PartijIdentificator.objects.filter(partij_id__in=orphaned_partij_ids)
        )
        if not identificatoren:
            return

        identificator_ids = {identificator.pk for identificator in identificatoren}
        externally_referenced = PartijIdentificator.objects.filter(
            sub_identificator_van_id__in=identificator_ids
        ).exclude(pk__in=identificator_ids)
        if externally_referenced.exists():
            return

        collector.collect(identificatoren, collect_related=False)

    def _build_records(
        self,
        collector: Collector,
        klantcontact_datums: dict[int, str],
        partij_datums: dict[int, str],
    ) -> list[dict]:
        object_datums: dict[tuple[type[Model], object], str] = {
            (Klantcontact, pk): datum for pk, datum in klantcontact_datums.items()
        }
        object_datums.update(
            {(Partij, pk): datum for pk, datum in partij_datums.items()}
        )
        self._resolve_object_datums(collector, object_datums)

        records = []
        for model, objs in collector.data.items():
            type_label = _record_type_label(model)
            for obj in objs:
                datum = object_datums[(model, obj.pk)]
                records.append(
                    {
                        "identificatie": str(obj.uuid),
                        "type": type_label,
                        "aangemaakt": datum,
                        "gesloten": datum,
                    }
                )

        records.sort(
            key=lambda record: (
                record["gesloten"],
                record["type"],
                record["identificatie"],
            )
        )
        return records

    @staticmethod
    def _resolve_object_datums(
        collector: Collector, object_datums: dict[tuple[type[Model], object], str]
    ) -> None:
        pending = [
            obj
            for objs in collector.data.values()
            for obj in objs
            if (type(obj), obj.pk) not in object_datums
        ]
        while pending:
            still_pending = []
            progressed = False
            for obj in pending:
                datum = Command._find_related_datum(obj, object_datums)
                if datum is None:
                    still_pending.append(obj)
                    continue
                object_datums[(type(obj), obj.pk)] = datum
                progressed = True
            if not progressed:
                raise AssertionError(
                    "Kan geen sluitingsdatum bepalen voor de volgende records bij "
                    f"het opbouwen van de vernietigingslijst: {still_pending!r}"
                )
            pending = still_pending

    @staticmethod
    def _find_related_datum(
        obj: Model, object_datums: dict[tuple[type[Model], object], str]
    ) -> str | None:
        """
        Find a known destruction date from a related record.

        Some records don't have their own date, so they use the date of a related
        record that has already been resolved.
        """
        for field in type(obj)._meta.get_fields():
            if not getattr(field, "concrete", False):
                continue
            if not (field.many_to_one or field.one_to_one):
                continue
            value = getattr(obj, field.attname, None)
            if value is None:
                continue
            related_key = (field.related_model, value)
            if related_key in object_datums:
                return object_datums[related_key]
        return None

    def delete_klantcontacten(self, collector: Collector, record_count: int) -> int:
        collector.delete()
        return record_count
