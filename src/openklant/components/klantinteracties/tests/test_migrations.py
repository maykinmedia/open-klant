from django.db import IntegrityError

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


class TestNewAadresFields(BaseMigrationTest):
    app = "klantinteracties"
    migrate_from = "0027_alter_betrokkene_bezoekadres_nummeraanduiding_id_and_more"
    migrate_to = "0028_betrokkene_bezoekadres_huisnummer_and_more"

    def test_ok_migration_betrokkene_model(self):

        Betrokkene = self.old_app_state.get_model("klantinteracties", "Betrokkene")
        Klantcontact = self.old_app_state.get_model("klantinteracties", "Klantcontact")

        betrokkene = Betrokkene.objects.create(
            partij=None,
            klantcontact=Klantcontact.objects.create(vertrouwelijk=False),
            initiator=False,
        )
        self.assertFalse(hasattr(betrokkene, "bezoekadres_straatnaam"))
        self.assertFalse(hasattr(betrokkene, "bezoekadres_huisnummer"))
        self.assertFalse(hasattr(betrokkene, "bezoekadres_huisnummertoevoeging"))
        self.assertFalse(hasattr(betrokkene, "bezoekadres_postcode"))
        self.assertFalse(hasattr(betrokkene, "bezoekadres_stad"))
        self.assertFalse(hasattr(betrokkene, "correspondentieadres_straatnaam"))
        self.assertFalse(hasattr(betrokkene, "correspondentieadres_huisnummer"))
        self.assertFalse(
            hasattr(betrokkene, "correspondentieadres_huisnummertoevoeging")
        )
        self.assertFalse(hasattr(betrokkene, "correspondentieadres_postcode"))
        self.assertFalse(hasattr(betrokkene, "correspondentieadres_stad"))

        self._perform_migration()

        Betrokkene = self.apps.get_model("klantinteracties", "Betrokkene")

        betrokkene = Betrokkene.objects.get()

        self.assertEqual(betrokkene.bezoekadres_straatnaam, "")
        self.assertEqual(betrokkene.bezoekadres_huisnummer, "")
        self.assertEqual(betrokkene.bezoekadres_huisnummertoevoeging, "")
        self.assertEqual(betrokkene.bezoekadres_postcode, "")
        self.assertEqual(betrokkene.bezoekadres_stad, "")
        self.assertEqual(betrokkene.correspondentieadres_straatnaam, "")
        self.assertEqual(betrokkene.correspondentieadres_huisnummer, "")
        self.assertEqual(betrokkene.correspondentieadres_huisnummertoevoeging, "")
        self.assertEqual(betrokkene.correspondentieadres_postcode, "")
        self.assertEqual(betrokkene.correspondentieadres_stad, "")

    def test_ok_migration_partij_model(self):

        Partij = self.old_app_state.get_model("klantinteracties", "Partij")

        partij = Partij.objects.create(
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="ABC",
            correspondentieadres_nummeraanduiding_id="DEF",
        )
        self.assertFalse(hasattr(partij, "bezoekadres_straatnaam"))
        self.assertFalse(hasattr(partij, "bezoekadres_huisnummer"))
        self.assertFalse(hasattr(partij, "bezoekadres_huisnummertoevoeging"))
        self.assertFalse(hasattr(partij, "bezoekadres_postcode"))
        self.assertFalse(hasattr(partij, "bezoekadres_stad"))

        self.assertFalse(hasattr(partij, "correspondentieadres_straatnaam"))
        self.assertFalse(hasattr(partij, "correspondentieadres_huisnummer"))
        self.assertFalse(hasattr(partij, "correspondentieadres_huisnummertoevoeging"))
        self.assertFalse(hasattr(partij, "correspondentieadres_postcode"))
        self.assertFalse(hasattr(partij, "correspondentieadres_stad"))

        self._perform_migration()

        Partij = self.apps.get_model("klantinteracties", "Partij")

        partij = Partij.objects.get()

        self.assertEqual(partij.bezoekadres_straatnaam, "")
        self.assertEqual(partij.bezoekadres_huisnummer, "")
        self.assertEqual(partij.bezoekadres_huisnummertoevoeging, "")
        self.assertEqual(partij.bezoekadres_postcode, "")
        self.assertEqual(partij.bezoekadres_stad, "")
        self.assertEqual(partij.correspondentieadres_straatnaam, "")
        self.assertEqual(partij.correspondentieadres_huisnummer, "")
        self.assertEqual(partij.correspondentieadres_huisnummertoevoeging, "")
        self.assertEqual(partij.correspondentieadres_postcode, "")
        self.assertEqual(partij.correspondentieadres_stad, "")
