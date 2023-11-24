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
        list_url = reverse("klantinteracties:partij-list")
        PartijFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_partij(self):
        partij = PartijFactory.create()
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_partij(self):
        vertegenwoordigde = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create()
        digitaal_adres, digitaal_adres2 = DigitaalAdresFactory.create_batch(2)
        partij_identificator = PartijIdentificatorFactory.create()
        list_url = reverse("klantinteracties:partij-list")
        data = {
            "nummer": "1298329191",
            "interneNotitie": "interneNotitie",
            "betrokkenen": [{"uuid": str(betrokkene.uuid)}],
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "vertegenwoordigde": [{"uuid": str(vertegenwoordigde.uuid)}],
            "partijIdentificatoren": [{"uuid": str(partij_identificator.uuid)}],
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

        self.assertEqual(len(data["partijIdentificatoren"]), 1)
        self.assertEqual(len(data["betrokkenen"]), 1)

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["betrokkenen"][0]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["digitaleAdressen"][0]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres.uuid)
        )
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde.uuid)
        )
        self.assertEqual(
            data["partijIdentificatoren"][0]["uuid"], str(partij_identificator.uuid)
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

        with self.subTest("voorkeurs_adres_must_be_given_digitaal_adres_validation"):
            data["voorkeursDigitaalAdres"] = {"uuid": str(digitaal_adres2.uuid)}
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(
                response_data["invalidParams"],
                [
                    {
                        "name": "voorkeursDigitaalAdres",
                        "code": "invalid",
                        "reason": "Het voorkeurs adres moet een gelinkte digitaal adres zijn.",
                    }
                ],
            )

        with self.subTest("create_partij_without_foreignkey_relations"):
            data["betrokkenen"] = []
            data["digitaleAdressen"] = []
            data["voorkeursDigitaalAdres"] = None
            data["vertegenwoordigde"] = []
            data["partijIdentificatoren"] = []

            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            response_data = response.json()

            self.assertEqual(response_data["nummer"], "1298329191")
            self.assertEqual(response_data["interneNotitie"], "interneNotitie")
            self.assertEqual(response_data["betrokkenen"], [])
            self.assertEqual(response_data["digitaleAdressen"], [])
            self.assertIsNone(response_data["voorkeursDigitaalAdres"])
            self.assertEqual(response_data["vertegenwoordigde"], [])
            self.assertEqual(response_data["partijIdentificatoren"], [])
            self.assertEqual(response_data["soortPartij"], "persoon")
            self.assertTrue(response_data["indicatieGeheimhouding"])
            self.assertEqual(response_data["voorkeurstaal"], "ndl")
            self.assertTrue(response_data["indicatieActief"])
            self.assertEqual(
                response_data["bezoekadres"],
                {
                    "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                    "adresregel1": "adres1",
                    "adresregel2": "adres2",
                    "adresregel3": "adres3",
                    "land": "6030",
                },
            )
            self.assertEqual(
                response_data["correspondentieadres"],
                {
                    "nummeraanduidingId": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                    "adresregel1": "adres1",
                    "adresregel2": "adres2",
                    "adresregel3": "adres3",
                    "land": "6030",
                },
            )

    def test_update_partij(self):
        vertegenwoordigde, vertegenwoordigde2 = PartijFactory.create_batch(2)
        betrokkene = BetrokkeneFactory.create()
        partij_identificator = PartijIdentificatorFactory.create()
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
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
        betrokkene2 = BetrokkeneFactory.create(partij=partij)

        digitaal_adres = DigitaalAdresFactory.create(partij=partij)
        digitaal_adres2 = DigitaalAdresFactory.create()
        partij_identificator2 = PartijIdentificatorFactory.create(partij=partij)

        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(len(data["partijIdentificatoren"]), 1)
        self.assertEqual(len(data["betrokkenen"]), 1)

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["betrokkenen"][0]["uuid"], str(betrokkene2.uuid))
        self.assertEqual(
            data["digitaleAdressen"],
            [
                {
                    "uuid": str(digitaal_adres.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/digitaleadressen/{str(digitaal_adres.uuid)}",
                },
            ],
        )
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde.uuid)
        )
        self.assertEqual(
            data["partijIdentificatoren"][0]["uuid"], str(partij_identificator2.uuid)
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
            "betrokkenen": [{"uuid": str(betrokkene.uuid)}],
            "digitaleAdressen": [{"uuid": str(digitaal_adres2.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres2.uuid)},
            "vertegenwoordigde": [{"uuid": str(vertegenwoordigde2.uuid)}],
            "partijIdentificatoren": [{"uuid": str(partij_identificator.uuid)}],
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

        self.assertEqual(len(data["partijIdentificatoren"]), 1)
        self.assertEqual(len(data["betrokkenen"]), 1)

        self.assertEqual(data["nummer"], "6427834668")
        self.assertEqual(data["interneNotitie"], "changed")
        self.assertEqual(data["betrokkenen"][0]["uuid"], str(betrokkene.uuid))
        self.assertEqual(
            data["digitaleAdressen"],
            [
                {
                    "uuid": str(digitaal_adres2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/digitaleadressen/{str(digitaal_adres2.uuid)}",
                },
            ],
        )
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres2.uuid)
        )
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde2.uuid)
        )
        self.assertEqual(
            data["partijIdentificatoren"][0]["uuid"], str(partij_identificator.uuid)
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

        with self.subTest(
            "test_voorkeurs_digitaal_adres_must_be_part_of_digitale_adressen"
        ):
            data["voorkeursDigitaalAdres"] = {"uuid": str(digitaal_adres.uuid)}
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(
                response_data["invalidParams"],
                [
                    {
                        "name": "voorkeursDigitaalAdres",
                        "code": "invalid",
                        "reason": "Het voorkeurs adres moet een gelinkte digitaal adres zijn.",
                    }
                ],
            )

        with self.subTest(
            "test_voorkeurs_adres_can_only_be_given_with_none_empty_digitale_adressen"
        ):
            data["digitaleAdressen"] = []
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(
                response_data["invalidParams"],
                [
                    {
                        "name": "voorkeursDigitaalAdres",
                        "code": "invalid",
                        "reason": "voorkeursDigitaalAdres mag niet meegegeven worden als digitaleAdressen leeg is.",
                    }
                ],
            )

        with self.subTest("set_foreignkey_fields_to_none"):
            data = {
                "nummer": "6427834668",
                "interneNotitie": "changed",
                "betrokkenen": [],
                "digitaleAdressen": [],
                "voorkeursDigitaalAdres": None,
                "vertegenwoordigde": [],
                "partijIdentificatoren": [],
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
            self.assertEqual(data["betrokkenen"], [])
            self.assertEqual(data["digitaleAdressen"], [])
            self.assertIsNone(data["voorkeursDigitaalAdres"])
            self.assertEqual(data["vertegenwoordigde"], [])
            self.assertEqual(data["partijIdentificatoren"], [])
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
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
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
        betrokkene = BetrokkeneFactory.create(partij=partij)
        digitaal_adres = DigitaalAdresFactory.create(partij=partij)
        partij_identificator = PartijIdentificatorFactory.create(partij=partij)

        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(len(data["partijIdentificatoren"]), 1)
        self.assertEqual(len(data["betrokkenen"]), 1)

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["betrokkenen"][0]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["digitaleAdressen"][0]["uuid"], str(digitaal_adres.uuid))
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde.uuid)
        )
        self.assertEqual(
            data["partijIdentificatoren"][0]["uuid"], str(partij_identificator.uuid)
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

        data = {"voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)}}

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(len(data["partijIdentificatoren"]), 1)
        self.assertEqual(len(data["betrokkenen"]), 1)

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["betrokkenen"][0]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["digitaleAdressen"][0]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres.uuid)
        )
        self.assertEqual(
            data["vertegenwoordigde"][0]["uuid"], str(vertegenwoordigde.uuid)
        )
        self.assertEqual(
            data["partijIdentificatoren"][0]["uuid"], str(partij_identificator.uuid)
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
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:partij-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class OrganisatieTests(JWTAuthMixin, APITestCase):
    def test_list_organisatie(self):
        list_url = reverse("klantinteracties:organisatie-list")
        OrganisatieFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_organisatie(self):
        organisatie = OrganisatieFactory.create()
        detail_url = reverse(
            "klantinteracties:organisatie-detail", kwargs={"id": str(organisatie.id)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organisatie(self):
        partij = PartijFactory.create()
        list_url = reverse("klantinteracties:organisatie-list")
        data = {
            "partij": {"uuid": str(partij.uuid)},
            "contactpersoon": [],
            "naam": "whitechapel",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["contactpersoon"], [])
        self.assertEqual(data["naam"], "whitechapel")

        with self.subTest("check_if_partij_unique_validation_works"):
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "partij.uuid")

    def test_create_organisatie_with_contact_personen(self):
        contactpersoon = ContactpersoonFactory.create(organisatie=None)
        partij = PartijFactory.create()

        list_url = reverse("klantinteracties:organisatie-list")
        data = {
            "partij": {"uuid": str(partij.uuid)},
            "contactpersoon": [{"id": contactpersoon.id}],
            "naam": "whitechapel",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["contactpersoon"][0]["id"], contactpersoon.id)
        self.assertEqual(data["naam"], "whitechapel")

        with self.subTest("test_contactpersoon_unique"):
            partij2 = PartijFactory.create()
            data = {
                "partij": {"uuid": str(partij2.uuid)},
                "contactpersoon": [{"id": contactpersoon.id}],
                "naam": "whitechapel",
            }
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "contactpersoon.0.id")

        with self.subTest("test_partij_unique"):
            data = {
                "partij": {"uuid": str(partij.uuid)},
                "contactpersoon": [],
                "naam": "whitechapel",
            }
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "partij.uuid")

    def test_update_organisatie(self):
        partij, partij2 = PartijFactory.create_batch(2)
        contactpersoon = ContactpersoonFactory.create()
        organisatie = OrganisatieFactory.create(partij=partij, naam="whitechapel")
        detail_url = reverse(
            "klantinteracties:organisatie-detail", kwargs={"id": organisatie.id}
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["naam"], "whitechapel")

        data = {
            "partij": {"uuid": str(partij2.uuid)},
            "contactpersoon": [{"id": contactpersoon.id}],
            "naam": "changed",
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij2.uuid))
        self.assertEqual(data["contactpersoon"][0]["id"], contactpersoon.id)
        self.assertEqual(data["naam"], "changed")

        with self.subTest("check_if_changing_contactpersonen_removes_relation"):
            data = {
                "contactpersoon": [],
            }

            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["contactpersoon"], [])

        with self.subTest("check_if_partij_unique_validation_works"):
            OrganisatieFactory.create(partij=partij)
            data = {
                "partij": {"uuid": str(partij.uuid)},
            }

            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "partij.uuid")

    def test_partial_update_organisatie(self):
        partij = PartijFactory.create()
        organisatie = OrganisatieFactory.create(partij=partij, naam="whitechapel")
        detail_url = reverse(
            "klantinteracties:organisatie-detail", kwargs={"id": str(organisatie.id)}
        )

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
        detail_url = reverse(
            "klantinteracties:organisatie-detail", kwargs={"id": str(organisatie.id)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:organisatie-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class PersoonTests(JWTAuthMixin, APITestCase):
    def test_list_persoon(self):
        list_url = reverse("klantinteracties:persoon-list")
        PersoonFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_persoon(self):
        persoon = PersoonFactory.create()
        detail_url = reverse(
            "klantinteracties:persoon-detail", kwargs={"id": str(persoon.id)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_persoon(self):
        partij = PartijFactory.create()
        list_url = reverse("klantinteracties:persoon-list")
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

        with self.subTest("check_if_partij_unique_validation_works"):
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "partij.uuid")

    def test_update_persoon(self):
        partij, partij2 = PartijFactory.create_batch(2)
        persoon = PersoonFactory.create(
            partij=partij,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        detail_url = reverse(
            "klantinteracties:persoon-detail", kwargs={"id": persoon.id}
        )

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

        with self.subTest("check_if_partij_unique_validation_works"):
            persoon2 = PersoonFactory.create()
            new_detail_url = reverse(
                "klantinteracties:persoon-detail", kwargs={"id": persoon2.id}
            )
            response = self.client.put(new_detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "partij.uuid")

    def test_partial_update_persoon(self):
        partij = PartijFactory.create()
        persoon = PersoonFactory.create(
            partij=partij,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        detail_url = reverse(
            "klantinteracties:persoon-detail", kwargs={"id": persoon.id}
        )

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
        detail_url = reverse(
            "klantinteracties:persoon-detail", kwargs={"id": str(persoon.id)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:persoon-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class ContactpersoonTests(JWTAuthMixin, APITestCase):
    def test_list_contact_persoon(self):
        list_url = reverse("klantinteracties:contactpersoon-list")
        ContactpersoonFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_contact_persoon(self):
        contact_persoon = ContactpersoonFactory.create()
        detail_url = reverse(
            "klantinteracties:contactpersoon-detail",
            kwargs={"id": str(contact_persoon.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_contact_persoon(self):
        partij = PartijFactory.create()
        organisatie = OrganisatieFactory.create()
        list_url = reverse("klantinteracties:contactpersoon-list")
        data = {
            "partij": {"uuid": str(partij.uuid)},
            "werkte_voor_organisatie": {"id": str(organisatie.id)},
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
        self.assertEqual(data["werkteVoorOrganisatie"]["id"], organisatie.id)
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        with self.subTest("check_if_partij_unique_validation_works"):
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "partij.uuid")

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
        detail_url = reverse(
            "klantinteracties:contactpersoon-detail", kwargs={"id": contact_persoon.id}
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["werkteVoorOrganisatie"]["id"], organisatie.id)
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
            "werkteVoorOrganisatie": {"id": organisatie2.id},
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
        self.assertEqual(data["werkteVoorOrganisatie"]["id"], organisatie2.id)
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        )

        with self.subTest("check_if_partij_unique_validation_works"):
            contact_persoon2 = ContactpersoonFactory.create()
            new_detail_url = reverse(
                "klantinteracties:contactpersoon-detail",
                kwargs={"id": contact_persoon2.id},
            )
            response = self.client.put(new_detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "partij.uuid")

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
        detail_url = reverse(
            "klantinteracties:contactpersoon-detail", kwargs={"id": contact_persoon.id}
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["werkteVoorOrganisatie"]["id"], organisatie.id)
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
        self.assertEqual(data["werkteVoorOrganisatie"]["id"], organisatie.id)
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
            "klantinteracties:contactpersoon-detail",
            kwargs={"id": str(contact_persoon.id)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:contactpersoon-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class PartijIdentificatorTests(JWTAuthMixin, APITestCase):
    def test_list_partij_indetificator(self):
        list_url = reverse("klantinteracties:partijidentificator-list")
        PartijIdentificatorFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_partij_identificator(self):
        partij_identificator = PartijIdentificatorFactory.create()
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_partij_indetificator(self):
        list_url = reverse("klantinteracties:partijidentificator-list")
        partij = PartijFactory.create()
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
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

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
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
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
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
            "identificeerdePartij": {"uuid": str(partij2.uuid)},
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

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij2.uuid))
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
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
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

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
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
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:partijidentificator-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
