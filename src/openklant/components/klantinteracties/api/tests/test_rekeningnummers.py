from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijFactory,
)
from openklant.components.klantinteracties.models.tests.factories.rekeningnummer import (
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

    def test_read_rekeningnummer(self):
        rekeningnummer = RekeningnummerFactory.create()
        detail_url = reverse(
            "klantinteracties:rekeningnummer-detail",
            kwargs={"uuid": str(rekeningnummer.uuid)},
        )

        response = self.client.get(detail_url)

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
