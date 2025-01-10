from openklant.tests.test_migrate import BaseMigrationTest


class TestCountryConverter(BaseMigrationTest):
    app = "klantinteracties"
    migrate_from = "0023_alter_digitaaladres_omschrijving"
    migrate_to = "0024_alter_betrokkene_bezoekadres_land_and_more"

    def test_migrate_betrokkene_model(self):

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

    def test_migrate_partij_model(self):

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
