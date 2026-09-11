from datetime import datetime, timezone as dt_timezone
from io import StringIO

from django.core.management import CommandError, call_command
from django.test import TestCase

from freezegun.api import freeze_time

from openklant.components.klantinteracties.models.actoren import (
    Actor,
    ActorKlantcontact,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Bijlage,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.klantinteracties.models.partijen import Partij
from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    ActorKlantcontactFactory,
    BetrokkeneFactory,
    BijlageFactory,
    DigitaalAdresFactory,
    InterneTaakFactory,
    KlantcontactFactory,
    OnderwerpobjectFactory,
    PartijFactory,
)


def _run_command(*args) -> str:
    stdout = StringIO()
    call_command("delete_klantcontacten_not_related_to_zaken", *args, stdout=stdout)
    return stdout.getvalue()


class DeleteKlantcontactenNotRelatedToZakenTests(TestCase):
    def test_dry_run_by_default_does_not_delete(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )

        output = _run_command()

        self.assertTrue(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertIn("Modus: previewmodus", output)
        self.assertNotIn("Bewijs van vernietiging", output)

    def test_no_dry_run_deletes_klantcontact_not_related_to_zaak(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )

        output = _run_command("--no-dry-run")

        self.assertFalse(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertIn("Modus: vernietigingsmodus", output)
        self.assertIn("Bewijs van vernietiging", output)
        self.assertIn("1 records vernietigd", output)
        self.assertIn("overeenkomstig de vernietigingslijst.", output)

    def test_klantcontact_related_to_zaak_via_klantcontact_side_is_kept(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=None,
            onderwerpobjectidentificator_code_objecttype="zaak",
        )

        output = _run_command("--no-dry-run")

        self.assertTrue(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertIn("Totaal aantal geselecteerde records: 0", output)

    def test_klantcontact_related_to_zaak_via_was_klantcontact_side_is_kept(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        OnderwerpobjectFactory.create(
            klantcontact=None,
            was_klantcontact=klantcontact,
            onderwerpobjectidentificator_code_objecttype="ZAAK",
        )

        output = _run_command("--no-dry-run")

        self.assertTrue(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertIn("Totaal aantal geselecteerde records: 0", output)

    def test_klantcontact_related_to_non_zaak_onderwerpobject_is_deleted(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=None,
            onderwerpobjectidentificator_code_objecttype="document",
        )

        _run_command("--no-dry-run")

        self.assertFalse(Klantcontact.objects.filter(pk=klantcontact.pk).exists())

    def test_deleting_eligible_klantcontact_cascades_shared_onderwerpobject_but_keeps_other_side(
        self,
    ):
        eligible = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        kept = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        OnderwerpobjectFactory.create(
            klantcontact=kept,
            was_klantcontact=None,
            onderwerpobjectidentificator_code_objecttype="zaak",
        )
        shared_onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=kept,
            was_klantcontact=eligible,
            onderwerpobjectidentificator_code_objecttype="document",
        )

        _run_command("--no-dry-run")

        self.assertFalse(Klantcontact.objects.filter(pk=eligible.pk).exists())
        self.assertTrue(Klantcontact.objects.filter(pk=kept.pk).exists())
        self.assertFalse(
            Onderwerpobject.objects.filter(pk=shared_onderwerpobject.pk).exists()
        )

    def test_minimum_date_excludes_older_klantcontacten(self):
        too_old = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2019, 12, 31, tzinfo=dt_timezone.utc)
        )
        in_range = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )

        _run_command("--no-dry-run", "--minimum-date", "2020-01-01")

        self.assertTrue(Klantcontact.objects.filter(pk=too_old.pk).exists())
        self.assertFalse(Klantcontact.objects.filter(pk=in_range.pk).exists())

    def test_maximum_date_excludes_newer_klantcontacten(self):
        in_range = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        too_new = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 2, tzinfo=dt_timezone.utc)
        )

        _run_command("--no-dry-run", "--maximum-date", "2020-01-01")

        self.assertFalse(Klantcontact.objects.filter(pk=in_range.pk).exists())
        self.assertTrue(Klantcontact.objects.filter(pk=too_new.pk).exists())

    def test_minimum_date_after_maximum_date_raises(self):
        with self.assertRaises(CommandError):
            call_command(
                "delete_klantcontacten_not_related_to_zaken",
                "--minimum-date",
                "2020-06-01",
                "--maximum-date",
                "2020-01-01",
                stdout=StringIO(),
            )

    def test_invalid_date_format_raises(self):
        with self.assertRaises(CommandError):
            call_command(
                "delete_klantcontacten_not_related_to_zaken",
                "--minimum-date",
                "not-a-date",
                stdout=StringIO(),
            )

    @freeze_time("2026-09-11")
    def test_default_maximum_date_is_last_day_of_previous_month_minus_one_year(self):
        output = _run_command()

        self.assertIn("Sluitingsdatum maximum: 2025-08-31", output)

    @freeze_time("2028-03-01")
    def test_default_maximum_date_handles_leap_day_in_previous_month(self):
        output = _run_command()

        self.assertIn("Sluitingsdatum maximum: 2027-02-28", output)

    def test_cascade_deletes_related_objects(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        betrokkene = BetrokkeneFactory.create(klantcontact=klantcontact, partij=None)
        bijlage = BijlageFactory.create(klantcontact=klantcontact)
        interne_taak = InterneTaakFactory.create(klantcontact=klantcontact)
        actor = ActorFactory.create()
        actor_klantcontact = ActorKlantcontactFactory.create(
            klantcontact=klantcontact, actor=actor
        )
        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=None,
            onderwerpobjectidentificator_code_objecttype="document",
        )
        orphan_digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=betrokkene, partij=None
        )

        _run_command("--no-dry-run")

        self.assertFalse(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertFalse(Betrokkene.objects.filter(pk=betrokkene.pk).exists())
        self.assertFalse(Bijlage.objects.filter(pk=bijlage.pk).exists())
        self.assertFalse(InterneTaak.objects.filter(pk=interne_taak.pk).exists())
        self.assertFalse(
            ActorKlantcontact.objects.filter(pk=actor_klantcontact.pk).exists()
        )
        self.assertTrue(Actor.objects.filter(pk=actor.pk).exists())
        self.assertFalse(Onderwerpobject.objects.filter(pk=onderwerpobject.pk).exists())
        self.assertFalse(
            DigitaalAdres.objects.filter(pk=orphan_digitaal_adres.pk).exists()
        )

    def test_trailing_partij_deleted_when_no_longer_referenced(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        partij = PartijFactory.create()
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)

        _run_command("--no-dry-run")

        self.assertFalse(Partij.objects.filter(pk=partij.pk).exists())

    def test_partij_kept_when_still_referenced_by_other_betrokkene(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        other_klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        OnderwerpobjectFactory.create(
            klantcontact=other_klantcontact,
            was_klantcontact=None,
            onderwerpobjectidentificator_code_objecttype="zaak",
        )
        partij = PartijFactory.create()
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)
        BetrokkeneFactory.create(klantcontact=other_klantcontact, partij=partij)

        _run_command("--no-dry-run")

        self.assertFalse(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertTrue(Klantcontact.objects.filter(pk=other_klantcontact.pk).exists())
        self.assertTrue(Partij.objects.filter(pk=partij.pk).exists())

    def test_digitaal_adres_with_partij_is_kept(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        partij = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create(klantcontact=klantcontact, partij=None)
        digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=betrokkene, partij=partij
        )

        _run_command("--no-dry-run")

        self.assertTrue(DigitaalAdres.objects.filter(pk=digitaal_adres.pk).exists())

    def test_output_lists_klantcontact_and_related_interne_taak_as_separate_records(
        self,
    ):
        klantcontact = KlantcontactFactory.create(
            nummer="1234567890",
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc),
        )
        InterneTaakFactory.create(klantcontact=klantcontact, nummer="9876543210")

        output = _run_command()

        expected_datum = "2020-01-01T00:00:00+00:00"
        self.assertIn(
            f"Record 1234567890 Contactmoment {expected_datum} {expected_datum}",
            output,
        )
        self.assertIn(
            f"Record 9876543210 Contactverzoek {expected_datum} {expected_datum}",
            output,
        )
        self.assertIn("Totaal aantal geselecteerde records: 2", output)

    @freeze_time("2026-09-11")
    def test_maximum_date_less_than_twelve_months_in_the_past_raises(self):
        with self.assertRaises(CommandError):
            call_command(
                "delete_klantcontacten_not_related_to_zaken",
                "--maximum-date",
                "2026-03-11",
                stdout=StringIO(),
            )

    @freeze_time("2026-09-11")
    def test_maximum_date_exactly_twelve_months_in_the_past_is_allowed(self):
        output = _run_command("--maximum-date", "2025-09-11")

        self.assertIn("Sluitingsdatum maximum: 2025-09-11", output)
