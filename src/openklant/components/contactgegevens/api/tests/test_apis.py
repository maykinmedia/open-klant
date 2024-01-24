from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.contactgegevens.api.tests.factories import (
    OrganisatieFactory,
    PersoonFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class PersoonTests(APITestCase):
    def test_create_persoon(self):
        list_url = reverse("contactgegevens:persoon-list")

        data = {
            "geboortedatum": "1972-05-05",
            "geslachtsnaam": "Townsend",
            "geslacht": "m",
            "voornamen": "Devin",
            "adres": {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
            "land": "5001",
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
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], "5001")

    def test_update_persoon(self):
        persoon = PersoonFactory(
            geboortedatum="1972-05-05",
            overlijdensdatum=None,
            geslachtsnaam="Townsend",
            geslacht="m",
            voorvoegsel="",
            voornamen="Devin",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="5001",
            land="5001",
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
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], "5001")

        data = {
            "geboortedatum": "1972-05-06",
            "overlijdensdatum": "2023-11-22",
            "geslachtsnaam": "changed",
            "geslacht": "v",
            "voorvoegsel": "changed",
            "voornamen": "changed",
            "adres": {
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "6713",
            },
            "land": "6713",
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
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "6713",
            },
        )
        self.assertEqual(data["land"], "6713")

    def test_update_partial_persoon(self):
        persoon = PersoonFactory(
            geboortedatum="1972-05-05",
            overlijdensdatum=None,
            geslachtsnaam="Townsend",
            geslacht="m",
            voorvoegsel="",
            voornamen="Devin",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="5001",
            land="5001",
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
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], "5001")

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
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], "5001")


class OrganisatiesTests(APITestCase):
    def test_create_organisatie(self):
        list_url = reverse("contactgegevens:organisatie-list")

        data = {
            "handelsnaam": "Devin Townsend",
            "oprichtingsdatum": "1996-03-12",
            "adres": {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
            "land": "5001",
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
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], "5001")

    def test_update_organisatie(self):
        organisatie = OrganisatieFactory(
            handelsnaam="Devin Townsend",
            oprichtingsdatum="1996-03-12",
            opheffingsdatum=None,
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="5001",
            land="5001",
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
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], "5001")

        data = {
            "handelsnaam": "changed",
            "oprichtingsdatum": "1996-03-13",
            "opheffingsdatum": "2023-11-22",
            "adres": {
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "6713",
            },
            "land": "6713",
        }
        response = self.client.put(detail_url, data)
        data = response.json()
        self.assertEqual(data["handelsnaam"], "changed")
        self.assertEqual(data["opheffingsdatum"], "2023-11-22")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-13")
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "6713",
            },
        )
        self.assertEqual(data["land"], "6713")

    def test_update_partial_organisatie(self):
        organisatie = OrganisatieFactory(
            handelsnaam="Devin Townsend",
            oprichtingsdatum="1996-03-12",
            opheffingsdatum=None,
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="5001",
            land="5001",
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
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], "5001")

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
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], "5001")
