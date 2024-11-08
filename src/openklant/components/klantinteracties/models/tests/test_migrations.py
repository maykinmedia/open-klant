from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models.constants import (
    Klantcontrol,
    SoortPartij,
)
from openklant.tests.utils import TestMigrations


class MigrateDigitaalAdresToBetrokkeneAdres(TestMigrations):
    migrate_from = "0023_betrokkeneadres"
    migrate_to = "0024_migrate_digitaaladres_to_betrokkeneadres"
    app = "klantinteracties"

    def setUpBeforeMigration(self, apps):
        KlantContact = apps.get_model("klantinteracties", "KlantContact")
        Betrokkene = apps.get_model("klantinteracties", "Betrokkene")
        Partij = apps.get_model("klantinteracties", "Partij")
        DigitaalAdres = apps.get_model("klantinteracties", "DigitaalAdres")

        self.klantcontact1 = KlantContact.objects.create(
            nummer="123",
            kanaal="email",
            onderwerp="foo",
            taal="nld",
            vertrouwelijk=False,
        )
        self.klantcontact2 = KlantContact.objects.create(
            nummer="456",
            kanaal="email",
            onderwerp="bar",
            taal="nld",
            vertrouwelijk=True,
        )

        self.partij1 = Partij.objects.create(
            nummer="123",
            soort_partij=SoortPartij.persoon,
            indicatie_actief=True,
        )
        self.partij2 = Partij.objects.create(
            nummer="456",
            soort_partij=SoortPartij.persoon,
            indicatie_actief=True,
        )

        self.betrokkene1 = Betrokkene.objects.create(
            partij=self.partij1,
            klantcontact=self.klantcontact1,
            rol=Klantcontrol.klant,
            initiator=True,
        )
        self.betrokkene2 = Betrokkene.objects.create(
            partij=self.partij2,
            klantcontact=self.klantcontact1,
            rol=Klantcontrol.klant,
            initiator=True,
        )

        DigitaalAdres.objects.create(
            partij=self.partij1,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="foo@bar.nl",
        )
        DigitaalAdres.objects.create(
            partij=self.partij2,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="foo@bar.com",
        )
        DigitaalAdres.objects.create(
            betrokkene=self.betrokkene1,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="bar@baz.nl",
        )
        DigitaalAdres.objects.create(
            betrokkene=self.betrokkene2,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="bar@baz.com",
        )

    def test_autorisatiespecs_created(self):
        DigitaalAdres = self.apps.get_model("klantinteracties", "DigitaalAdres")
        BetrokkeneAdres = self.apps.get_model("klantinteracties", "BetrokkeneAdres")

        digitale_adressen = DigitaalAdres.objects.all()
        betrokkene_adressen = BetrokkeneAdres.objects.all()

        # Two DigitaalAdressen should be removed and replaced with BetrokkeneAdressen
        self.assertEqual(digitale_adressen.count(), 2)
        self.assertEqual(betrokkene_adressen.count(), 2)

        self.assertEqual(digitale_adressen.first().partij.pk, self.partij1.pk)
        self.assertEqual(digitale_adressen.first().betrokkene, None)
        self.assertEqual(digitale_adressen.first().adres, "foo@bar.nl")
        self.assertEqual(digitale_adressen.last().partij.pk, self.partij2.pk)
        self.assertEqual(digitale_adressen.last().betrokkene, None)
        self.assertEqual(digitale_adressen.last().adres, "foo@bar.com")

        self.assertEqual(betrokkene_adressen.first().betrokkene.pk, self.betrokkene1.pk)
        self.assertEqual(betrokkene_adressen.first().adres, "bar@baz.nl")
        self.assertEqual(betrokkene_adressen.last().betrokkene.pk, self.betrokkene2.pk)
        self.assertEqual(betrokkene_adressen.last().adres, "bar@baz.com")


class MigrateBetrokkeneAdresDigitaalAdres(TestMigrations):
    migrate_from = "0024_migrate_digitaaladres_to_betrokkeneadres"
    migrate_to = "0023_betrokkeneadres"
    app = "klantinteracties"

    def setUpBeforeMigration(self, apps):
        KlantContact = apps.get_model("klantinteracties", "KlantContact")
        Betrokkene = apps.get_model("klantinteracties", "Betrokkene")
        Partij = apps.get_model("klantinteracties", "Partij")
        DigitaalAdres = apps.get_model("klantinteracties", "DigitaalAdres")
        BetrokkeneAdres = apps.get_model("klantinteracties", "BetrokkeneAdres")

        self.klantcontact1 = KlantContact.objects.create(
            nummer="123",
            kanaal="email",
            onderwerp="foo",
            taal="nld",
            vertrouwelijk=False,
        )
        self.klantcontact2 = KlantContact.objects.create(
            nummer="456",
            kanaal="email",
            onderwerp="bar",
            taal="nld",
            vertrouwelijk=True,
        )

        self.partij1 = Partij.objects.create(
            nummer="123",
            soort_partij=SoortPartij.persoon,
            indicatie_actief=True,
        )
        self.partij2 = Partij.objects.create(
            nummer="456",
            soort_partij=SoortPartij.persoon,
            indicatie_actief=True,
        )

        self.betrokkene1 = Betrokkene.objects.create(
            partij=self.partij1,
            klantcontact=self.klantcontact1,
            rol=Klantcontrol.klant,
            initiator=True,
        )
        self.betrokkene2 = Betrokkene.objects.create(
            partij=self.partij2,
            klantcontact=self.klantcontact1,
            rol=Klantcontrol.klant,
            initiator=True,
        )

        DigitaalAdres.objects.create(
            partij=self.partij1,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="foo@bar.nl",
        )
        DigitaalAdres.objects.create(
            partij=self.partij2,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="foo@bar.com",
        )
        BetrokkeneAdres.objects.create(
            betrokkene=self.betrokkene1,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="bar@baz.nl",
        )
        BetrokkeneAdres.objects.create(
            betrokkene=self.betrokkene2,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="bar@baz.com",
        )

    def test_autorisatiespecs_created(self):
        DigitaalAdres = self.apps.get_model("klantinteracties", "DigitaalAdres")
        BetrokkeneAdres = self.apps.get_model("klantinteracties", "BetrokkeneAdres")

        digitale_adressen = DigitaalAdres.objects.all()
        betrokkene_adressen = BetrokkeneAdres.objects.all()

        # All BetrokkeneAddressen should be migrated back to DigitaalAdressen
        self.assertEqual(digitale_adressen.count(), 4)
        self.assertEqual(betrokkene_adressen.count(), 0)

        self.assertEqual(digitale_adressen[0].partij.pk, self.partij1.pk)
        self.assertEqual(digitale_adressen[0].betrokkene, None)
        self.assertEqual(digitale_adressen[0].adres, "foo@bar.nl")

        self.assertEqual(digitale_adressen[1].partij.pk, self.partij2.pk)
        self.assertEqual(digitale_adressen[1].betrokkene, None)
        self.assertEqual(digitale_adressen[1].adres, "foo@bar.com")

        self.assertEqual(digitale_adressen[2].partij, None)
        self.assertEqual(digitale_adressen[2].betrokkene.pk, self.betrokkene1.pk)
        self.assertEqual(digitale_adressen[2].adres, "bar@baz.nl")

        self.assertEqual(digitale_adressen[3].partij, None)
        self.assertEqual(digitale_adressen[3].betrokkene.pk, self.betrokkene2.pk)
        self.assertEqual(digitale_adressen[3].adres, "bar@baz.com")
