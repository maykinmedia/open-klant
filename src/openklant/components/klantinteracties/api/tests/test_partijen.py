from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    ContactpersoonFactory,
    OrganisatieFactory,
    PartijFactory,
    PartijIdentificatorFactory,
    PersoonFactory,
)


class PartijTests(JWTAuthMixin, APITestCase):
    def test_list_partij(self):
        list_url = reverse("partij-list")
        PartijFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_partij(self):
        partij = PartijFactory.create()
        detail_url = reverse("partij-detail", kwargs={"uuid": str(partij.uuid)})

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_partij(self):
        vertegenwoordigde = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create()
        digitaal_adres, digitaal_adres2 = DigitaalAdresFactory.create_batch(2)
        list_url = reverse("partij-list")
        data = {
            "nummer": "1298329191",
            "interneNotitie": "interneNotitie",
            "betrokkene": {"uuid": str(betrokkene.uuid)},
            "digitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres2.uuid)},
            "vertegenwoordigde": [{"uuid": str(vertegenwoordigde.uuid)}],
            "soortPartij": "persoon",
            "indicatieGeheimhouding": True,
            "voorkeurstaal": "ndl",
            "indicatieActief": True,
            "bezoekadres": {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres2.uuid)
        )
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde.uuid)
        )
        self.assertEqual(data["soortPartij"], "persoon")
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )

    def test_update_parij(self):
        vertegenwoordigde, vertegenwoordigde2 = PartijFactory.create_batch(2)
        betrokkene, betrokkene2 = BetrokkeneFactory.create_batch(2)
        (
            digitaal_adres,
            digitaal_adres2,
            digitaal_adres3,
        ) = DigitaalAdresFactory.create_batch(3)
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            betrokkene=betrokkene,
            digitaal_adres=digitaal_adres,
            voorkeurs_digitaal_adres=digitaal_adres2,
            vertegenwoordigde=[vertegenwoordigde],
            soort_partij="persoon",
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="6030",
            correspondentieadres_nummeraanduiding_id="095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="6030",
        )

        detail_url = reverse("partij-detail", kwargs={"uuid": str(partij.uuid)})
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres2.uuid)
        )
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde.uuid)
        )
        self.assertEqual(data["soortPartij"], "persoon")
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )

        data = {
            "nummer": "6427834668",
            "interneNotitie": "changed",
            "betrokkene": {"uuid": str(betrokkene2.uuid)},
            "digitaalAdres": {"uuid": str(digitaal_adres2.uuid)},
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres3.uuid)},
            "vertegenwoordigde": [{"uuid": str(vertegenwoordigde2.uuid)}],
            "soortPartij": "organisatie",
            "indicatieGeheimhouding": False,
            "voorkeurstaal": "ger",
            "indicatieActief": False,
            "bezoekadres": {
                "nummeraanduidingId": "f78sd8f-uh45-34km-2o3n-aasdasdasc9g",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "sd76f7sd-j4nr-a9s8-83ec-sad89f79a7sd",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["nummer"], "6427834668")
        self.assertEqual(data["interneNotitie"], "changed")
        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene2.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres2.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres3.uuid)
        )
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde2.uuid)
        )
        self.assertEqual(data["soortPartij"], "organisatie")
        self.assertFalse(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ger")
        self.assertFalse(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "f78sd8f-uh45-34km-2o3n-aasdasdasc9g",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "sd76f7sd-j4nr-a9s8-83ec-sad89f79a7sd",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
        )

    def test_partial_update_parij(self):
        vertegenwoordigde = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create()
        (
            digitaal_adres,
            digitaal_adres2,
        ) = DigitaalAdresFactory.create_batch(2)
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            betrokkene=betrokkene,
            digitaal_adres=digitaal_adres,
            voorkeurs_digitaal_adres=digitaal_adres2,
            vertegenwoordigde=[vertegenwoordigde],
            soort_partij="persoon",
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="6030",
            correspondentieadres_nummeraanduiding_id="095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="6030",
        )

        detail_url = reverse("partij-detail", kwargs={"uuid": str(partij.uuid)})
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres2.uuid)
        )
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde.uuid)
        )
        self.assertEqual(data["soortPartij"], "persoon")
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )

        data = {
            "nummer": "6427834668",
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["nummer"], "6427834668")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres2.uuid)
        )
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde.uuid)
        )
        self.assertEqual(data["soortPartij"], "persoon")
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )

    def test_destroy_partij(self):
        partij = PartijFactory.create()
        detail_url = reverse("partij-detail", kwargs={"uuid": str(partij.uuid)})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("partij-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class OrganisatieTests(JWTAuthMixin, APITestCase):
    def test_list_organisatie(self):
        list_url = reverse("organisatie-list")
        OrganisatieFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_organisatie(self):
        organisatie = OrganisatieFactory.create()
        detail_url = reverse("organisatie-detail", kwargs={"id": str(organisatie.id)})

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organisatie(self):
        partij = PartijFactory.create()
        list_url = reverse("organisatie-list")
        data = {
            "partij": {"uuid": str(partij.uuid)},
            "naam": "whitechapel",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["naam"], "whitechapel")

        # TODO: write subtest test to test if partij's unique is true validation works propperly

    def test_update_organisatie(self):
        partij, partij2 = PartijFactory.create_batch(2)
        organisatie = OrganisatieFactory.create(partij=partij, naam="whitechapel")
        detail_url = reverse("organisatie-detail", kwargs={"id": organisatie.id})

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["naam"], "whitechapel")

        data = {
            "partij": {"uuid": str(partij2.uuid)},
            "naam": "changed",
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij2.uuid))
        self.assertEqual(data["naam"], "changed")

        # TODO: write subtest test to test if partij's unique is true validation works propperly

    def test_partial_update_organisatie(self):
        partij = PartijFactory.create()
        organisatie = OrganisatieFactory.create(partij=partij, naam="whitechapel")
        detail_url = reverse("organisatie-detail", kwargs={"id": str(organisatie.id)})

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["naam"], "whitechapel")

        data = {
            "naam": "changed",
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["naam"], "changed")

    def test_destroy_organisatie(self):
        organisatie = OrganisatieFactory.create()
        detail_url = reverse("organisatie-detail", kwargs={"id": str(organisatie.id)})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("organisatie-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class PersoonTests(JWTAuthMixin, APITestCase):
    def test_list_persoon(self):
        list_url = reverse("persoon-list")
        PersoonFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_persoon(self):
        persoon = PersoonFactory.create()
        detail_url = reverse("persoon-detail", kwargs={"id": str(persoon.id)})

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_persoon(self):
        partij = PartijFactory.create()
        list_url = reverse("persoon-list")
        data = {
            "partij": {"uuid": str(partij.uuid)},
            "contactnaam": {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        # TODO: write subtest test to test if partij's unique is true validation works propperly

    def test_update_persoon(self):
        partij, partij2 = PartijFactory.create_batch(2)
        persoon = PersoonFactory.create(
            partij=partij,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        detail_url = reverse("persoon-detail", kwargs={"id": persoon.id})

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        data = {
            "partij": {"uuid": str(partij2.uuid)},
            "contactnaam": {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij2.uuid))
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        )

        # TODO: write subtest test to test if partij's unique is true validation works propperly

    def test_partial_update_persoon(self):
        partij = PartijFactory.create()
        persoon = PersoonFactory.create(
            partij=partij,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        detail_url = reverse("persoon-detail", kwargs={"id": persoon.id})

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        data = {
            "contactnaam": {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        )

    def test_destroy_persoon(self):
        persoon = PersoonFactory.create()
        detail_url = reverse("persoon-detail", kwargs={"id": str(persoon.id)})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("persoon-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class ContactpersoonTests(JWTAuthMixin, APITestCase):
    def test_list_contact_persoon(self):
        list_url = reverse("contactpersoon-list")
        ContactpersoonFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_contact_persoon(self):
        contact_persoon = ContactpersoonFactory.create()
        detail_url = reverse(
            "contactpersoon-detail", kwargs={"id": str(contact_persoon.id)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_contact_persoon(self):
        partij = PartijFactory.create()
        organisatie = OrganisatieFactory.create()
        list_url = reverse("contactpersoon-list")
        data = {
            "partij": {"uuid": str(partij.uuid)},
            "organisatie": {"id": str(organisatie.id)},
            "contactnaam": {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["organisatie"]["id"], organisatie.id)
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        # TODO: write subtest test to test if partij's unique is true validation works propperly

    def test_update_contact_persoon(self):
        partij, partij2 = PartijFactory.create_batch(2)
        organisatie, organisatie2 = OrganisatieFactory.create_batch(2)
        contact_persoon = ContactpersoonFactory.create(
            partij=partij,
            organisatie=organisatie,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        detail_url = reverse("contactpersoon-detail", kwargs={"id": contact_persoon.id})

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["organisatie"]["id"], organisatie.id)
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        data = {
            "partij": {"uuid": str(partij2.uuid)},
            "organisatie": {"id": organisatie2.id},
            "contactnaam": {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij2.uuid))
        self.assertEqual(data["organisatie"]["id"], organisatie2.id)
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        )

        # TODO: write subtest test to test if partij's unique is true validation works propperly

    def test_partial_update_contact_persoon(self):
        partij = PartijFactory.create()
        organisatie = OrganisatieFactory.create()
        contact_persoon = ContactpersoonFactory.create(
            partij=partij,
            organisatie=organisatie,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        detail_url = reverse("contactpersoon-detail", kwargs={"id": contact_persoon.id})

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["organisatie"]["id"], organisatie.id)
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        data = {
            "contactnaam": {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["organisatie"]["id"], organisatie.id)
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        )

    def test_destroy_contact_persoon(self):
        contact_persoon = ContactpersoonFactory.create()
        detail_url = reverse(
            "contactpersoon-detail", kwargs={"id": str(contact_persoon.id)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("contactpersoon-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class PartijIdentificatorTests(JWTAuthMixin, APITestCase):
    def test_list_partij_indetificator(self):
        list_url = reverse("partijidentificator-list")
        PartijIdentificatorFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_partij_identificator(self):
        partij_identificator = PartijIdentificatorFactory.create()
        detail_url = reverse(
            "partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_partij_indetificator(self):
        list_url = reverse("partijidentificator-list")
        partij = PartijFactory.create()
        data = {
            "partij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "anderePartijIdentificator")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

    def test_update_partij_indetificator(self):
        partij, partij2 = PartijFactory.create_batch(2)
        partij_identificator = PartijIdentificatorFactory.create(
            partij=partij,
            andere_partij_identificator="anderePartijIdentificator",
            partij_identificator_objecttype="objecttype",
            partij_identificator_soort_object_id="soortObjectId",
            partij_identificator_object_id="objectId",
            partij_identificator_register="register",
        )

        detail_url = reverse(
            "partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "anderePartijIdentificator")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

        data = {
            "partij": {"uuid": str(partij2.uuid)},
            "anderePartijIdentificator": "changed",
            "partijIdentificator": {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij2.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "changed")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        )

    def test_partial_update_partij_indetificator(self):
        partij = PartijFactory.create()
        partij_identificator = PartijIdentificatorFactory.create(
            partij=partij,
            andere_partij_identificator="anderePartijIdentificator",
            partij_identificator_objecttype="objecttype",
            partij_identificator_soort_object_id="soortObjectId",
            partij_identificator_object_id="objectId",
            partij_identificator_register="register",
        )

        detail_url = reverse(
            "partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "anderePartijIdentificator")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

        data = {
            "anderePartijIdentificator": "changed",
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "changed")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

    def test_destroy_partij_identificator(self):
        partij_identificator = PartijIdentificatorFactory.create()
        detail_url = reverse(
            "partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("partijidentificator-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
