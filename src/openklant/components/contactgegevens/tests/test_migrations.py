from django.db import IntegrityError

from openklant.tests.test_migrate import BaseMigrationTest


class TestCountryConverter(BaseMigrationTest):
    app = "contactgegevens"
    migrate_from = "0003_alter_persoon_overlijdensdatum"
    migrate_to = "0004_alter_organisatie_adres_land_alter_organisatie_land_and_more"

    def test_ok_migration_organisatie_model(self):

        Organisatie = self.old_app_state.get_model("contactgegevens", "Organisatie")

        Organisatie.objects.create(land="6030", adres_land="6030")

        self._perform_migration()

        Organisatie = self.apps.get_model("contactgegevens", "Organisatie")

        records = Organisatie.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].land, "NL")
        self.assertEqual(records[0].adres_land, "NL")
        self.assertNotEqual(records[0].land, "6030")
        self.assertNotEqual(records[0].adres_land, "6030")

    def test_ok_migration_organisatie_model_empty_code(self):

        Organisatie = self.old_app_state.get_model("contactgegevens", "Organisatie")
        org1 = Organisatie.objects.create(land="", adres_land="")
        org2 = Organisatie.objects.create(land="6030", adres_land="6030")

        self._perform_migration()
        Organisatie = self.apps.get_model("contactgegevens", "Organisatie")

        records = Organisatie.objects.all()
        org1 = records.get(pk=org1.pk)
        org2 = records.get(pk=org2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(org1.land, "")
        self.assertEqual(org1.adres_land, "")
        self.assertEqual(org2.land, "NL")
        self.assertEqual(org2.adres_land, "NL")
        self.assertNotEqual(org2.land, "6030")
        self.assertNotEqual(org2.adres_land, "6030")

    def test_ko_migration_organisatie_model_wrong_code(self):

        Organisatie = self.old_app_state.get_model("contactgegevens", "Organisatie")
        org1 = Organisatie.objects.create(land="9999", adres_land="9999")
        org2 = Organisatie.objects.create(land="5001", adres_land="5001")

        with self.assertRaises(IntegrityError) as error:
            self._perform_migration()

        self.assertEqual(
            (
                "The migration cannot proceed due to 1 records that don't comply with the "
                "Organisatie model's requirements. Possible data inconsistency or mapping error."
            ),
            str(error.exception),
        )

        records = Organisatie.objects.all()
        org1 = records.get(pk=org1.pk)
        org2 = records.get(pk=org2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(org1.land, "9999")
        self.assertEqual(org1.adres_land, "9999")
        self.assertEqual(org2.land, "5001")
        self.assertEqual(org2.adres_land, "5001")

        # Update manually
        org1 = records.get(pk=org1.pk)
        org1.land = "6030"
        org1.adres_land = "6030"
        org1.save()

        # Re-Run the migration
        self._perform_migration()
        Organisatie = self.apps.get_model("contactgegevens", "Organisatie")

        records = Organisatie.objects.all()
        org1 = records.get(pk=org1.pk)
        org2 = records.get(pk=org2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(org1.land, "NL")
        self.assertEqual(org1.adres_land, "NL")
        self.assertEqual(org2.land, "CA")
        self.assertEqual(org2.adres_land, "CA")

        self.assertNotEqual(org1.land, "6030")
        self.assertNotEqual(org1.adres_land, "6030")
        self.assertNotEqual(org2.land, "5001")
        self.assertNotEqual(org2.adres_land, "5001")

    def test_ok_migrate_persoon_model(self):

        Persoon = self.old_app_state.get_model("contactgegevens", "Persoon")

        Persoon.objects.create(
            land="6030", adres_land="6030", geboortedatum="1980-02-23"
        )

        self._perform_migration()
        Persoon = self.apps.get_model("contactgegevens", "Persoon")

        records = Persoon.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].land, "NL")
        self.assertEqual(records[0].adres_land, "NL")
        self.assertNotEqual(records[0].land, "6030")
        self.assertNotEqual(records[0].adres_land, "6030")

    def test_ok_migration_persoon_model_empty_code(self):

        Persoon = self.old_app_state.get_model("contactgegevens", "Persoon")

        persoon1 = Persoon.objects.create(
            land="", adres_land="", geboortedatum="1980-02-23"
        )
        persoon2 = Persoon.objects.create(
            land="6030", adres_land="6030", geboortedatum="1980-02-23"
        )

        self._perform_migration()
        Persoon = self.apps.get_model("contactgegevens", "Persoon")

        records = Persoon.objects.all()
        persoon1 = records.get(pk=persoon1.pk)
        persoon2 = records.get(pk=persoon2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(persoon1.land, "")
        self.assertEqual(persoon1.adres_land, "")
        self.assertEqual(persoon2.land, "NL")
        self.assertEqual(persoon2.adres_land, "NL")

    def test_ko_migration_persoon_model_wrong_code(self):

        Persoon = self.old_app_state.get_model("contactgegevens", "Persoon")
        persoon1 = Persoon.objects.create(
            land="9999", adres_land="9999", geboortedatum="1980-02-23"
        )
        persoon2 = Persoon.objects.create(
            land="5001", adres_land="5001", geboortedatum="1980-02-23"
        )

        with self.assertRaises(IntegrityError) as error:
            self._perform_migration()

        self.assertEqual(
            (
                "The migration cannot proceed due to 1 records that don't comply with the "
                "Persoon model's requirements. Possible data inconsistency or mapping error."
            ),
            str(error.exception),
        )

        records = Persoon.objects.all()
        self.assertEqual(records.count(), 2)
        self.assertEqual(persoon1.land, "9999")
        self.assertEqual(persoon1.adres_land, "9999")
        self.assertEqual(persoon2.land, "5001")
        self.assertEqual(persoon2.adres_land, "5001")

        # Update manually
        persoon1 = records.get(pk=persoon1.pk)
        persoon2 = records.get(pk=persoon2.pk)
        persoon1.land = "6030"
        persoon1.adres_land = "6030"
        persoon1.save()

        # Re-Run the migration
        self._perform_migration()
        Persoon = self.apps.get_model("contactgegevens", "Persoon")

        records = Persoon.objects.all()
        persoon1 = records.get(pk=persoon1.pk)
        persoon2 = records.get(pk=persoon2.pk)

        self.assertEqual(records.count(), 2)
        self.assertEqual(persoon1.land, "NL")
        self.assertEqual(persoon1.adres_land, "NL")
        self.assertEqual(persoon2.land, "CA")
        self.assertEqual(persoon2.adres_land, "CA")

        self.assertNotEqual(persoon1.land, "6030")
        self.assertNotEqual(persoon1.adres_land, "6030")
        self.assertNotEqual(persoon2.land, "5001")
        self.assertNotEqual(persoon2.adres_land, "5001")
