from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories import (
    PartijFactory,
    RekeningnummerFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class RekeningnummerTests(APITestCase):
    def test_list_rekeningnummer(self):
        list_url = reverse("klantinteracties:rekeningnummer-list")
        RekeningnummerFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_list_filters(self):
        list_url = reverse("klantinteracties:rekeningnummer-list")
        RekeningnummerFactory.create(bic="12345678")
        RekeningnummerFactory.create(bic="87654321")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["results"]), 2)

        response = self.client.get(list_url, {"bic": "12345678"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["bic"], "12345678")

        response = self.client.get(list_url, {"bic": "00000000"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["results"]), 0)

    def test_list_pagination_pagesize_param(self):
        list_url = reverse("klantinteracties:rekeningnummer-list")
        RekeningnummerFactory.create_batch(10)

        response = self.client.get(list_url, {"pageSize": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 10)
        self.assertEqual(len(data["results"]), 5)
        self.assertEqual(data["next"], f"http://testserver{list_url}?page=2&pageSize=5")

    def test_read_rekeningnummer(self):
        rekeningnummer = RekeningnummerFactory.create()
        detail_url = reverse(
            "klantinteracties:rekeningnummer-detail",
            kwargs={"uuid": str(rekeningnummer.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create_only_required(self):
        response = self.client.post(reverse("klantinteracties:rekeningnummer-list"), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "iban",
                    "code": "required",
                    "reason": "Dit veld is vereist.",
                },
            ],
        )

    def test_update_only_required(self):
        rekeningnummer = RekeningnummerFactory.create(
            partij=PartijFactory.create(),
            iban="NL18BANK23481326",
            bic="1734723742",
        )
        detail_url = reverse(
            "klantinteracties:rekeningnummer-detail",
            kwargs={"uuid": str(rekeningnummer.uuid)},
        )
        # PUT
        response = self.client.put(detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "iban",
                    "code": "required",
                    "reason": "Dit veld is vereist.",
                },
            ],
        )
        # PATCH
        response = self.client.patch(detail_url, {})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_rekeningnummer(self):
        list_url = reverse("klantinteracties:rekeningnummer-list")
        data = {
            "partij": None,
            "iban": "NL18BANK23481326",
            "bic": "1734723742",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertIsNone(data["partij"])
        self.assertEqual(data["iban"], "NL18BANK23481326")
        self.assertEqual(data["bic"], "1734723742")

        with self.subTest("with_partij"):
            partij = PartijFactory.create()
            data["partij"] = {"uuid": str(partij.uuid)}

            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            data = response.json()

            self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
            self.assertEqual(data["iban"], "NL18BANK23481326")
            self.assertEqual(data["bic"], "1734723742")

    def test_update_rekeningnummer(self):
        partij, partij2 = PartijFactory.create_batch(2)
        digitaal_adres = RekeningnummerFactory.create(
            partij=partij2,
            iban="NL18BANK23481326",
            bic="1734723742",
        )
        detail_url = reverse(
            "klantinteracties:rekeningnummer-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij2.uuid))
        self.assertEqual(data["iban"], "NL18BANK23481326")
        self.assertEqual(data["bic"], "1734723742")

        data = {
            "partij": {"uuid": str(partij.uuid)},
            "iban": "NL18BANK746328229",
            "bic": "8258243823",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["iban"], "NL18BANK746328229")
        self.assertEqual(data["bic"], "8258243823")

        with self.subTest("update_partij_to_none"):
            data = {
                "partij": None,
                "iban": "NL18BANK746328229",
                "bic": "8258243823",
            }

            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertIsNone(data["partij"])
            self.assertEqual(data["iban"], "NL18BANK746328229")
            self.assertEqual(data["bic"], "8258243823")

    def test_partial_update_rekeningnummer(self):
        partij = PartijFactory.create()
        digitaal_adres = RekeningnummerFactory.create(
            partij=partij,
            iban="NL18BANK23481326",
            bic="1734723742",
        )
        detail_url = reverse(
            "klantinteracties:rekeningnummer-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["iban"], "NL18BANK23481326")
        self.assertEqual(data["bic"], "1734723742")

        data = {
            "bic": "8438538453",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["iban"], "NL18BANK23481326")
        self.assertEqual(data["bic"], "8438538453")

    def test_destroy_rekeningnummer(self):
        rekeningnummer = RekeningnummerFactory.create()
        detail_url = reverse(
            "klantinteracties:rekeningnummer-detail",
            kwargs={"uuid": str(rekeningnummer.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:rekeningnummer-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
