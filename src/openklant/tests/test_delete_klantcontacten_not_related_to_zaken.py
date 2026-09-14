import os
import re
from datetime import datetime, timezone as dt_timezone
from io import StringIO
from unittest import mock

from django.core.management import CommandError, call_command
from django.test import TestCase

from freezegun.api import freeze_time

from openklant.components.klantinteracties.models.actoren import (
    Actor,
    ActorKlantcontact,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.internetaken import (
    InterneTaak,
    InterneTakenActorenThoughModel,
)
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Bijlage,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.klantinteracties.models.partijen import (
    CategorieRelatie,
    Contactpersoon,
    Partij,
    PartijIdentificator,
    Vertegenwoordigden,
)
from openklant.components.klantinteracties.models.rekeningnummers import Rekeningnummer
from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    ActorKlantcontactFactory,
    BetrokkeneFactory,
    BijlageFactory,
    BsnPartijIdentificatorFactory,
    CategorieFactory,
    CategorieRelatieFactory,
    ContactpersoonFactory,
    DigitaalAdresFactory,
    InterneTaakFactory,
    KlantcontactFactory,
    OnderwerpobjectFactory,
    PartijFactory,
    PersoonFactory,
    RekeningnummerFactory,
    VertegenwoordigdenFactory,
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

    @mock.patch.dict(
        os.environ, {"KLANTCONTACT_CLEANUP_ZAAK_OBJECTTYPE": "zaakidentificatie"}
    )
    def test_zaak_objecttype_env_var_overrides_default(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=None,
            onderwerpobjectidentificator_code_objecttype="zaakidentificatie",
        )

        output = _run_command("--no-dry-run")

        self.assertTrue(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertIn("Totaal aantal geselecteerde records: 0", output)

    @mock.patch.dict(
        os.environ, {"KLANTCONTACT_CLEANUP_ZAAK_OBJECTTYPE": "zaakidentificatie"}
    )
    def test_default_objecttype_is_no_longer_recognized_when_env_var_overridden(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=None,
            onderwerpobjectidentificator_code_objecttype="zaak",
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
        self.assertTrue(Partij.objects.filter(pk=partij.pk).exists())

    def test_output_lists_klantcontact_and_related_interne_taak_as_separate_records(
        self,
    ):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc),
        )
        interne_taak = InterneTaakFactory.create(klantcontact=klantcontact)

        output = _run_command()

        expected_datum = "2020-01-01T00:00:00+00:00"
        self.assertIn(
            f"Record {klantcontact.uuid} Klantcontact {expected_datum} "
            f"{expected_datum}",
            output,
        )
        self.assertIn(
            f"Record {interne_taak.uuid} Interne taak {expected_datum} "
            f"{expected_datum}",
            output,
        )
        self.assertIn("Totaal aantal geselecteerde records: 2", output)

    def test_output_explicitly_lists_all_related_records(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        partij = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)
        bijlage = BijlageFactory.create(klantcontact=klantcontact)
        actor = ActorFactory.create()
        actor_klantcontact = ActorKlantcontactFactory.create(
            klantcontact=klantcontact, actor=actor
        )
        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=None,
            onderwerpobjectidentificator_code_objecttype="document",
        )
        digitaal_adres = DigitaalAdresFactory.create(betrokkene=betrokkene, partij=None)

        output = _run_command()

        expected_datum = "2020-01-01T00:00:00+00:00"

        def _assert_record_listed(identificatie: str, type_: str) -> None:
            pattern = (
                rf"Record\s+{re.escape(str(identificatie))}\s+{re.escape(type_)}\s+"
                rf"{re.escape(expected_datum)}\s+{re.escape(expected_datum)}"
            )
            self.assertRegex(output, pattern)

        _assert_record_listed(betrokkene.uuid, "Betrokkene bij klantcontact")
        _assert_record_listed(actor_klantcontact.uuid, "Actor klantcontact")
        _assert_record_listed(onderwerpobject.uuid, "Onderwerpobject")
        _assert_record_listed(bijlage.uuid, "Bijlage")
        _assert_record_listed(digitaal_adres.uuid, "Digitaal adres")
        _assert_record_listed(partij.uuid, "Partij")
        self.assertIn("Totaal aantal geselecteerde records: 7", output)

    def test_shared_onderwerpobject_between_two_eligible_klantcontacten_is_listed_once(
        self,
    ):
        first = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        second = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 2, tzinfo=dt_timezone.utc)
        )
        shared_onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=first,
            was_klantcontact=second,
            onderwerpobjectidentificator_code_objecttype="document",
        )

        output = _run_command()

        self.assertEqual(output.count(f"Record {shared_onderwerpobject.uuid}"), 1)
        self.assertIn("Totaal aantal geselecteerde records: 3", output)

    def test_output_lists_full_partij_cascade_when_partij_becomes_orphaned(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="persoon"
        )
        other_partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="organisatie"
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)

        rekeningnummer = RekeningnummerFactory.create(partij=partij)
        categorie = CategorieFactory.create()
        categorie_relatie = CategorieRelatieFactory.create(
            partij=partij, categorie=categorie
        )
        partij_identificator = BsnPartijIdentificatorFactory.create(partij=partij)
        vertegenwoordigden = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij, vertegenwoordigde_partij=other_partij
        )
        persoon = PersoonFactory.create(partij=partij)

        output = _run_command()

        expected_datum = "2020-01-01T00:00:00+00:00"

        def _assert_record_listed(identificatie, type_: str) -> None:
            pattern = (
                rf"Record\s+{re.escape(str(identificatie))}\s+{re.escape(type_)}\s+"
                rf"{re.escape(expected_datum)}\s+{re.escape(expected_datum)}"
            )
            self.assertRegex(output, pattern)

        _assert_record_listed(rekeningnummer.uuid, "Rekeningnummer")
        _assert_record_listed(categorie_relatie.uuid, "Categorie relatie")
        _assert_record_listed(partij_identificator.uuid, "Partij identificator")
        _assert_record_listed(vertegenwoordigden.uuid, "Vertegenwoordigde")
        _assert_record_listed(persoon.uuid, "Persoon")
        self.assertIn("Totaal aantal geselecteerde records: 8", output)

    def test_no_dry_run_deletes_full_partij_cascade_but_keeps_unrelated_partijen(
        self,
    ):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="persoon"
        )
        other_partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="organisatie"
        )
        employee_partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="persoon"
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)

        rekeningnummer = RekeningnummerFactory.create(partij=partij)
        partij_identificator = BsnPartijIdentificatorFactory.create(partij=partij)
        vertegenwoordigden = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij, vertegenwoordigde_partij=other_partij
        )
        own_contactpersoon = ContactpersoonFactory.create(
            partij=PartijFactory.create(
                voorkeurs_digitaal_adres=None, soort_partij="contactpersoon"
            ),
            werkte_voor_partij=None,
        )
        employee_contactpersoon = ContactpersoonFactory.create(
            partij=employee_partij, werkte_voor_partij=partij
        )

        output = _run_command("--no-dry-run")

        self.assertIn("7 records vernietigd", output)

        self.assertFalse(Partij.objects.filter(pk=partij.pk).exists())
        self.assertFalse(Rekeningnummer.objects.filter(pk=rekeningnummer.pk).exists())
        self.assertFalse(
            PartijIdentificator.objects.filter(pk=partij_identificator.pk).exists()
        )
        self.assertFalse(CategorieRelatie.objects.filter(partij_id=partij.pk).exists())
        self.assertFalse(
            Vertegenwoordigden.objects.filter(pk=vertegenwoordigden.pk).exists()
        )
        self.assertFalse(
            Contactpersoon.objects.filter(pk=employee_contactpersoon.pk).exists()
        )

        self.assertTrue(Partij.objects.filter(pk=other_partij.pk).exists())
        self.assertTrue(Partij.objects.filter(pk=employee_partij.pk).exists())
        self.assertTrue(
            Contactpersoon.objects.filter(pk=own_contactpersoon.pk).exists()
        )

    def test_output_lists_and_deletes_interne_taak_actor_toewijzing(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        interne_taak = InterneTaakFactory.create(klantcontact=klantcontact)
        actor = ActorFactory.create()
        toewijzing = InterneTakenActorenThoughModel.objects.create(
            actor=actor, internetaak=interne_taak
        )

        output = _run_command()

        expected_datum = "2020-01-01T00:00:00+00:00"
        pattern = (
            rf"Record\s+{re.escape(str(toewijzing.uuid))}\s+"
            rf"{re.escape('Interne taak - toegewezen actor')}\s+"
            rf"{re.escape(expected_datum)}\s+{re.escape(expected_datum)}"
        )
        self.assertRegex(output, pattern)

        _run_command("--no-dry-run")

        self.assertFalse(
            InterneTakenActorenThoughModel.objects.filter(pk=toewijzing.pk).exists()
        )
        self.assertTrue(Actor.objects.filter(pk=actor.pk).exists())

    def test_partij_identificator_hierarchy_of_orphaned_partij_is_deleted(self):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="persoon"
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)

        parent_identificator = BsnPartijIdentificatorFactory.create(partij=partij)
        child_identificator = PartijIdentificator.objects.create(
            partij=partij,
            sub_identificator_van=parent_identificator,
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="000000000000",
        )

        output = _run_command()

        self.assertIn(str(parent_identificator.uuid), output)
        self.assertIn(str(child_identificator.uuid), output)

        output = _run_command("--no-dry-run")

        self.assertIn(str(parent_identificator.uuid), output)
        self.assertIn(str(child_identificator.uuid), output)
        self.assertFalse(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertFalse(Partij.objects.filter(pk=partij.pk).exists())
        self.assertFalse(
            PartijIdentificator.objects.filter(pk=parent_identificator.pk).exists()
        )
        self.assertFalse(
            PartijIdentificator.objects.filter(pk=child_identificator.pk).exists()
        )

    def test_sub_identificator_of_other_partij_blocks_deletion_in_preview_mode(self):
        """
        The PROTECT relation is not limited to identificators of the same Partij,
        a kept Partij whose identificator points to an identificator of an
        orphaned Partij also blocks the deletion, even in preview mode.
        """
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        orphaned_partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="persoon"
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=orphaned_partij)
        parent_identificator = BsnPartijIdentificatorFactory.create(
            partij=orphaned_partij
        )

        other_partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="organisatie"
        )
        child_identificator = PartijIdentificator.objects.create(
            partij=other_partij,
            sub_identificator_van=parent_identificator,
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="000000000000",
        )

        with self.assertRaises(CommandError) as context:
            _run_command()

        message = str(context.exception)
        self.assertIn("Partij identificator", message)
        self.assertIn(str(child_identificator.uuid), message)

        self.assertTrue(Klantcontact.objects.filter(pk=klantcontact.pk).exists())
        self.assertTrue(Partij.objects.filter(pk=orphaned_partij.pk).exists())
        self.assertTrue(Partij.objects.filter(pk=other_partij.pk).exists())
        self.assertTrue(
            PartijIdentificator.objects.filter(pk=child_identificator.pk).exists()
        )

    def test_partij_identificator_hierarchy_across_two_orphaned_partijen_is_deleted(
        self,
    ):
        klantcontact = KlantcontactFactory.create(
            plaatsgevonden_op=datetime(2020, 1, 1, tzinfo=dt_timezone.utc)
        )
        parent_partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="persoon"
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=parent_partij)
        parent_identificator = BsnPartijIdentificatorFactory.create(
            partij=parent_partij
        )

        child_partij = PartijFactory.create(
            voorkeurs_digitaal_adres=None, soort_partij="organisatie"
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=child_partij)
        child_identificator = PartijIdentificator.objects.create(
            partij=child_partij,
            sub_identificator_van=parent_identificator,
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="000000000000",
        )

        output = _run_command("--no-dry-run")

        self.assertIn(str(parent_identificator.uuid), output)
        self.assertIn(str(child_identificator.uuid), output)
        self.assertFalse(Partij.objects.filter(pk=parent_partij.pk).exists())
        self.assertFalse(Partij.objects.filter(pk=child_partij.pk).exists())
        self.assertFalse(
            PartijIdentificator.objects.filter(pk=parent_identificator.pk).exists()
        )
        self.assertFalse(
            PartijIdentificator.objects.filter(pk=child_identificator.pk).exists()
        )

    @freeze_time("2026-09-11")
    def test_maximum_date_less_than_twelve_months_in_the_past_raises(self):
        with self.assertRaisesMessage(
            CommandError,
            "maximum-date moet minimaal 12 maanden in het verleden liggen "
            "(dus op of voor 2025-09-11).",
        ):
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
