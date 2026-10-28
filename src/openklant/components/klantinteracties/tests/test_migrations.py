from django.db import IntegrityError, transaction

from openklant.tests.test_migrate import BaseMigrationTest


class TestCountryConverter(BaseMigrationTest):
    app = "klantinteracties"
    migrate_from = (
        "0025_alter_partijidentificator_partij_identificator_code_objecttype_and_more"
    )
    migrate_to = "0026_alter_betrokkene_bezoekadres_land_and_more"

    def test_ok_migration_betrokkene_model(self):
        Betrokkene = self.old_app_state.get_model("klantinteracties", "Betrokkene")
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False),
            initiator=False,
            bezoekadres_land="6030",
            correspondentieadres_land="6030",
        )

        self._perform_migration()

        Betrokkene = self.apps.get_model("klantinteracties", "Betrokkene")

        records = Betrokkene.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_land, "NL")
        self.assertEqual(records[0].correspondentieadres_land, "NL")
        self.assertNotEqual(records[0].bezoekadres_land, "6030")
        self.assertNotEqual(records[0].correspondentieadres_land, "6030")

    def test_ok_migration_betrokkene_model_empty_code(self):
        Betrokkene = self.old_app_state.get_model("klantinteracties", "Betrokkene")
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        betrokken1 = Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False, nummer=123),
            initiator=False,
            bezoekadres_land="",
            correspondentieadres_land="",
        )

        betrokken2 = Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False, nummer=456),
            initiator=False,
            bezoekadres_land="6030",
            correspondentieadres_land="6030",
        )

        self._perform_migration()

        Betrokkene = self.apps.get_model("klantinteracties", "Betrokkene")

        records = Betrokkene.objects.all()
        betrokken1 = records.get(pk=betrokken1.pk)
        betrokken2 = records.get(pk=betrokken2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(betrokken1.bezoekadres_land, "")
        self.assertEqual(betrokken1.correspondentieadres_land, "")
        self.assertEqual(betrokken2.bezoekadres_land, "NL")
        self.assertEqual(betrokken2.correspondentieadres_land, "NL")
        self.assertNotEqual(betrokken2.bezoekadres_land, "6030")
        self.assertNotEqual(betrokken2.correspondentieadres_land, "6030")

    def test_ko_migration_betrokkene_model_wrong_code(self):
        Betrokkene = self.old_app_state.get_model("klantinteracties", "Betrokkene")
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        betrokken1 = Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False, nummer=123),
            initiator=False,
            bezoekadres_land="9999",
            correspondentieadres_land="9999",
        )

        betrokken2 = Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False, nummer=456),
            initiator=False,
            bezoekadres_land="5001",
            correspondentieadres_land="5001",
        )

        with self.assertRaises(IntegrityError) as error:
            self._perform_migration()

        self.assertEqual(
            (
                "The migration cannot proceed due to 1 records that don't comply with the "
                "Betrokkene model's requirements. Possible data inconsistency or mapping error."
            ),
            str(error.exception),
        )

        records = Betrokkene.objects.all()
        betrokken1 = records.get(pk=betrokken1.pk)
        betrokken2 = records.get(pk=betrokken2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(betrokken1.bezoekadres_land, "9999")
        self.assertEqual(betrokken1.correspondentieadres_land, "9999")
        self.assertEqual(betrokken2.bezoekadres_land, "5001")
        self.assertEqual(betrokken2.correspondentieadres_land, "5001")

        # Update manually
        betrokken1 = records.get(pk=betrokken1.pk)
        betrokken1.bezoekadres_land = "6030"
        betrokken1.correspondentieadres_land = "6030"
        betrokken1.save()

        # Re-Run the migration
        self._perform_migration()

        Betrokkene = self.apps.get_model("klantinteracties", "Betrokkene")

        records = Betrokkene.objects.all()
        betrokken1 = records.get(pk=betrokken1.pk)
        betrokken2 = records.get(pk=betrokken2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(betrokken1.bezoekadres_land, "NL")
        self.assertEqual(betrokken1.correspondentieadres_land, "NL")
        self.assertEqual(betrokken2.bezoekadres_land, "CA")
        self.assertEqual(betrokken2.correspondentieadres_land, "CA")

    def test_ok_migration_partij_model(self):
        Partij = self.old_app_state.get_model("klantinteracties", "Partij")

        Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_land="6030",
            correspondentieadres_land="6030",
        )

        self._perform_migration()

        Partij = self.apps.get_model("klantinteracties", "Partij")

        records = Partij.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_land, "NL")
        self.assertEqual(records[0].correspondentieadres_land, "NL")
        self.assertNotEqual(records[0].bezoekadres_land, "6030")
        self.assertNotEqual(records[0].correspondentieadres_land, "6030")

    def test_ok_migration_partij_model_empty_code(self):
        Partij = self.old_app_state.get_model("klantinteracties", "Partij")

        partij1 = Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_land="",
            correspondentieadres_land="",
            nummer=123,
        )
        partij2 = Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_land="6030",
            correspondentieadres_land="6030",
            nummer=456,
        )

        self._perform_migration()

        Partij = self.apps.get_model("klantinteracties", "Partij")

        records = Partij.objects.all()
        partij1 = records.get(pk=partij1.pk)
        partij2 = records.get(pk=partij2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(partij1.bezoekadres_land, "")
        self.assertEqual(partij1.correspondentieadres_land, "")
        self.assertEqual(partij2.bezoekadres_land, "NL")
        self.assertEqual(partij2.correspondentieadres_land, "NL")
        self.assertNotEqual(partij2.bezoekadres_land, "6030")
        self.assertNotEqual(partij2.correspondentieadres_land, "6030")

    def test_ko_migration_partij_model_wrong_code(self):
        Partij = self.old_app_state.get_model("klantinteracties", "Partij")

        partij1 = Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_land="9999",
            correspondentieadres_land="9999",
            nummer=123,
        )
        partij2 = Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_land="5001",
            correspondentieadres_land="5001",
            nummer=456,
        )

        with self.assertRaises(IntegrityError) as error:
            self._perform_migration()

        self.assertEqual(
            (
                "The migration cannot proceed due to 1 records that don't comply with the "
                "Partij model's requirements. Possible data inconsistency or mapping error."
            ),
            str(error.exception),
        )

        records = Partij.objects.all()
        partij1 = records.get(pk=partij1.pk)
        partij2 = records.get(pk=partij2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(partij1.bezoekadres_land, "9999")
        self.assertEqual(partij1.correspondentieadres_land, "9999")
        self.assertEqual(partij2.bezoekadres_land, "5001")
        self.assertEqual(partij2.correspondentieadres_land, "5001")

        # Update manually
        partij1 = records.get(pk=partij1.pk)
        partij1.bezoekadres_land = "6030"
        partij1.correspondentieadres_land = "6030"
        partij1.save()

        # Re-Run the migration
        self._perform_migration()

        Partij = self.apps.get_model("klantinteracties", "Partij")

        records = Partij.objects.all()
        partij1 = records.get(pk=partij1.pk)
        partij2 = records.get(pk=partij2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(partij1.bezoekadres_land, "NL")
        self.assertEqual(partij1.correspondentieadres_land, "NL")
        self.assertEqual(partij2.bezoekadres_land, "CA")
        self.assertEqual(partij2.correspondentieadres_land, "CA")


class TestValidateBagId(BaseMigrationTest):
    app = "klantinteracties"
    migrate_from = "0026_alter_betrokkene_bezoekadres_land_and_more"
    migrate_to = "0027_alter_betrokkene_bezoekadres_nummeraanduiding_id_and_more"

    def test_ok_migration_betrokkene_model(self):
        Betrokkene = self.old_app_state.get_model("klantinteracties", "Betrokkene")
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False),
            initiator=False,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            correspondentieadres_nummeraanduiding_id="1234567890000002",
        )

        self._perform_migration()

        Betrokkene = self.apps.get_model("klantinteracties", "Betrokkene")

        records = Betrokkene.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_nummeraanduiding_id, "1234567890000001")
        self.assertEqual(
            records[0].correspondentieadres_nummeraanduiding_id, "1234567890000002"
        )

    def test_ok_migration_betrokkene_model_empty_value(self):
        Betrokkene = self.old_app_state.get_model("klantinteracties", "Betrokkene")
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False),
            initiator=False,
            bezoekadres_nummeraanduiding_id="",
            correspondentieadres_nummeraanduiding_id="",
        )

        self._perform_migration()

        Betrokkene = self.apps.get_model("klantinteracties", "Betrokkene")

        records = Betrokkene.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_nummeraanduiding_id, "")
        self.assertEqual(records[0].correspondentieadres_nummeraanduiding_id, "")

    def test_ko_migration_betrokkene_model_wrong_code(self):
        Betrokkene = self.old_app_state.get_model("klantinteracties", "Betrokkene")
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False),
            initiator=False,
            bezoekadres_nummeraanduiding_id="123456",
            correspondentieadres_nummeraanduiding_id="789",
        )

        with self.assertRaises(IntegrityError) as error:
            self._perform_migration()

        self.assertEqual(
            (
                "The migration cannot proceed due to 1 records that don't comply with the "
                "Betrokkene model's requirements. Possible data inconsistency or mapping error."
            ),
            str(error.exception),
        )

        records = Betrokkene.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_nummeraanduiding_id, "123456")
        self.assertEqual(records[0].correspondentieadres_nummeraanduiding_id, "789")

        # Update manually
        betrokken = records.get(pk=records[0].pk)
        betrokken.bezoekadres_nummeraanduiding_id = "1234567890000001"
        betrokken.correspondentieadres_nummeraanduiding_id = "1234567890000002"
        betrokken.save()

        # Re-Run the migration
        self._perform_migration()

        Betrokkene = self.apps.get_model("klantinteracties", "Betrokkene")

        records = Betrokkene.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_nummeraanduiding_id, "1234567890000001")
        self.assertEqual(
            records[0].correspondentieadres_nummeraanduiding_id, "1234567890000002"
        )
        self.assertNotEqual(records[0].bezoekadres_nummeraanduiding_id, "123456")
        self.assertNotEqual(records[0].correspondentieadres_nummeraanduiding_id, "789")

    def test_ok_migration_partij_model(self):
        Partij = self.old_app_state.get_model("klantinteracties", "Partij")

        Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            correspondentieadres_nummeraanduiding_id="1234567890000002",
        )

        self._perform_migration()

        Partij = self.apps.get_model("klantinteracties", "Partij")

        records = Partij.objects.all()

        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_nummeraanduiding_id, "1234567890000001")
        self.assertEqual(
            records[0].correspondentieadres_nummeraanduiding_id, "1234567890000002"
        )

    def test_ok_migration_partij_model_empty_value(self):
        Partij = self.old_app_state.get_model("klantinteracties", "Partij")

        Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="",
            correspondentieadres_nummeraanduiding_id="",
        )

        self._perform_migration()

        Partij = self.apps.get_model("klantinteracties", "Partij")

        records = Partij.objects.all()

        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_nummeraanduiding_id, "")
        self.assertEqual(records[0].correspondentieadres_nummeraanduiding_id, "")

    def test_ko_migration_partij_model_wrong_code(self):
        Partij = self.old_app_state.get_model("klantinteracties", "Partij")

        Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="ABC",
            correspondentieadres_nummeraanduiding_id="DEF",
        )

        with self.assertRaises(IntegrityError) as error:
            self._perform_migration()

        self.assertEqual(
            (
                "The migration cannot proceed due to 1 records that don't comply with the "
                "Partij model's requirements. Possible data inconsistency or mapping error."
            ),
            str(error.exception),
        )

        records = Partij.objects.all()

        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_nummeraanduiding_id, "ABC")
        self.assertEqual(records[0].correspondentieadres_nummeraanduiding_id, "DEF")

        # Update manually
        partij1 = records.get(pk=records[0].pk)
        partij1.bezoekadres_nummeraanduiding_id = "1234567890000001"
        partij1.correspondentieadres_nummeraanduiding_id = "1234567890000002"
        partij1.save()

        # Re-Run the migration
        self._perform_migration()

        Partij = self.apps.get_model("klantinteracties", "Partij")

        records = Partij.objects.all()

        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].bezoekadres_nummeraanduiding_id, "1234567890000001")
        self.assertEqual(
            records[0].correspondentieadres_nummeraanduiding_id, "1234567890000002"
        )
        self.assertNotEqual(records[0].bezoekadres_nummeraanduiding_id, "ABC")
        self.assertNotEqual(records[0].correspondentieadres_nummeraanduiding_id, "DEF")


class TestNummerAutogenerate(BaseMigrationTest):
    app = "klantinteracties"
    migrate_from = "0048_klantcontact_hoofd_onderwerp_type_and_more"
    migrate_to = "0049_backfill_nummer_and_autogeneration"

    def test_existing_nummers_are_not_changed(self):
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        klantcontact1 = Klantcontact.objects.create(vertrouwelijk=False, nummer="1")
        klantcontact2 = Klantcontact.objects.create(vertrouwelijk=False, nummer="123")
        klantcontact3 = Klantcontact.objects.create(
            vertrouwelijk=False, nummer="0000000456"
        )

        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")

        self.assertEqual(Klantcontact.objects.get(pk=klantcontact1.pk).nummer, "1")
        self.assertEqual(Klantcontact.objects.get(pk=klantcontact2.pk).nummer, "123")
        self.assertEqual(
            Klantcontact.objects.get(pk=klantcontact3.pk).nummer, "0000000456"
        )

    def test_saving_existing_record_keeps_old_nummer(self):
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")
        klantcontact = Klantcontact.objects.create(vertrouwelijk=False, nummer="123")

        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")

        klantcontact = Klantcontact.objects.get(pk=klantcontact.pk)
        klantcontact.save()
        klantcontact.refresh_from_db()

        self.assertEqual(klantcontact.nummer, "123")

    def test_empty_and_null_nummers_are_generated(self):
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        existing = Klantcontact.objects.create(vertrouwelijk=False, nummer="0000000010")
        empty = Klantcontact.objects.create(vertrouwelijk=False, nummer="")
        null1 = Klantcontact.objects.create(vertrouwelijk=False, nummer=None)
        null2 = Klantcontact.objects.create(vertrouwelijk=False, nummer=None)

        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")

        records = Klantcontact.objects.all()
        self.assertEqual(records.count(), 4)
        # existing nummer unchanged
        self.assertEqual(records.get(pk=existing.pk).nummer, "0000000010")
        # the sequence continues after the highest existing number; the order
        # in which the backfill assigns them is not guaranteed
        self.assertEqual(
            {records.get(pk=obj.pk).nummer for obj in (empty, null1, null2)},
            {"000000000011", "000000000012", "000000000013"},
        )

    def test_manual_nummer_is_padded_and_moves_sequence(self):
        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")

        manual = Klantcontact.objects.create(vertrouwelijk=False, nummer="500")
        manual.refresh_from_db()
        self.assertEqual(manual.nummer, "000000000500")

        generated = Klantcontact.objects.create(vertrouwelijk=False, nummer="")
        generated.refresh_from_db()
        self.assertEqual(generated.nummer, "000000000501")

        # skip numbers from 502 to 799
        jump = Klantcontact.objects.create(vertrouwelijk=False, nummer="800")
        jump.refresh_from_db()
        self.assertEqual(jump.nummer, "000000000800")

        generated = Klantcontact.objects.create(vertrouwelijk=False, nummer="")
        generated.refresh_from_db()
        self.assertEqual(generated.nummer, "000000000801")

    def test_lower_manual_nummer_does_not_move_sequence_back(self):
        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")

        Klantcontact.objects.create(vertrouwelijk=False, nummer="100")
        Klantcontact.objects.create(vertrouwelijk=False, nummer="30")

        # the sequence never goes back
        generated = Klantcontact.objects.create(vertrouwelijk=False, nummer="")
        generated.refresh_from_db()
        self.assertEqual(generated.nummer, "000000000101")

    def test_max_nummer_does_not_block_generation(self):
        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")

        Klantcontact.objects.create(vertrouwelijk=False, nummer="999999999999")
        generated = Klantcontact.objects.create(vertrouwelijk=False, nummer="")
        generated.refresh_from_db()

        # the sequence cycles and restarts from the first free number
        self.assertEqual(generated.nummer, "000000000001")

    def test_generation_ignores_numbers_in_old_format(self):
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        Klantcontact.objects.create(vertrouwelijk=False, nummer="0000000001")
        Klantcontact.objects.create(vertrouwelijk=False, nummer="2")

        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")

        # make the sequence cycle back to 1
        Klantcontact.objects.create(vertrouwelijk=False, nummer="999999999999")
        generated = Klantcontact.objects.create(vertrouwelijk=False, nummer="")
        generated.refresh_from_db()

        # old formats are different strings: they don't block the 12 digit ones
        self.assertEqual(generated.nummer, "000000000001")

    def test_all_models(self):
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")
        Partij = self.old_app_state.get_model("klantinteracties", "Partij")
        InterneTaak = self.old_app_state.get_model("klantinteracties", "InterneTaak")

        klantcontact = Klantcontact.objects.create(vertrouwelijk=False, nummer="7")
        partij = Partij.objects.create(
            soort_partij="persoon", indicatie_actief=True, nummer=None
        )
        internetaak = InterneTaak.objects.create(
            klantcontact=klantcontact,
            gevraagde_handeling="Terugbellen",
            status="te_verwerken",
            nummer="",
        )

        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")
        Partij = self.apps.get_model("klantinteracties", "Partij")
        InterneTaak = self.apps.get_model("klantinteracties", "InterneTaak")

        # existing nummer unchanged
        self.assertEqual(Klantcontact.objects.get(pk=klantcontact.pk).nummer, "7")
        # every table has its own sequence
        self.assertEqual(Partij.objects.get(pk=partij.pk).nummer, "000000000001")
        self.assertEqual(
            InterneTaak.objects.get(pk=internetaak.pk).nummer, "000000000001"
        )

    def test_no_integrity_error_without_nummer(self):
        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")

        for nummer in ("", "", None, None):
            Klantcontact.objects.create(vertrouwelijk=False, nummer=nummer)

        nummers = list(Klantcontact.objects.values_list("nummer", flat=True))
        self.assertEqual(len(nummers), 4)
        self.assertEqual(len(set(nummers)), 4)
        self.assertNotIn("", nummers)
        self.assertNotIn(None, nummers)

    def test_unique_constraint_is_still_enforced(self):
        self._perform_migration()

        Klantcontact = self.apps.get_model("klantinteracties", "Klantcontact")
        Klantcontact.objects.create(vertrouwelijk=False, nummer="56")

        # "56" and "000000000056" are both stored as "000000000056"
        for nummer in ("56", "000000000056"):
            with self.subTest(nummer=nummer):
                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        Klantcontact.objects.create(vertrouwelijk=False, nummer=nummer)
