from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.contactgegevens.api.tests.factories import (
    OrganisatieFactory,
    PersoonFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class PersoonTests(APITestCase):
    def test_persoon_detail(self):
        persoon = PersoonFactory.create(
            geboortedatum="1980-02-23",
            overlijdensdatum="2020-09-05",
            geslachtsnaam="Doe",
            geslacht="m",
            voorvoegsel="",
            voornamen="John",
            adres_nummeraanduiding_id="1234567890000001",
            adres_straatnaam="straat",
            adres_huisnummer="10",
            adres_huisnummertoevoeging="A2",
            adres_postcode="1008DG",
            adres_stad="Amsterdam",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="CA",
            land="CA",
        )
        detail_url = reverse(
            "contactgegevens:persoon-detail",
            kwargs={"uuid": str(persoon.uuid)},
        )

        expected_adres = {
            "nummeraanduidingId": "1234567890000001",
            "straatnaam": "straat",
            "huisnummer": "10",
            "huisnummertoevoeging": "A2",
            "postcode": "1008DG",
            "stad": "Amsterdam",
            "adresregel1": "adresregel1",
            "adresregel2": "adresregel2",
            "adresregel3": "adresregel3",
            "land": "CA",
        }
        expected_data = {
            "uuid": str(persoon.uuid),
            "url": "http://testserver" + detail_url,
            "geboortedatum": "1980-02-23",
            "overlijdensdatum": "2020-09-05",
            "geslachtsnaam": "Doe",
            "geslacht": "m",
            "voorvoegsel": "",
            "voornamen": "John",
            "adres": expected_adres,
            "land": "CA",
        }

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data, expected_data)

    def test_create_persoon(self):
        list_url = reverse("contactgegevens:persoon-list")

        data = {
            "geboortedatum": "1972-05-05",
            "geslachtsnaam": "Townsend",
            "geslacht": "m",
            "voornamen": "Devin",
            "adres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
            "land": "CA",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["geboortedatum"], "1972-05-05")
        self.assertEqual(data["overlijdensdatum"], None)
        self.assertEqual(data["geslachtsnaam"], "Townsend")
        self.assertEqual(data["geslacht"], "m")
        self.assertEqual(data["voorvoegsel"], "")
        self.assertEqual(data["voornamen"], "Devin")
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
        )
        self.assertEqual(data["land"], "CA")

    def test_update_persoon(self):
        persoon = PersoonFactory.create(
            geboortedatum="1972-05-05",
            overlijdensdatum=None,
            geslachtsnaam="Townsend",
            geslacht="m",
            voorvoegsel="",
            voornamen="Devin",
            adres_nummeraanduiding_id="1234567890000001",
            adres_straatnaam="straat",
            adres_huisnummer="10",
            adres_huisnummertoevoeging="A2",
            adres_postcode="1008DG",
            adres_stad="Amsterdam",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="CA",
            land="CA",
        )
        detail_url = reverse(
            "contactgegevens:persoon-detail",
            kwargs={"uuid": str(persoon.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["geboortedatum"], "1972-05-05")
        self.assertEqual(data["overlijdensdatum"], None)
        self.assertEqual(data["geslachtsnaam"], "Townsend")
        self.assertEqual(data["geslacht"], "m")
        self.assertEqual(data["voorvoegsel"], "")
        self.assertEqual(data["voornamen"], "Devin")
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
        )
        self.assertEqual(data["land"], "CA")

        data = {
            "geboortedatum": "1972-05-06",
            "overlijdensdatum": "2023-11-22",
            "geslachtsnaam": "changed",
            "geslacht": "v",
            "voorvoegsel": "changed",
            "voornamen": "changed",
            "adres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": "10",
                "huisnummertoevoeging": "changed",
                "postcode": "1001AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "FR",
            },
            "land": "FR",
        }
        response = self.client.put(detail_url, data)
        data = response.json()

        self.assertEqual(data["geboortedatum"], "1972-05-06")
        self.assertEqual(data["overlijdensdatum"], "2023-11-22")
        self.assertEqual(data["geslachtsnaam"], "changed")
        self.assertEqual(data["geslacht"], "v")
        self.assertEqual(data["voorvoegsel"], "changed")
        self.assertEqual(data["voornamen"], "changed")
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": "10",
                "huisnummertoevoeging": "changed",
                "postcode": "1001AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "FR",
            },
        )
        self.assertEqual(data["land"], "FR")

    def test_update_partial_persoon(self):
        persoon = PersoonFactory.create(
            geboortedatum="1972-05-05",
            overlijdensdatum=None,
            geslachtsnaam="Townsend",
            geslacht="m",
            voorvoegsel="",
            voornamen="Devin",
            adres_nummeraanduiding_id="1234567890000001",
            adres_straatnaam="straat",
            adres_huisnummer="10",
            adres_huisnummertoevoeging="A2",
            adres_postcode="1008DG",
            adres_stad="Amsterdam",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="CA",
            land="CA",
        )
        detail_url = reverse(
            "contactgegevens:persoon-detail",
            kwargs={"uuid": str(persoon.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["geboortedatum"], "1972-05-05")
        self.assertEqual(data["overlijdensdatum"], None)
        self.assertEqual(data["geslachtsnaam"], "Townsend")
        self.assertEqual(data["geslacht"], "m")
        self.assertEqual(data["voorvoegsel"], "")
        self.assertEqual(data["voornamen"], "Devin")
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
        )
        self.assertEqual(data["land"], "CA")

        data = {
            "overlijdensdatum": "2023-11-22",
        }

        response = self.client.patch(detail_url, data)
        data = response.json()
        self.assertEqual(data["geboortedatum"], "1972-05-05")
        self.assertEqual(data["overlijdensdatum"], "2023-11-22")
        self.assertEqual(data["geslachtsnaam"], "Townsend")
        self.assertEqual(data["geslacht"], "m")
        self.assertEqual(data["voorvoegsel"], "")
        self.assertEqual(data["voornamen"], "Devin")
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
        )
        self.assertEqual(data["land"], "CA")

    def test_list_pagination_pagesize_param(self):
        list_url = reverse("contactgegevens:persoon-list")
        PersoonFactory.create_batch(10)

        response = self.client.get(list_url, {"pageSize": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 10)
        self.assertEqual(len(data["results"]), 5)
        self.assertEqual(data["next"], f"http://testserver{list_url}?page=2&pageSize=5")


class OrganisatiesTests(APITestCase):
    def test_organisatie_detail(self):
        organisatie = OrganisatieFactory.create(
            handelsnaam="Devin Townsend",
            oprichtingsdatum="1980-02-23",
            opheffingsdatum="2020-09-05",
            adres_nummeraanduiding_id="1234567890000001",
            adres_straatnaam="straat",
            adres_huisnummer="10",
            adres_huisnummertoevoeging="A2",
            adres_postcode="1008DG",
            adres_stad="Amsterdam",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="CA",
            land="CA",
        )
        detail_url = reverse(
            "contactgegevens:organisatie-detail",
            kwargs={"uuid": str(organisatie.uuid)},
        )

        expected_adres = {
            "nummeraanduidingId": "1234567890000001",
            "straatnaam": "straat",
            "huisnummer": "10",
            "huisnummertoevoeging": "A2",
            "postcode": "1008DG",
            "stad": "Amsterdam",
            "adresregel1": "adresregel1",
            "adresregel2": "adresregel2",
            "adresregel3": "adresregel3",
            "land": "CA",
        }
        expected_data = {
            "uuid": str(organisatie.uuid),
            "url": "http://testserver" + detail_url,
            "oprichtingsdatum": "1980-02-23",
            "opheffingsdatum": "2020-09-05",
            "handelsnaam": "Devin Townsend",
            "adres": expected_adres,
            "land": "CA",
        }

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data, expected_data)

    def test_create_organisatie(self):
        list_url = reverse("contactgegevens:organisatie-list")

        data = {
            "handelsnaam": "Devin Townsend",
            "oprichtingsdatum": "1996-03-12",
            "adres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
            "land": "CA",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["handelsnaam"], "Devin Townsend")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-12")
        self.assertEqual(data["opheffingsdatum"], None)
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
        )
        self.assertEqual(data["land"], "CA")

    def test_update_organisatie(self):
        organisatie = OrganisatieFactory.create(
            handelsnaam="Devin Townsend",
            oprichtingsdatum="1996-03-12",
            opheffingsdatum=None,
            adres_nummeraanduiding_id="1234567890000001",
            adres_straatnaam="straat",
            adres_huisnummer="10",
            adres_huisnummertoevoeging="A2",
            adres_postcode="1008DG",
            adres_stad="Amsterdam",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="CA",
            land="CA",
        )
        detail_url = reverse(
            "contactgegevens:organisatie-detail",
            kwargs={"uuid": str(organisatie.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["handelsnaam"], "Devin Townsend")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-12")
        self.assertEqual(data["opheffingsdatum"], None)
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
        )
        self.assertEqual(data["land"], "CA")

        data = {
            "handelsnaam": "changed",
            "oprichtingsdatum": "1996-03-13",
            "opheffingsdatum": "2023-11-22",
            "adres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": "10",
                "huisnummertoevoeging": "changed",
                "postcode": "1001AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "FR",
            },
            "land": "FR",
        }
        response = self.client.put(detail_url, data)
        data = response.json()
        self.assertEqual(data["handelsnaam"], "changed")
        self.assertEqual(data["opheffingsdatum"], "2023-11-22")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-13")
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": "10",
                "huisnummertoevoeging": "changed",
                "postcode": "1001AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "FR",
            },
        )
        self.assertEqual(data["land"], "FR")

    def test_update_partial_organisatie(self):
        organisatie = OrganisatieFactory.create(
            handelsnaam="Devin Townsend",
            oprichtingsdatum="1996-03-12",
            opheffingsdatum=None,
            adres_nummeraanduiding_id="1234567890000001",
            adres_straatnaam="straat",
            adres_huisnummer="10",
            adres_huisnummertoevoeging="A2",
            adres_postcode="1008DG",
            adres_stad="Amsterdam",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="CA",
            land="CA",
        )
        detail_url = reverse(
            "contactgegevens:organisatie-detail",
            kwargs={"uuid": str(organisatie.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["handelsnaam"], "Devin Townsend")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-12")
        self.assertEqual(data["opheffingsdatum"], None)
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
        )
        self.assertEqual(data["land"], "CA")

        data = {
            "opheffingsdatum": "2023-11-22",
        }

        response = self.client.patch(detail_url, data)
        data = response.json()

        self.assertEqual(data["handelsnaam"], "Devin Townsend")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-12")
        self.assertEqual(data["opheffingsdatum"], "2023-11-22")
        self.assertEqual(
            data["adres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": "10",
                "huisnummertoevoeging": "A2",
                "postcode": "1008DG",
                "stad": "Amsterdam",
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "CA",
            },
        )
        self.assertEqual(data["land"], "CA")

    def test_list_pagination_pagesize_param(self):
        list_url = reverse("contactgegevens:organisatie-list")
        OrganisatieFactory.create_batch(10)

        response = self.client.get(list_url, {"pageSize": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 10)
        self.assertEqual(len(data["results"]), 5)
        self.assertEqual(data["next"], f"http://testserver{list_url}?page=2&pageSize=5")
