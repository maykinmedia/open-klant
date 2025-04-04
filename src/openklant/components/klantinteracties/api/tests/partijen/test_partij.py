from django.utils.translation import gettext as _

from rest_framework import status
from vng_api_common.tests import get_validation_errors, reverse, reverse_lazy

from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.klantinteracties.models.partijen import (
    Partij,
    PartijIdentificator,
)
from openklant.components.klantinteracties.models.tests.factories import (
    BsnPartijIdentificatorFactory,
    CategorieFactory,
    CategorieRelatieFactory,
    ContactpersoonFactory,
    DigitaalAdresFactory,
    KvkNummerPartijIdentificatorFactory,
    OrganisatieFactory,
    PartijFactory,
    PersoonFactory,
    RekeningnummerFactory,
    VertegenwoordigdenFactory,
    VestigingsnummerPartijIdentificatorFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class PartijTests(APITestCase):
    def test_list_partij(self):
        list_url = reverse("klantinteracties:partij-list")
        partij, partij2 = PartijFactory.create_batch(2)
        VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij, vertegenwoordigde_partij=partij2
        )

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

        with self.subTest("test_vertegenwoordigden"):
            # test if parij2 doesn't vertegenwoordigd anything
            self.assertEqual(data["results"][0]["nummer"], str(partij2.nummer))
            self.assertEqual(data["results"][0]["vertegenwoordigden"], [])

            # test if parij vertegenwoordigd partij2
            self.assertEqual(data["results"][1]["nummer"], str(partij.nummer))
            self.assertEqual(
                data["results"][1]["vertegenwoordigden"],
                [
                    {
                        "uuid": str(partij2.uuid),
                        "url": f"http://testserver/klantinteracties/api/v1/partijen/{str(partij2.uuid)}",
                    }
                ],
            )

    def test_list_pagination_pagesize_param(self):
        list_url = reverse("klantinteracties:partij-list")
        PartijFactory.create_batch(10)

        response = self.client.get(list_url, {"pageSize": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 10)
        self.assertEqual(len(data["results"]), 5)
        self.assertEqual(data["next"], f"http://testserver{list_url}?page=2&pageSize=5")

    def test_read_partij(self):
        partij = PartijFactory.create()
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

        with self.subTest("test_categorie_relatie_with_categorie_names"):
            categorie = CategorieFactory.create(naam="test-categorie-naam")
            CategorieRelatieFactory.create(partij=partij, categorie=categorie)

            response = self.client.get(detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()

            self.assertEqual(
                data["categorieRelaties"][0]["categorieNaam"], "test-categorie-naam"
            )

    def test_create_partij_with_adressen_huisnummer_set_to_none(self):
        digitaal_adres, digitaal_adres2 = DigitaalAdresFactory.create_batch(2)
        rekeningnummer, rekeningnummer2 = RekeningnummerFactory.create_batch(2)
        list_url = reverse("klantinteracties:partij-list")
        data = {
            "nummer": "1298329191",
            "interneNotitie": "interneNotitie",
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": "persoon",
            "voorkeurstaal": "ndl",
            "indicatieActief": True,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": None,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": None,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "partijIdentificatie": {
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                }
            },
        }
        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIsNone(data["bezoekadres"]["huisnummer"])
        self.assertIsNone(data["correspondentieadres"]["huisnummer"])

    def test_create_partij(self):
        digitaal_adres, digitaal_adres2 = DigitaalAdresFactory.create_batch(2)
        rekeningnummer, rekeningnummer2 = RekeningnummerFactory.create_batch(2)
        list_url = reverse("klantinteracties:partij-list")
        data = {
            "nummer": "1298329191",
            "interneNotitie": "interneNotitie",
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.persoon.value,
            "voorkeurstaal": "ndl",
            "indicatieActief": True,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "partijIdentificatie": {
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                }
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["digitaleAdressen"][0]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres.uuid)
        )
        self.assertEqual(data["rekeningnummers"][0]["uuid"], str(rekeningnummer.uuid))
        self.assertEqual(
            data["voorkeursRekeningnummer"]["uuid"], str(rekeningnummer.uuid)
        )
        self.assertEqual(data["soortPartij"], SoortPartij.persoon.value)
        self.assertIsNone(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"],
            {
                "volledigeNaam": "Phil Bozeman",
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                },
            },
        )

        with self.subTest("create_partij_without_foreignkey_relations"):
            data["nummer"] = "1298329192"
            data["digitaleAdressen"] = []
            data["voorkeursDigitaalAdres"] = None
            data["rekeningnummers"] = []
            data["voorkeursRekeningnummer"] = None

            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            response_data = response.json()

            self.assertEqual(response_data["nummer"], "1298329192")
            self.assertEqual(response_data["interneNotitie"], "interneNotitie")
            self.assertEqual(response_data["digitaleAdressen"], [])
            self.assertIsNone(response_data["voorkeursDigitaalAdres"])
            self.assertEqual(response_data["rekeningnummers"], [])
            self.assertIsNone(response_data["voorkeursRekeningnummer"])
            self.assertEqual(response_data["soortPartij"], SoortPartij.persoon.value)
            self.assertIsNone(data["indicatieGeheimhouding"])
            self.assertEqual(response_data["voorkeurstaal"], "ndl")
            self.assertTrue(response_data["indicatieActief"])
            self.assertEqual(
                response_data["bezoekadres"],
                {
                    "nummeraanduidingId": "1234567890000001",
                    "straatnaam": "straat",
                    "huisnummer": 10,
                    "huisnummertoevoeging": "A2",
                    "postcode": "1008 DG",
                    "stad": "Amsterdam",
                    "adresregel1": "adres1",
                    "adresregel2": "adres2",
                    "adresregel3": "adres3",
                    "land": "NL",
                },
            )
            self.assertEqual(
                response_data["correspondentieadres"],
                {
                    "nummeraanduidingId": "1234567890000001",
                    "straatnaam": "straat",
                    "huisnummer": 10,
                    "huisnummertoevoeging": "A2",
                    "postcode": "1008 DG",
                    "stad": "Amsterdam",
                    "adresregel1": "adres1",
                    "adresregel2": "adres2",
                    "adresregel3": "adres3",
                    "land": "NL",
                },
            )
            self.assertEqual(
                data["partijIdentificatie"],
                {
                    "volledigeNaam": "Phil Bozeman",
                    "contactnaam": {
                        "voorletters": "P",
                        "voornaam": "Phil",
                        "voorvoegselAchternaam": "",
                        "achternaam": "Bozeman",
                    },
                },
            )

        with self.subTest("auto_generate_max_nummer_plus_one"):
            data["nummer"] = ""
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = response.json()
            self.assertEqual(response_data["nummer"], "1298329193")

        with self.subTest("auto_generate_nummer_unique_validation"):
            data["nummer"] = "1298329193"
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "nummer")
            self.assertEqual(error["code"], "unique")
            self.assertEqual(
                error["reason"], "Er bestaat al een partij met eenzelfde nummer."
            )

        with self.subTest("auto_generate_nummer_over_10_characters_error_message"):
            PartijFactory.create(nummer="9999999999")
            data["nummer"] = ""
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
            response_data = response.json()
            self.assertEqual(
                response_data["detail"],
                "Er kon niet automatisch een opvolgend nummer worden gegenereerd. "
                "Het maximaal aantal tekens is bereikt.",
            )

        with self.subTest("voorkeurs_adres_must_be_given_digitaal_adres_validation"):
            data["nummer"] = "1298329194"
            data["voorkeursDigitaalAdres"] = {"uuid": str(digitaal_adres2.uuid)}
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "voorkeursDigitaalAdres")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "Het voorkeurs adres moet een gelinkte digitaal adres zijn.",
            )

        with self.subTest("voorkeurs_adres_must_be_given_digitaal_adres_validation"):
            data["nummer"] = "1298329194"
            # change voorkeursDigitaalAdres because of previous subtest
            data["voorkeursDigitaalAdres"] = None

            data["voorkeursRekeningnummer"] = {"uuid": str(rekeningnummer2.uuid)}
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "voorkeursRekeningnummer")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "Het voorkeurs rekeningnummer moet een gelinkte rekeningnummer zijn.",
            )

    def test_create_partij_only_required(self):
        """
        Test if object is created with only required parameters

        Regression Test for #227
        """
        list_url = reverse("klantinteracties:partij-list")

        response = self.client.post(list_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(response_data["title"], "Invalid input.")
        self.assertEqual(response_data["code"], "invalid")
        self.assertEqual(response_data["status"], 400)
        self.assertEqual(
            response_data["invalidParams"],
            [
                {
                    "name": "soortPartij",
                    "code": "required",
                    "reason": _("This field is required."),
                },
                {
                    "name": "indicatieActief",
                    "code": "required",
                    "reason": _("This field is required."),
                },
            ],
        )

        digitaal_adres = DigitaalAdresFactory()

        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "soortPartij": SoortPartij.organisatie.value,
            "indicatieActief": True,
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_persoon(self):
        list_url = reverse("klantinteracties:partij-list")
        data = {
            "nummer": "1298329191",
            "interneNotitie": "interneNotitie",
            "digitaleAdressen": [],
            "voorkeursDigitaalAdres": None,
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "indicatieGeheimhouding": True,
            "voorkeurstaal": "ndl",
            "indicatieActief": True,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "soortPartij": SoortPartij.persoon.value,
            "partijIdentificatie": {
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                }
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["nummer"], "1298329191")
        self.assertEqual(response_data["interneNotitie"], "interneNotitie")
        self.assertEqual(response_data["digitaleAdressen"], [])
        self.assertIsNone(response_data["voorkeursDigitaalAdres"])
        self.assertEqual(response_data["rekeningnummers"], [])
        self.assertIsNone(response_data["voorkeursRekeningnummer"])
        self.assertEqual(response_data["soortPartij"], SoortPartij.persoon.value)
        self.assertTrue(response_data["indicatieGeheimhouding"])
        self.assertEqual(response_data["voorkeurstaal"], "ndl")
        self.assertTrue(response_data["indicatieActief"])
        self.assertEqual(
            response_data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            response_data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            response_data["partijIdentificatie"],
            {
                "volledigeNaam": "Phil Bozeman",
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                },
            },
        )

    def test_create_organisatie(self):
        contactpersoon = ContactpersoonFactory.create(
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        list_url = reverse("klantinteracties:partij-list")
        data = {
            "nummer": "1298329191",
            "interneNotitie": "interneNotitie",
            "digitaleAdressen": [],
            "voorkeursDigitaalAdres": None,
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "indicatieGeheimhouding": True,
            "voorkeurstaal": "ndl",
            "indicatieActief": True,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {
                "naam": "Whitechapel",
                "contactpersonen": [{"id": contactpersoon.id}],
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["nummer"], "1298329191")
        self.assertEqual(response_data["interneNotitie"], "interneNotitie")
        self.assertEqual(response_data["digitaleAdressen"], [])
        self.assertIsNone(response_data["voorkeursDigitaalAdres"])
        self.assertEqual(response_data["rekeningnummers"], [])
        self.assertIsNone(response_data["voorkeursRekeningnummer"])
        self.assertEqual(response_data["soortPartij"], SoortPartij.organisatie.value)
        self.assertTrue(response_data["indicatieGeheimhouding"])
        self.assertEqual(response_data["voorkeurstaal"], "ndl")
        self.assertTrue(response_data["indicatieActief"])
        self.assertEqual(
            response_data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            response_data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            response_data["partijIdentificatie"],
            {"naam": "Whitechapel"},
        )

    def test_create_contactpersoon(self):
        organisatie = PartijFactory.create(soort_partij=SoortPartij.organisatie.value)
        list_url = reverse("klantinteracties:partij-list")
        data = {
            "nummer": "1298329191",
            "interneNotitie": "interneNotitie",
            "digitaleAdressen": [],
            "voorkeursDigitaalAdres": None,
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "indicatieGeheimhouding": True,
            "voorkeurstaal": "ndl",
            "indicatieActief": True,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "soortPartij": SoortPartij.contactpersoon.value,
            "partijIdentificatie": {
                "werkteVoorPartij": {
                    "uuid": organisatie.uuid,
                },
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["nummer"], "1298329191")
        self.assertEqual(response_data["interneNotitie"], "interneNotitie")
        self.assertEqual(response_data["digitaleAdressen"], [])
        self.assertIsNone(response_data["voorkeursDigitaalAdres"])
        self.assertEqual(response_data["rekeningnummers"], [])
        self.assertIsNone(response_data["voorkeursRekeningnummer"])
        self.assertEqual(response_data["soortPartij"], SoortPartij.contactpersoon.value)
        self.assertTrue(response_data["indicatieGeheimhouding"])
        self.assertEqual(response_data["voorkeurstaal"], "ndl")
        self.assertTrue(response_data["indicatieActief"])
        self.assertEqual(
            response_data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            response_data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            response_data["partijIdentificatie"]["werkteVoorPartij"],
            {
                "uuid": str(organisatie.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/partijen/{str(organisatie.uuid)}",
            },
        )
        self.assertEqual(
            response_data["partijIdentificatie"]["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

    def test_update_partij(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.persoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            bezoekadres_straatnaam="straat",
            bezoekadres_huisnummer=10,
            bezoekadres_huisnummertoevoeging="A2",
            bezoekadres_postcode="1008 DG",
            bezoekadres_stad="Amsterdam",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="NL",
            correspondentieadres_nummeraanduiding_id="1234567890000001",
            correspondentieadres_straatnaam="straat",
            correspondentieadres_huisnummer=10,
            correspondentieadres_huisnummertoevoeging="A2",
            correspondentieadres_postcode="1008 DG",
            correspondentieadres_stad="Amsterdam",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="NL",
        )
        PersoonFactory.create(
            partij=partij,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )

        digitaal_adres = DigitaalAdresFactory.create(partij=partij)
        digitaal_adres2 = DigitaalAdresFactory.create()

        rekeningnummer = RekeningnummerFactory.create(partij=partij)
        rekeningnummer2 = RekeningnummerFactory.create()

        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(
            data["digitaleAdressen"],
            [
                {
                    "uuid": str(digitaal_adres.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/digitaleadressen/{str(digitaal_adres.uuid)}",
                },
            ],
        )
        self.assertEqual(
            data["rekeningnummers"],
            [
                {
                    "uuid": str(rekeningnummer.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/rekeningnummers/{str(rekeningnummer.uuid)}",
                },
            ],
        )
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.persoon.value)
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"],
            {
                "volledigeNaam": "Phil Bozeman",
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                },
            },
        )

        data = {
            "nummer": "6427834668",
            "interneNotitie": "changed",
            "digitaleAdressen": [{"uuid": str(digitaal_adres2.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres2.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer2.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer2.uuid)},
            "soortPartij": SoortPartij.persoon.value,
            "indicatieGeheimhouding": None,
            "voorkeurstaal": "ger",
            "indicatieActief": False,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "partijIdentificatie": {
                "contactnaam": {
                    "voorletters": "V",
                    "voornaam": "Vincent",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bennette",
                }
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["nummer"], "6427834668")
        self.assertEqual(data["interneNotitie"], "changed")
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
            data["rekeningnummers"],
            [
                {
                    "uuid": str(rekeningnummer2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/rekeningnummers/{str(rekeningnummer2.uuid)}",
                },
            ],
        )
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres2.uuid)
        )
        self.assertEqual(
            data["voorkeursRekeningnummer"]["uuid"], str(rekeningnummer2.uuid)
        )
        self.assertEqual(data["soortPartij"], SoortPartij.persoon.value)
        self.assertIsNone(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ger")
        self.assertFalse(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"],
            {
                "volledigeNaam": "Vincent Bennette",
                "contactnaam": {
                    "voorletters": "V",
                    "voornaam": "Vincent",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bennette",
                },
            },
        )

        with self.subTest(
            "test_voorkeurs_digitaal_adres_must_be_part_of_digitale_adressen"
        ):
            data["voorkeursDigitaalAdres"] = {"uuid": str(digitaal_adres.uuid)}
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "voorkeursDigitaalAdres")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "Het voorkeurs adres moet een gelinkte digitaal adres zijn.",
            )

        with self.subTest(
            "test_voorkeurs_adres_can_only_be_given_with_none_empty_digitale_adressen"
        ):
            data["digitaleAdressen"] = []
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "voorkeursDigitaalAdres")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "voorkeursDigitaalAdres mag niet meegegeven worden als digitaleAdressen leeg is.",
            )
        with self.subTest(
            "test_voorkeurs_rekeningnummer_must_be_part_of_rekeningnummers"
        ):
            # set voorkeursDigitaalAdres to null because of previous subtests
            data["voorkeursDigitaalAdres"] = None

            data["voorkeursRekeningnummer"] = {"uuid": str(rekeningnummer.uuid)}
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "voorkeursRekeningnummer")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "Het voorkeurs rekeningnummer moet een gelinkte rekeningnummer zijn.",
            )

        with self.subTest(
            "test_rekeningnummer_can_only_be_given_with_none_empty_rekeningnummer"
        ):
            data["rekeningnummers"] = []
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "voorkeursRekeningnummer")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "voorkeursRekeningnummer mag niet meegegeven worden als rekeningnummers leeg is.",
            )
        with self.subTest("set_foreignkey_fields_to_none"):
            data = {
                "nummer": "6427834668",
                "interneNotitie": "changed",
                "digitaleAdressen": [],
                "voorkeursDigitaalAdres": None,
                "rekeningnummers": [],
                "voorkeursRekeningnummer": None,
                "soortPartij": SoortPartij.organisatie.value,
                "partijIdentificatie": {"naam": "string"},
                "indicatieGeheimhouding": False,
                "voorkeurstaal": "ger",
                "indicatieActief": False,
                "bezoekadres": {
                    "nummeraanduidingId": "1234567890000002",
                    "straatnaam": "changed",
                    "huisnummer": 10,
                    "huisnummertoevoeging": "changed",
                    "postcode": "1001 AB",
                    "stad": "Amsterdam",
                    "adresregel1": "changed",
                    "adresregel2": "changed",
                    "adresregel3": "changed",
                    "land": "NL",
                },
                "correspondentieadres": {
                    "nummeraanduidingId": "1234567890000003",
                    "straatnaam": "changed",
                    "huisnummer": 10,
                    "huisnummertoevoeging": "changed",
                    "postcode": "1001 AB",
                    "stad": "Amsterdam",
                    "adresregel1": "changed",
                    "adresregel2": "changed",
                    "adresregel3": "changed",
                    "land": "NL",
                },
            }
            # assert initial state for some fields
            self.assertEqual(partij.digitaaladres_set.first(), digitaal_adres2)
            self.assertEqual(partij.rekeningnummer_set.first(), rekeningnummer2)

            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()

            # the relation should be unlinked from the Partij
            self.assertFalse(partij.digitaaladres_set.exists())
            self.assertFalse(partij.rekeningnummer_set.exists())

            self.assertEqual(data["nummer"], "6427834668")
            self.assertEqual(data["interneNotitie"], "changed")
            self.assertEqual(data["digitaleAdressen"], [])
            self.assertIsNone(data["voorkeursDigitaalAdres"])
            self.assertEqual(data["rekeningnummers"], [])
            self.assertIsNone(data["voorkeursRekeningnummer"])
            self.assertEqual(data["soortPartij"], SoortPartij.organisatie.value)
            self.assertFalse(data["indicatieGeheimhouding"])
            self.assertEqual(data["voorkeurstaal"], "ger")
            self.assertFalse(data["indicatieActief"])
            self.assertEqual(
                data["bezoekadres"],
                {
                    "nummeraanduidingId": "1234567890000002",
                    "straatnaam": "changed",
                    "huisnummer": 10,
                    "huisnummertoevoeging": "changed",
                    "postcode": "1001 AB",
                    "stad": "Amsterdam",
                    "adresregel1": "changed",
                    "adresregel2": "changed",
                    "adresregel3": "changed",
                    "land": "NL",
                },
            )
            self.assertEqual(
                data["correspondentieadres"],
                {
                    "nummeraanduidingId": "1234567890000003",
                    "straatnaam": "changed",
                    "huisnummer": 10,
                    "huisnummertoevoeging": "changed",
                    "postcode": "1001 AB",
                    "stad": "Amsterdam",
                    "adresregel1": "changed",
                    "adresregel2": "changed",
                    "adresregel3": "changed",
                    "land": "NL",
                },
            )

    def test_update_partij_only_required(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            soort_partij=SoortPartij.persoon.value,
        )

        data = {}
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertEqual(response_data["title"], "Invalid input.")
        self.assertEqual(response_data["code"], "invalid")
        self.assertEqual(response_data["status"], 400)
        self.assertEqual(
            response_data["invalidParams"],
            [
                {
                    "name": "soortPartij",
                    "code": "required",
                    "reason": _("This field is required."),
                },
                {
                    "name": "indicatieActief",
                    "code": "required",
                    "reason": _("This field is required."),
                },
            ],
        )

        digitaal_adres = DigitaalAdresFactory()

        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["nummer"], "1298329191")
        self.assertEqual(response_data["soortPartij"], SoortPartij.organisatie.value)
        self.assertEqual(
            response_data["digitaleAdressen"][0]["uuid"], str(digitaal_adres.uuid)
        )
        self.assertEqual(
            response_data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres.uuid)
        )
        self.assertEqual(response_data["rekeningnummers"], [])
        self.assertIsNone(response_data["voorkeursRekeningnummer"])

    def test_update_partij_fk_fields(self):
        partij = PartijFactory.create()
        digitaal_adres = DigitaalAdresFactory.create(partij=partij)
        rekeningnummer = RekeningnummerFactory.create(partij=partij)

        # initial state relation
        self.assertTrue(partij.digitaaladres_set.exists())
        self.assertTrue(partij.rekeningnummer_set.exists())

        detail_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": partij.uuid},
        )

        with self.subTest("set_fk_none"):
            data = {
                "rekeningnummers": None,
                "digitaleAdressen": None,
            }
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            partij = Partij.objects.get(uuid=partij.uuid)
            self.assertEqual(response_data["rekeningnummers"], [])
            self.assertEqual(response_data["digitaleAdressen"], [])

            # the relation should be unlinked from the Partij
            self.assertFalse(partij.digitaaladres_set.exists())
            self.assertFalse(partij.rekeningnummer_set.exists())

        digitaal_adres.partij = partij
        digitaal_adres.save()
        rekeningnummer.partij = partij
        rekeningnummer.save()
        # initial state relation
        self.assertTrue(partij.digitaaladres_set.exists())
        self.assertTrue(partij.rekeningnummer_set.exists())
        with self.subTest("set_fk_empty_list"):
            data = {
                "rekeningnummers": [],
                "digitaleAdressen": [],
            }
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            partij = Partij.objects.get(uuid=partij.uuid)
            self.assertEqual(response_data["rekeningnummers"], [])
            self.assertEqual(response_data["digitaleAdressen"], [])

            # the relation should be unlinked from the Partij
            self.assertFalse(partij.digitaaladres_set.exists())
            self.assertFalse(partij.rekeningnummer_set.exists())

    def test_update_partially_partij_only_required(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            soort_partij=SoortPartij.persoon.value,
        )

        data = {}
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["nummer"], "1298329191")
        self.assertEqual(response_data["interneNotitie"], "interneNotitie")
        self.assertEqual(response_data["voorkeursDigitaalAdres"], None)
        self.assertEqual(response_data["voorkeursRekeningnummer"], None)
        self.assertEqual(response_data["voorkeurstaal"], "ndl")
        self.assertEqual(response_data["indicatieGeheimhouding"], True)
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["soortPartij"], SoortPartij.persoon.value)

    def test_update_partij_persoon(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.persoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            bezoekadres_straatnaam="straat",
            bezoekadres_huisnummer=10,
            bezoekadres_huisnummertoevoeging="A2",
            bezoekadres_postcode="1008 DG",
            bezoekadres_stad="Amsterdam",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="NL",
            correspondentieadres_nummeraanduiding_id="1234567890000001",
            correspondentieadres_straatnaam="straat",
            correspondentieadres_huisnummer=10,
            correspondentieadres_huisnummertoevoeging="A2",
            correspondentieadres_postcode="1008 DG",
            correspondentieadres_stad="Amsterdam",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="NL",
        )
        PersoonFactory.create(
            partij=partij,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["digitaleAdressen"], [])
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"], [])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.persoon.value)
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"],
            {
                "volledigeNaam": "Phil Bozeman",
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                },
            },
        )

        data = {
            "nummer": "6427834668",
            "interneNotitie": "changed",
            "digitaleAdressen": [],
            "voorkeursDigitaalAdres": None,
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "soortPartij": SoortPartij.persoon.value,
            "indicatieGeheimhouding": False,
            "voorkeurstaal": "ger",
            "indicatieActief": False,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "partijIdentificatie": {
                "contactnaam": {
                    "voorletters": "V",
                    "voornaam": "Vincent",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bennett",
                }
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["nummer"], "6427834668")
        self.assertEqual(data["interneNotitie"], "changed")
        self.assertEqual(data["digitaleAdressen"], [])
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"], [])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.persoon.value)
        self.assertFalse(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ger")
        self.assertFalse(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"],
            {
                "volledigeNaam": "Vincent Bennett",
                "contactnaam": {
                    "voorletters": "V",
                    "voornaam": "Vincent",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bennett",
                },
            },
        )

    def test_update_partij_organisatie(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.organisatie.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            bezoekadres_straatnaam="straat",
            bezoekadres_huisnummer=10,
            bezoekadres_huisnummertoevoeging="A2",
            bezoekadres_postcode="1008 DG",
            bezoekadres_stad="Amsterdam",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="NL",
            correspondentieadres_nummeraanduiding_id="1234567890000001",
            correspondentieadres_straatnaam="straat",
            correspondentieadres_huisnummer=10,
            correspondentieadres_huisnummertoevoeging="A2",
            correspondentieadres_postcode="1008 DG",
            correspondentieadres_stad="Amsterdam",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="NL",
        )
        OrganisatieFactory(partij=partij, naam="Whitechapel")
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["digitaleAdressen"], [])
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"], [])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.organisatie.value)
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(data["partijIdentificatie"], {"naam": "Whitechapel"})

        data = {
            "nummer": "6427834668",
            "interneNotitie": "changed",
            "digitaleAdressen": [],
            "voorkeursDigitaalAdres": None,
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "soortPartij": SoortPartij.organisatie.value,
            "indicatieGeheimhouding": False,
            "voorkeurstaal": "ger",
            "indicatieActief": False,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "partijIdentificatie": {"naam": "string"},
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["nummer"], "6427834668")
        self.assertEqual(data["interneNotitie"], "changed")
        self.assertEqual(data["digitaleAdressen"], [])
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"], [])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.organisatie.value)
        self.assertFalse(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ger")
        self.assertFalse(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(data["partijIdentificatie"], {"naam": "string"})

    def test_update_partij_contactpersoon(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.contactpersoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            bezoekadres_straatnaam="straat",
            bezoekadres_huisnummer=10,
            bezoekadres_huisnummertoevoeging="A2",
            bezoekadres_postcode="1008 DG",
            bezoekadres_stad="Amsterdam",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="NL",
            correspondentieadres_nummeraanduiding_id="1234567890000001",
            correspondentieadres_straatnaam="straat",
            correspondentieadres_huisnummer=10,
            correspondentieadres_huisnummertoevoeging="A2",
            correspondentieadres_postcode="1008 DG",
            correspondentieadres_stad="Amsterdam",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="NL",
        )
        organisatie = PartijFactory.create(soort_partij=SoortPartij.organisatie.value)
        ContactpersoonFactory.create(
            partij=partij,
            werkte_voor_partij=organisatie,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        organisatie2 = PartijFactory.create(soort_partij=SoortPartij.organisatie.value)
        ContactpersoonFactory.create(
            werkte_voor_partij=organisatie2,
            contactnaam_voorletters="V",
            contactnaam_voornaam="Vincent",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Benette",
        )
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["digitaleAdressen"], [])
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"], [])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.contactpersoon.value)
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"]["werkteVoorPartij"],
            {
                "uuid": str(organisatie.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/partijen/{str(organisatie.uuid)}",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"]["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        data = {
            "nummer": "6427834668",
            "interneNotitie": "changed",
            "digitaleAdressen": [],
            "voorkeursDigitaalAdres": None,
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "soortPartij": SoortPartij.contactpersoon.value,
            "indicatieGeheimhouding": False,
            "voorkeurstaal": "ger",
            "indicatieActief": False,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "partijIdentificatie": {
                "werkteVoorPartij": {"uuid": str(organisatie2.uuid)},
                "contactnaam": {
                    "voorletters": "V",
                    "voornaam": "Vincent",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bennett",
                },
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["nummer"], "6427834668")
        self.assertEqual(data["interneNotitie"], "changed")
        self.assertEqual(data["digitaleAdressen"], [])
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"], [])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.contactpersoon.value)
        self.assertFalse(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ger")
        self.assertFalse(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"]["werkteVoorPartij"],
            {
                "uuid": str(organisatie2.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/partijen/{str(organisatie2.uuid)}",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"]["contactnaam"],
            {
                "voorletters": "V",
                "voornaam": "Vincent",
                "voorvoegselAchternaam": "",
                "achternaam": "Bennett",
            },
        )

    def test_update_partij_contactpersoon_to_persoon(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.contactpersoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            bezoekadres_straatnaam="straat",
            bezoekadres_huisnummer=10,
            bezoekadres_huisnummertoevoeging="A2",
            bezoekadres_postcode="1008 DG",
            bezoekadres_stad="Amsterdam",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="NL",
            correspondentieadres_nummeraanduiding_id="1234567890000001",
            correspondentieadres_straatnaam="straat",
            correspondentieadres_huisnummer=10,
            correspondentieadres_huisnummertoevoeging="A2",
            correspondentieadres_postcode="1008 DG",
            correspondentieadres_stad="Amsterdam",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="NL",
        )
        organisatie = PartijFactory.create(soort_partij=SoortPartij.organisatie.value)
        ContactpersoonFactory.create(
            partij=partij,
            werkte_voor_partij=organisatie,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["digitaleAdressen"], [])
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"], [])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.contactpersoon.value)
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"]["werkteVoorPartij"],
            {
                "uuid": str(organisatie.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/partijen/{str(organisatie.uuid)}",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"]["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )

        data = {
            "nummer": "6427834668",
            "interneNotitie": "changed",
            "digitaleAdressen": [],
            "voorkeursDigitaalAdres": None,
            "rekeningnummers": [],
            "voorkeursRekeningnummer": None,
            "soortPartij": SoortPartij.persoon.value,
            "indicatieGeheimhouding": False,
            "voorkeurstaal": "ger",
            "indicatieActief": False,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "partijIdentificatie": {
                "contactnaam": {
                    "voorletters": "V",
                    "voornaam": "Vincent",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bennett",
                },
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["nummer"], "6427834668")
        self.assertEqual(data["interneNotitie"], "changed")
        self.assertEqual(data["digitaleAdressen"], [])
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"], [])
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertEqual(data["soortPartij"], SoortPartij.persoon.value)
        self.assertFalse(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ger")
        self.assertFalse(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000003",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"],
            {
                "volledigeNaam": "Vincent Bennett",
                "contactnaam": {
                    "voorletters": "V",
                    "voornaam": "Vincent",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bennett",
                },
            },
        )

    def test_partial_update_partij(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.persoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            bezoekadres_straatnaam="straat",
            bezoekadres_huisnummer=10,
            bezoekadres_huisnummertoevoeging="A2",
            bezoekadres_postcode="1008 DG",
            bezoekadres_stad="Amsterdam",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="NL",
            correspondentieadres_nummeraanduiding_id="1234567890000001",
            correspondentieadres_straatnaam="straat",
            correspondentieadres_huisnummer=10,
            correspondentieadres_huisnummertoevoeging="A2",
            correspondentieadres_postcode="1008 DG",
            correspondentieadres_stad="Amsterdam",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="NL",
        )
        digitaal_adres = DigitaalAdresFactory.create(partij=partij)
        digitaal_adres2 = DigitaalAdresFactory.create(partij=None)

        rekeningnummer = RekeningnummerFactory.create(partij=partij)
        rekeningnummer2 = RekeningnummerFactory.create()

        PersoonFactory.create(
            partij=partij,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )

        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["digitaleAdressen"][0]["uuid"], str(digitaal_adres.uuid))
        self.assertIsNone(data["voorkeursDigitaalAdres"])
        self.assertEqual(data["rekeningnummers"][0]["uuid"], str(rekeningnummer.uuid))
        self.assertIsNone(data["voorkeursRekeningnummer"])
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"],
            {
                "volledigeNaam": "Phil Bozeman",
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                },
            },
        )

        data = {
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["nummer"], "1298329191")
        self.assertEqual(data["interneNotitie"], "interneNotitie")
        self.assertEqual(data["digitaleAdressen"][0]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres.uuid)
        )
        self.assertEqual(data["rekeningnummers"][0]["uuid"], str(rekeningnummer.uuid))
        self.assertEqual(
            data["voorkeursRekeningnummer"]["uuid"], str(rekeningnummer.uuid)
        )
        self.assertEqual(data["soortPartij"], SoortPartij.persoon.value)
        self.assertTrue(data["indicatieGeheimhouding"])
        self.assertEqual(data["voorkeurstaal"], "ndl")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["partijIdentificatie"],
            {
                "volledigeNaam": "Phil Bozeman",
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                },
            },
        )

        with self.subTest("voorkeurs_adres_must_be_given_digitaal_adres_validation"):
            data["voorkeursDigitaalAdres"] = {"uuid": str(digitaal_adres2.uuid)}
            response = self.client.patch(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "voorkeursDigitaalAdres")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "Het voorkeurs adres moet een gelinkte digitaal adres zijn.",
            )

        with self.subTest(
            "voorkeurs_rekeningnummer_must_be_given_rekeningnummers_validation"
        ):
            # set voorkeursDigitaalAdres to none because of previous subtest
            data["voorkeursDigitaalAdres"] = None

            data["voorkeursRekeningnummer"] = {"uuid": str(rekeningnummer2.uuid)}
            response = self.client.patch(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "voorkeursRekeningnummer")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "Het voorkeurs rekeningnummer moet een gelinkte rekeningnummer zijn.",
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

    def test_digitale_adressen_inclusion_param(self):
        persoon = PersoonFactory(partij__soort_partij=SoortPartij.persoon)

        persoon_with_adressen = PersoonFactory(partij__soort_partij=SoortPartij.persoon)
        digitaal_adres = DigitaalAdresFactory(partij=persoon_with_adressen.partij)

        def _get_detail_url(partij: Partij) -> str:
            return reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
            )

        # request the partij *without* any digitale adressen
        response = self.client.get(
            _get_detail_url(persoon.partij), data=dict(expand="digitaleAdressen")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data: dict = response.json()

        self.assertEqual(response_data["_expand"], {"digitaleAdressen": []})

        # request the partij *with* digitale adressen
        response = self.client.get(
            _get_detail_url(persoon_with_adressen.partij),
            data=dict(expand="digitaleAdressen"),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data: dict = response.json()

        received_adressen = response_data["_expand"]["digitaleAdressen"]
        expected_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs=dict(uuid=digitaal_adres.uuid),
        )

        self.assertEqual(len(received_adressen), 1)
        self.assertEqual(
            received_adressen[0]["url"], f"http://testserver{expected_url}"
        )


class NestedPartijIdentificatorTests(APITestCase):
    list_url = reverse_lazy("klantinteracties:partij-list")

    def test_read(self):
        partij = PartijFactory.create()
        partij_identificator = BsnPartijIdentificatorFactory.create(partij=partij)
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        url = "http://testserver/klantinteracties/api/v1"
        self.assertEqual(
            data["partijIdentificatoren"],
            [
                {
                    "uuid": str(partij_identificator.uuid),
                    "url": f"{url}/partij-identificatoren/{str(partij_identificator.uuid)}",
                    "identificeerdePartij": {
                        "uuid": str(partij.uuid),
                        "url": f"{url}/partijen/{str(partij.uuid)}",
                    },
                    "anderePartijIdentificator": partij_identificator.andere_partij_identificator,
                    "partijIdentificator": {
                        "codeObjecttype": partij_identificator.partij_identificator_code_objecttype,
                        "codeSoortObjectId": partij_identificator.partij_identificator_code_soort_object_id,
                        "objectId": partij_identificator.partij_identificator_object_id,
                        "codeRegister": partij_identificator.partij_identificator_code_register,
                    },
                    "subIdentificatorVan": partij_identificator.sub_identificator_van,
                }
            ],
        )

    def test_create_partij_with_new_partij_identificator(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        list_url = reverse("klantinteracties:partij-list")
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "partijIdentificatoren": [
                {
                    "anderePartijIdentificator": "anderePartijIdentificator",
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "296648875",
                        "codeRegister": "brp",
                    },
                }
            ],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(Partij.objects.all().count(), 1)
        self.assertEqual(PartijIdentificator.objects.all().count(), 1)

        partij = Partij.objects.get(uuid=response_data["uuid"])
        self.assertEqual(partij.partijidentificator_set.count(), 1)
        self.assertEqual(len(response_data["partijIdentificatoren"]), 1)

        partij_identificator = partij.partijidentificator_set.get()
        partij_identificator_dict = response_data["partijIdentificatoren"][0]
        self.assertEqual(
            partij_identificator_dict["uuid"],
            str(partij_identificator.uuid),
        )
        self.assertEqual(
            partij_identificator_dict["identificeerdePartij"]["uuid"],
            str(partij_identificator.partij.uuid),
        )
        self.assertEqual(
            partij_identificator_dict["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )
        self.assertEqual(
            partij_identificator_dict["subIdentificatorVan"],
            partij_identificator.sub_identificator_van,
        )

    def test_create_with_null_values(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }
        self.assertEqual(Partij.objects.all().count(), 0)

        for sub_test in [
            (lambda data: data, 1),
            (lambda data: data.setdefault("partijIdentificatoren", None), 2),
            (lambda data: data.setdefault("partijIdentificatoren", []), 3),
        ]:
            sub_test[0](data)
            response = self.client.post(self.list_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = response.json()
            partij = Partij.objects.get(uuid=str(response_data["uuid"]))
            self.assertEqual(partij.partijidentificator_set.count(), 0)
            self.assertEqual(response_data["partijIdentificatoren"], [])
            self.assertEqual(Partij.objects.all().count(), sub_test[1])

    def test_create_with_wrong_uuid(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "partijIdentificatoren": [
                {
                    "anderePartijIdentificator": "anderePartijIdentificator",
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "296648875",
                        "codeRegister": "brp",
                    },
                }
            ],
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }
        # object with this UUID does not exist for partijIdentificatoren
        data["partijIdentificatoren"][0]["uuid"] = str(rekeningnummer.uuid)
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "partijIdentificatoren.0.uuid")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(error["reason"], "PartijIdentificator object bestaat niet.")

    def test_create_existing_uuid_and_same_partij(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        partij = PartijFactory()
        # pass kvk_nummer uuid for new bsn data
        kvk_nummer = KvkNummerPartijIdentificatorFactory.create(partij=partij)
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "partijIdentificatoren": [
                {
                    "uuid": str(kvk_nummer.uuid),
                    "anderePartijIdentificator": "anderePartijIdentificator",
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "296648875",
                        "codeRegister": "brp",
                    },
                }
            ],
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()

        # created new partij
        # kvk_nummer was updated with bsn data
        self.assertEqual(len(response_data["partijIdentificatoren"]), 1)

        partij_identificator = PartijIdentificator.objects.get()
        partij_identificator_dict = response_data["partijIdentificatoren"][0]

        self.assertEqual(
            partij_identificator_dict["uuid"],
            str(partij_identificator.uuid),
        )
        self.assertEqual(
            partij_identificator_dict["identificeerdePartij"]["uuid"],
            str(partij_identificator.partij.uuid),
        )
        self.assertEqual(
            partij_identificator_dict["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )
        self.assertEqual(
            partij_identificator_dict["subIdentificatorVan"],
            partij_identificator.sub_identificator_van,
        )

    def test_create_existing_uuid_and_different_partij(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "partijIdentificatoren": [
                {
                    "anderePartijIdentificator": "anderePartijIdentificator",
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "296648875",
                        "codeRegister": "brp",
                    },
                }
            ],
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }

        # pass kvk_nummer uuid for new bsn data
        new_partij = PartijFactory.create()
        kvk_nummer = KvkNummerPartijIdentificatorFactory.create(partij=new_partij)
        data["partijIdentificatoren"][0]["uuid"] = str(kvk_nummer.uuid)
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()

        # created new partij
        # kvk_nummer was updated with bsn data and also partij belonging.
        self.assertEqual(len(response_data["partijIdentificatoren"]), 1)

        partij_identificator = PartijIdentificator.objects.get()
        partij_identificator_dict = response_data["partijIdentificatoren"][0]
        self.assertEqual(
            partij_identificator_dict["uuid"],
            str(partij_identificator.uuid),
        )
        self.assertNotEqual(partij_identificator.partij, new_partij)
        self.assertEqual(
            partij_identificator_dict["identificeerdePartij"]["uuid"],
            str(partij_identificator.partij.uuid),
        )
        self.assertEqual(
            partij_identificator_dict["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )
        self.assertEqual(
            partij_identificator_dict["subIdentificatorVan"],
            partij_identificator.sub_identificator_van,
        )

    def test_create_vestigingsnummer(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        partij = PartijFactory.create()
        self.assertEqual(Partij.objects.count(), 1)
        kvk_nummer = KvkNummerPartijIdentificatorFactory.create(partij=partij)
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "partijIdentificatoren": [
                {
                    "sub_identificator_van": {"uuid": str(kvk_nummer.uuid)},
                    "anderePartijIdentificator": "anderePartijIdentificator",
                    "partijIdentificator": {
                        "codeObjecttype": "vestiging",
                        "codeSoortObjectId": "vestigingsnummer",
                        "objectId": "444455556666",
                        "codeRegister": "hr",
                    },
                }
            ],
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Partij.objects.count(), 2)

    def test_create_kvk_nummer_and_create_vestigingsnummer(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "partijIdentificatoren": [
                {
                    "partijIdentificator": {
                        "codeObjecttype": "niet_natuurlijk_persoon",
                        "codeSoortObjectId": "kvk_nummer",
                        "objectId": "12345678",
                        "codeRegister": "hr",
                    },
                }
            ],
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        partij = Partij.objects.get()
        sub_identificator_van = PartijIdentificator.objects.get()

        data = {
            "partijIdentificatoren": [
                {
                    "uuid": str(sub_identificator_van.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "niet_natuurlijk_persoon",
                        "codeSoortObjectId": "kvk_nummer",
                        "objectId": "12345678",
                        "codeRegister": "hr",
                    },
                },
                {
                    "sub_identificator_van": {"uuid": str(sub_identificator_van.uuid)},
                    "partijIdentificator": {
                        "codeObjecttype": "vestiging",
                        "codeSoortObjectId": "vestigingsnummer",
                        "objectId": "444455556666",
                        "codeRegister": "hr",
                    },
                },
            ],
        }
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data["partijIdentificatoren"]), 2)

    def test_invalid_create_where_partij_uuid_is_passed(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        list_url = reverse("klantinteracties:partij-list")
        partij = PartijFactory.create()
        self.assertEqual(Partij.objects.all().count(), 1)

        # identificeerdePartij' must not be selected.
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "partijIdentificatoren": [
                {
                    "identificeerdePartij": {"uuid": str(partij.uuid)},
                    "anderePartijIdentificator": "anderePartijIdentificator",
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "296648875",
                        "codeRegister": "brp",
                    },
                }
            ],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.persoon.value,
            "indicatieActief": True,
            "partijIdentificatie": {
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                }
            },
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(
            response, "partijIdentificatoren.identificeerdePartij"
        )
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "Het veld `identificeerde_partij` wordt automatisch ingesteld en dient niet te worden opgegeven.",
        )

        self.assertEqual(Partij.objects.all().count(), 1)

        # PATC and PUT allow to pass identificeerdePartij
        data["soortPartij"] = SoortPartij.organisatie.value
        data["partijIdentificatie"] = {"naam": "string"}
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        # PUT same data received from POST
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data["partijIdentificatoren"]), 1)
        self.assertEqual(response_data["soortPartij"], SoortPartij.organisatie.value)

    def test_invalid_create_partij_identificator_globally_uniqueness(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        list_url = reverse("klantinteracties:partij-list")

        bsn = BsnPartijIdentificatorFactory.create()

        self.assertIsNotNone(bsn.partij)
        self.assertEqual(Partij.objects.all().count(), 1)

        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "partijIdentificatoren": [
                {
                    "anderePartijIdentificator": "anderePartijIdentificator",
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "296648875",
                        "codeRegister": "brp",
                    },
                }
            ],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }
        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "__all__")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie.",
        )
        # Remains only 1 partij
        self.assertEqual(Partij.objects.all().count(), 1)

    def test_invalid_create_duplicated_partij_identificator_globally_uniqueness(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        list_url = reverse("klantinteracties:partij-list")

        self.assertEqual(Partij.objects.all().count(), 0)
        self.assertEqual(PartijIdentificator.objects.all().count(), 0)
        partij_identificator_dict = {
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "partijIdentificatoren": [
                partij_identificator_dict,
                partij_identificator_dict,
            ],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }
        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "__all__")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie.",
        )
        self.assertEqual(Partij.objects.all().count(), 0)
        self.assertEqual(PartijIdentificator.objects.all().count(), 0)

    def test_invalid_create_sub_identificator_required(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        list_url = reverse("klantinteracties:partij-list")

        self.assertEqual(Partij.objects.all().count(), 0)
        self.assertEqual(PartijIdentificator.objects.all().count(), 0)

        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "partijIdentificatoren": [
                {
                    "partijIdentificator": {
                        "codeObjecttype": "vestiging",
                        "codeSoortObjectId": "vestigingsnummer",
                        "objectId": "444455556666",
                        "codeRegister": "hr",
                    },
                },
            ],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "indicatieActief": True,
        }
        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(
            response, "partijIdentificatoren.0.subIdentificatorVan"
        )
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "Voor een PartijIdentificator met codeSoortObjectId = `vestigingsnummer` is het verplicht"
            " om een `sub_identifier_van` met codeSoortObjectId = `kvk_nummer` te kiezen.",
        )
        self.assertEqual(Partij.objects.all().count(), 0)
        self.assertEqual(PartijIdentificator.objects.all().count(), 0)

    def test_invalid_duplicated_uuid_passed_sub_identificator_required(self):
        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        list_url = reverse("klantinteracties:partij-list")
        bsn = BsnPartijIdentificatorFactory.create()
        data = {
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "partijIdentificatoren": [
                {
                    "uuid": str(bsn.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "123456782",
                        "codeRegister": "brp",
                    },
                },
                {
                    "uuid": str(bsn.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "niet_natuurlijk_persoon",
                        "codeSoortObjectId": "kvk_nummer",
                        "objectId": "12345678",
                        "codeRegister": "hr",
                    },
                },
            ],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.persoon.value,
            "indicatieActief": True,
            "partijIdentificatie": {
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                }
            },
        }
        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(
            response, "partijIdentificatoren.identificeerdePartij"
        )
        self.assertEqual(error["code"], "duplicated")
        self.assertEqual(
            error["reason"],
            "Duplicaat uuid kan niet worden ingevoerd voor `partij_identificatoren`.",
        )

    def test_partially_update_with_null_values(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            soort_partij=SoortPartij.persoon.value,
        )

        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )

        data = {}

        for sub_test in [
            (lambda data: data, 0),
            (lambda data: data.setdefault("partijIdentificatoren", None), 0),
            (lambda data: data.setdefault("partijIdentificatoren", []), 0),
        ]:
            sub_test[0](data)
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.assertEqual(response_data["partijIdentificatoren"], [])
            self.assertEqual(partij.partijidentificator_set.count(), sub_test[1])

    def test_partially_update_where_all_partij_identificatoren_have_uuid(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.persoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
        )
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        bsn = BsnPartijIdentificatorFactory.create(partij=partij)
        kvk_nummer = KvkNummerPartijIdentificatorFactory.create(partij=partij)
        vestigingsnummer = VestigingsnummerPartijIdentificatorFactory.create(
            partij=partij
        )

        # changes are only for objectId
        data = {
            "partijIdentificatoren": [
                {
                    "uuid": str(bsn.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "123456782",
                        "codeRegister": "brp",
                    },
                },
                {
                    "uuid": str(kvk_nummer.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "niet_natuurlijk_persoon",
                        "codeSoortObjectId": "kvk_nummer",
                        "objectId": "11112222",
                        "codeRegister": "hr",
                    },
                },
                {
                    "uuid": str(vestigingsnummer.uuid),
                    "sub_identificator_van": {"uuid": str(kvk_nummer.uuid)},
                    "partijIdentificator": {
                        "codeObjecttype": "vestiging",
                        "codeSoortObjectId": "vestigingsnummer",
                        "objectId": "444455556666",
                        "codeRegister": "hr",
                    },
                },
            ],
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        partij = Partij.objects.get(pk=partij.pk)

        self.assertEqual(len(response_data["partijIdentificatoren"]), 3)
        new_bsn = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="bsn"
        )
        new_kvk_nummer = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="kvk_nummer"
        )
        new_vestigingsnummer = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="vestigingsnummer"
        )
        # assert that they are the same objects
        self.assertEqual(new_bsn.uuid, bsn.uuid)
        self.assertEqual(new_kvk_nummer.uuid, kvk_nummer.uuid)
        self.assertEqual(new_vestigingsnummer.uuid, vestigingsnummer.uuid)
        # assert that the object_ids have been updated
        self.assertEqual(new_bsn.partij_identificator_object_id, "123456782")
        self.assertEqual(new_kvk_nummer.partij_identificator_object_id, "11112222")
        self.assertEqual(
            new_vestigingsnummer.partij_identificator_object_id, "444455556666"
        )

    def test_partially_update_where_no_partij_identificatoren_have_uuid(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.persoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
        )
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        bsn = BsnPartijIdentificatorFactory.create(partij=partij)
        kvk_nummer = KvkNummerPartijIdentificatorFactory.create(partij=partij)

        # changes are only for objectId
        data = {
            "partijIdentificatoren": [
                {
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "123456782",
                        "codeRegister": "brp",
                    },
                },
                {
                    "partijIdentificator": {
                        "codeObjecttype": "niet_natuurlijk_persoon",
                        "codeSoortObjectId": "kvk_nummer",
                        "objectId": "11112222",
                        "codeRegister": "hr",
                    },
                },
            ],
        }
        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        partij = Partij.objects.get(pk=partij.pk)
        self.assertEqual(len(response_data["partijIdentificatoren"]), 2)
        new_bsn = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="bsn"
        )
        new_kvk_nummer = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="kvk_nummer"
        )
        # assert they are different
        self.assertNotEqual(new_bsn.uuid, bsn.uuid)
        self.assertNotEqual(new_kvk_nummer.uuid, kvk_nummer.uuid)

        # assert that the object_ids have been updated
        self.assertEqual(new_bsn.partij_identificator_object_id, "123456782")
        self.assertEqual(new_kvk_nummer.partij_identificator_object_id, "11112222")

    def test_partially_update_where_not_all_partij_identificatoren_have_uuid(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.persoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
        )
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        bsn = BsnPartijIdentificatorFactory.create(partij=partij)
        kvk_nummer = KvkNummerPartijIdentificatorFactory.create(partij=partij)
        vestigingsnummer = VestigingsnummerPartijIdentificatorFactory.create(
            partij=partij
        )

        # changes are only for objectId
        data = {
            "partijIdentificatoren": [
                {
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "123456782",
                        "codeRegister": "brp",
                    },
                },
                {
                    "uuid": str(kvk_nummer.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "niet_natuurlijk_persoon",
                        "codeSoortObjectId": "kvk_nummer",
                        "objectId": "11112222",
                        "codeRegister": "hr",
                    },
                },
                {
                    "uuid": str(vestigingsnummer.uuid),
                    "sub_identificator_van": {"uuid": str(kvk_nummer.uuid)},
                    "partijIdentificator": {
                        "codeObjecttype": "vestiging",
                        "codeSoortObjectId": "vestigingsnummer",
                        "objectId": "444455556666",
                        "codeRegister": "hr",
                    },
                },
            ],
        }
        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        partij = Partij.objects.get(pk=partij.pk)
        self.assertEqual(len(response_data["partijIdentificatoren"]), 3)
        new_bsn = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="bsn"
        )
        new_kvk_nummer = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="kvk_nummer"
        )
        new_vestigingsnummer = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="vestigingsnummer"
        )
        # assert bsn was deleted and then created again with new values
        self.assertNotEqual(new_bsn.uuid, bsn.uuid)
        # assert that they are the same objects
        self.assertEqual(new_kvk_nummer.uuid, kvk_nummer.uuid)
        self.assertEqual(new_vestigingsnummer.uuid, vestigingsnummer.uuid)
        # assert that the object_ids have been updated
        self.assertEqual(new_bsn.partij_identificator_object_id, "123456782")
        self.assertEqual(new_kvk_nummer.partij_identificator_object_id, "11112222")
        self.assertEqual(
            new_vestigingsnummer.partij_identificator_object_id, "444455556666"
        )

    def test_partially_update_overwriting_partij_identificator(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.persoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
        )
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        bsn = BsnPartijIdentificatorFactory.create(partij=partij)

        self.assertTrue(partij.partijidentificator_set.count(), 1)
        self.assertFalse(
            partij.partijidentificator_set.filter(
                partij_identificator_code_soort_object_id="kvk_nummer"
            ).exists()
        )
        # changes are only for objectId
        data = {
            "partijIdentificatoren": [
                {  # same data as bsn object, without uuid
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "296648875",
                        "codeRegister": "brp",
                    },
                },
                {
                    "partijIdentificator": {
                        "codeObjecttype": "niet_natuurlijk_persoon",
                        "codeSoortObjectId": "kvk_nummer",
                        "objectId": "11112222",
                        "codeRegister": "hr",
                    },
                },
            ],
        }
        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        partij = Partij.objects.get(pk=partij.pk)

        self.assertEqual(len(response_data["partijIdentificatoren"]), 2)

        new_bsn = partij.partijidentificator_set.get(
            partij_identificator_code_soort_object_id="bsn"
        )
        # assert that bsn is new object, with same data
        self.assertNotEqual(new_bsn.uuid, bsn.uuid)

        # assert that kvk_nummer was created
        self.assertTrue(partij.partijidentificator_set.count(), 2)
        self.assertTrue(
            partij.partijidentificator_set.filter(
                partij_identificator_code_soort_object_id="kvk_nummer"
            ).exists()
        )

    def test_invalid_partially_update_globally_uniqueness(self):
        partij_a = PartijFactory.create(soort_partij=SoortPartij.persoon.value)
        partij_b = PartijFactory.create()
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij_a.uuid)}
        )

        BsnPartijIdentificatorFactory.create(partij=partij_a)
        BsnPartijIdentificatorFactory.create(
            partij=partij_b, partij_identificator_object_id="123456782"
        )
        self.assertTrue(partij_a.partijidentificator_set.count(), 1)
        self.assertTrue(partij_b.partijidentificator_set.count(), 1)
        self.assertEqual(partij_a.soort_partij, SoortPartij.persoon.value)
        data = {
            "partijIdentificatoren": [
                {
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "123456782",
                        "codeRegister": "brp",
                    },
                },
            ],
        }
        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "__all__")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie.",
        )

        self.assertTrue(partij_a.partijidentificator_set.count(), 1)
        self.assertTrue(partij_b.partijidentificator_set.count(), 1)
        # partij has the same data
        self.assertEqual(partij_a.soort_partij, SoortPartij.persoon.value)

    def test_invalid_partially_update_locally_uniqueness(self):
        partij = PartijFactory.create(soort_partij=SoortPartij.persoon.value)
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )

        bsn = BsnPartijIdentificatorFactory.create(partij=partij)
        kvk_nummer = KvkNummerPartijIdentificatorFactory.create(partij=partij)
        self.assertTrue(partij.partijidentificator_set.count(), 2)

        self.assertEqual(partij.soort_partij, SoortPartij.persoon.value)

        data = {
            "partijIdentificatoren": [
                {  # same data as bsn object
                    "uuid": str(bsn.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "123456782",
                        "codeRegister": "brp",
                    },
                },
                {  # update kvk_nummer with bsn
                    "uuid": str(kvk_nummer.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "296648875",
                        "codeRegister": "brp",
                    },
                },
            ],
        }
        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "__all__")
        self.assertEqual(error["code"], "unique_together")
        self.assertEqual(
            error["reason"],
            "Partij identificator met deze Partij en Soort object ID bestaat al.",
        )
        # partij has the same data
        self.assertEqual(partij.soort_partij, SoortPartij.persoon.value)

    def test_update_partij_identificatoren_only_required(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij=SoortPartij.persoon.value,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
        )
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        data = {
            "partijIdentificatoren": [{}],
        }
        with self.subTest("invalid_put_empty_dict"):
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "indicatieActief")
            self.assertEqual(error["code"], "required")
            self.assertEqual(
                error["reason"],
                "Dit veld is vereist.",
            )
        with self.subTest("invalid_patch_empty_dict"):
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "partijIdentificatoren": [
                {
                    "partijIdentificator": {},
                }
            ],
        }

        with self.subTest("invalid_put_empty_dict_for_object"):
            # PUT partijIdentificator values are required
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error_object_type = get_validation_errors(
                response, "partijIdentificatoren.0.partijIdentificator.codeObjecttype"
            )
            error_register = get_validation_errors(
                response, "partijIdentificatoren.0.partijIdentificator.codeRegister"
            )
            error_object_id = get_validation_errors(
                response, "partijIdentificatoren.0.partijIdentificator.objectId"
            )
            error_soort_object_id = get_validation_errors(
                response,
                "partijIdentificatoren.0.partijIdentificator.codeSoortObjectId",
            )
            self.assertEqual(error_object_type["code"], "required")
            self.assertEqual(error_register["code"], "required")
            self.assertEqual(error_object_id["code"], "required")
            self.assertEqual(error_soort_object_id["code"], "required")

        with self.subTest("invalid_patch_empty_dict_for_object"):
            # PATCH partijIdentificator values are required
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error_object_type = get_validation_errors(
                response, "partijIdentificatoren.0.partijIdentificator.codeObjecttype"
            )
            error_register = get_validation_errors(
                response, "partijIdentificatoren.0.partijIdentificator.codeRegister"
            )
            error_object_id = get_validation_errors(
                response, "partijIdentificatoren.0.partijIdentificator.objectId"
            )
            error_soort_object_id = get_validation_errors(
                response,
                "partijIdentificatoren.0.partijIdentificator.codeSoortObjectId",
            )
            self.assertEqual(error_object_type["code"], "required")
            self.assertEqual(error_register["code"], "required")
            self.assertEqual(error_object_id["code"], "required")
            self.assertEqual(error_soort_object_id["code"], "required")

    def test_invalid_update_delete_sub_identificator(self):
        partij = PartijFactory.create(soort_partij=SoortPartij.persoon.value)
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=partij
        )
        vestigingsnummer = VestigingsnummerPartijIdentificatorFactory.create(
            partij=partij,
            sub_identificator_van=sub_identificator_van,
        )

        self.assertEqual(partij.soort_partij, SoortPartij.persoon.value)
        self.assertEqual(Partij.objects.all().count(), 1)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)
        data = {
            "partijIdentificatoren": [
                {
                    "uuid": str(vestigingsnummer.uuid),
                    "sub_identificator_van": {"uuid": str(sub_identificator_van.uuid)},
                    "partijIdentificator": {
                        "codeObjecttype": "vestiging",
                        "codeSoortObjectId": "vestigingsnummer",
                        "objectId": "888888999999",
                        "codeRegister": "hr",
                    },
                },
            ],
        }
        # sub_identificator_van will be deleted and created new one, because the UUID wans't specified
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "Cannot delete some instances of model 'PartijIdentificator' because they are"
                " referenced through protected foreign keys: 'PartijIdentificator.sub_identificator_van'."
            ),
        )
        self.assertEqual(Partij.objects.all().count(), 1)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)
        # partij has the same data
        self.assertEqual(partij.soort_partij, SoortPartij.persoon.value)

    def test_invalid_delete_sub_identificator_van_parent(self):
        partij_a = PartijFactory.create(soort_partij=SoortPartij.persoon.value)
        partij_b = PartijFactory.create(soort_partij=SoortPartij.persoon.value)

        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij_a.uuid)}
        )
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=partij_a
        )
        VestigingsnummerPartijIdentificatorFactory.create(
            partij=partij_b,
            sub_identificator_van=sub_identificator_van,
        )

        partij_a.partijidentificator_set.get()
        partij_b.partijidentificator_set.get()

        # passes the new partijIdentificator = bsn and without specifying kvk_nummer,
        # so it should be deleted, but this is not allowed
        data = {
            "partijIdentificatoren": [
                {
                    "partijIdentificator": {
                        "codeObjecttype": "natuurlijk_persoon",
                        "codeSoortObjectId": "bsn",
                        "objectId": "123456782",
                        "codeRegister": "brp",
                    },
                },
            ],
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "Cannot delete some instances of model 'PartijIdentificator' because they are"
                " referenced through protected foreign keys: 'PartijIdentificator.sub_identificator_van'."
            ),
        )
        self.assertEqual(Partij.objects.all().count(), 2)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)
        partij_a.partijidentificator_set.get()
        partij_b.partijidentificator_set.get()

        # partij has the same data
        self.assertEqual(partij_a.soort_partij, SoortPartij.persoon.value)

    def test_invalid_update_remove_sub_identificator(self):
        partij = PartijFactory.create(soort_partij=SoortPartij.persoon.value)
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=partij
        )
        vestigingsnummer = VestigingsnummerPartijIdentificatorFactory.create(
            partij=partij,
            sub_identificator_van=sub_identificator_van,
        )

        self.assertEqual(partij.soort_partij, SoortPartij.persoon.value)
        self.assertEqual(Partij.objects.all().count(), 1)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)

        data = {
            "partijIdentificatoren": [
                {
                    "uuid": str(sub_identificator_van.uuid),
                    "partijIdentificator": {
                        "codeObjecttype": "niet_natuurlijk_persoon",
                        "codeSoortObjectId": "kvk_nummer",
                        "objectId": "11112222",
                        "codeRegister": "hr",
                    },
                },
                {
                    "uuid": str(vestigingsnummer.uuid),
                    "sub_identificator_van": None,
                    "partijIdentificator": {
                        "codeObjecttype": "vestiging",
                        "codeSoortObjectId": "vestigingsnummer",
                        "objectId": "888888999999",
                        "codeRegister": "hr",
                    },
                },
            ],
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(
            response, "partijIdentificatoren.1.subIdentificatorVan"
        )
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "Voor een PartijIdentificator met codeSoortObjectId = `vestigingsnummer` is het verplicht"
            " om een `sub_identifier_van` met codeSoortObjectId = `kvk_nummer` te kiezen.",
        )
        self.assertEqual(Partij.objects.all().count(), 1)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)
        # partij has the same data
        self.assertEqual(partij.soort_partij, SoortPartij.persoon.value)

    def test_invalid_update_delete_all(self):
        partij = PartijFactory.create(soort_partij=SoortPartij.persoon.value)
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=partij
        )
        VestigingsnummerPartijIdentificatorFactory.create(
            partij=partij,
            sub_identificator_van=sub_identificator_van,
        )

        self.assertEqual(partij.soort_partij, SoortPartij.persoon.value)
        self.assertEqual(Partij.objects.all().count(), 1)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)

        data = {
            "partijIdentificatoren": [],
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "Cannot delete some instances of model 'PartijIdentificator' because they are"
                " referenced through protected foreign keys: 'PartijIdentificator.sub_identificator_van'."
            ),
        )
        self.assertEqual(Partij.objects.all().count(), 1)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)

        # partij has the same data
        self.assertEqual(partij.soort_partij, SoortPartij.persoon.value)
