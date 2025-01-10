from openklant.tests.test_migrate import BaseMigrationTest


class TestCountryConverter(BaseMigrationTest):
    app = "contactgegevens"
    migrate_from = "0003_alter_persoon_overlijdensdatum"
    migrate_to = "0004_alter_organisatie_adres_land_alter_organisatie_land_and_more"

    def test_migrate_organisatie_model(self):

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

    def test_migrate_persoon_model(self):

        Persoon = self.old_app_state.get_model("contactgegevens", "Persoon")

        Persoon.objects.create(
            land="6030",
            adres_land="6030",
            geboortedatum="1980-02-23",
        )

        self._perform_migration()

        Persoon = self.apps.get_model("contactgegevens", "Persoon")

        records = Persoon.objects.all()
        self.assertEqual(records.count(), 1)
        self.assertEqual(records[0].land, "NL")
        self.assertEqual(records[0].adres_land, "NL")
        self.assertNotEqual(records[0].land, "6030")
        self.assertNotEqual(records[0].adres_land, "6030")
