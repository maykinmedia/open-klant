from django.utils.translation import gettext as _

from rest_framework import status
from vng_api_common.tests import get_validation_errors, reverse

from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.klantinteracties.models.partijen import Partij
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    CategorieFactory,
    CategorieRelatieFactory,
    ContactpersoonFactory,
    OrganisatieFactory,
    PartijFactory,
    PersoonFactory,
    VertegenwoordigdenFactory,
)
from openklant.components.klantinteracties.models.tests.factories.rekeningnummer import (
    RekeningnummerFactory,
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
            "soortPartij": "persoon",
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
        self.assertEqual(data["soortPartij"], "persoon")
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
            self.assertEqual(response_data["soortPartij"], "persoon")
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
                    "name": "digitaleAdressen",
                    "code": "required",
                    "reason": _("This field is required."),
                },
                {
                    "name": "voorkeursDigitaalAdres",
                    "code": "required",
                    "reason": _("This field is required."),
                },
                {
                    "name": "rekeningnummers",
                    "code": "required",
                    "reason": _("This field is required."),
                },
                {
                    "name": "voorkeursRekeningnummer",
                    "code": "required",
                    "reason": _("This field is required."),
                },
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
            "soortPartij": "persoon",
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
            "soortPartij": "persoon",
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
        self.assertEqual(response_data["soortPartij"], "persoon")
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
            "soortPartij": "organisatie",
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
        self.assertEqual(response_data["soortPartij"], "organisatie")
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
        organisatie = PartijFactory.create(soort_partij="organisatie")
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
            "soortPartij": "contactpersoon",
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
        self.assertEqual(response_data["soortPartij"], "contactpersoon")
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
            soort_partij="persoon",
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
        self.assertEqual(data["soortPartij"], "persoon")
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
            "soortPartij": "persoon",
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
        self.assertEqual(data["soortPartij"], "persoon")
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
                "soortPartij": "organisatie",
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

            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()

            self.assertEqual(data["nummer"], "6427834668")
            self.assertEqual(data["interneNotitie"], "changed")
            self.assertEqual(data["digitaleAdressen"], [])
            self.assertIsNone(data["voorkeursDigitaalAdres"])
            self.assertEqual(data["rekeningnummers"], [])
            self.assertIsNone(data["voorkeursRekeningnummer"])
            self.assertEqual(data["soortPartij"], "organisatie")
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
            soort_partij="persoon",
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
                    "name": "digitaleAdressen",
                    "code": "required",
                    "reason": _("This field is required."),
                },
                {
                    "name": "voorkeursDigitaalAdres",
                    "code": "required",
                    "reason": _("This field is required."),
                },
                {
                    "name": "rekeningnummers",
                    "code": "required",
                    "reason": _("This field is required."),
                },
                {
                    "name": "voorkeursRekeningnummer",
                    "code": "required",
                    "reason": _("This field is required."),
                },
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
            "soortPartij": "organisatie",
            "indicatieActief": True,
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["nummer"], "1298329191")
        self.assertEqual(response_data["soortPartij"], "organisatie")
        self.assertEqual(
            response_data["digitaleAdressen"][0]["uuid"], str(digitaal_adres.uuid)
        )
        self.assertEqual(
            response_data["voorkeursDigitaalAdres"]["uuid"], str(digitaal_adres.uuid)
        )
        self.assertEqual(response_data["rekeningnummers"], [])
        self.assertIsNone(response_data["voorkeursRekeningnummer"])

    def test_update_partially_partij_only_required(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            indicatie_geheimhouding=True,
            voorkeurstaal="ndl",
            indicatie_actief=True,
            soort_partij="persoon",
        )

        data = {}
        detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
        )
        response = self.client.patch(detail_url, data)
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
                    "code": "invalid",
                    "reason": "Dit veld is vereist.",
                }
            ],
        )
        data = {
            "soortPartij": "organisatie",
        }
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["soortPartij"], "organisatie")

    def test_update_partij_persoon(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij="persoon",
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
        self.assertEqual(data["soortPartij"], "persoon")
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
            "soortPartij": "persoon",
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
        self.assertEqual(data["soortPartij"], "persoon")
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
            soort_partij="organisatie",
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
        self.assertEqual(data["soortPartij"], "organisatie")
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
            "soortPartij": "organisatie",
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
                "naam": "The Acacia Strain",
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
        self.assertEqual(data["soortPartij"], "organisatie")
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
            {"naam": "The Acacia Strain"},
        )

    def test_update_partij_contactpersoon(self):
        partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            voorkeurs_digitaal_adres=None,
            voorkeurs_rekeningnummer=None,
            soort_partij="contactpersoon",
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
        organisatie = PartijFactory.create(soort_partij="organisatie")
        ContactpersoonFactory.create(
            partij=partij,
            werkte_voor_partij=organisatie,
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
        )
        organisatie2 = PartijFactory.create(soort_partij="organisatie")
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
        self.assertEqual(data["soortPartij"], "contactpersoon")
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
            "soortPartij": "contactpersoon",
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
        self.assertEqual(data["soortPartij"], "contactpersoon")
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
            soort_partij="contactpersoon",
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
        organisatie = PartijFactory.create(soort_partij="organisatie")
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
        self.assertEqual(data["soortPartij"], "contactpersoon")
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
            "soortPartij": "persoon",
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
        self.assertEqual(data["soortPartij"], "persoon")
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
            soort_partij="persoon",
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
            "soortPartij": "persoon",
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
        self.assertEqual(data["soortPartij"], "persoon")
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
