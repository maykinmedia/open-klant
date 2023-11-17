from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
)


class DigitaalAdresTests(JWTAuthMixin, APITestCase):
    def test_list_digitaal_adres(self):
        list_url = reverse("klantinteracties:digitaaladres-list")
        DigitaalAdresFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_digitaal_adres(self):
        digitaal_adres = DigitaalAdresFactory.create()
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_digitaal_adres(self):
        list_url = reverse("klantinteracties:digitaaladres-list")
        data = {
            "betrokkene": None,
            "soortDigitaalAdres": "soortDigitaalAdres",
            "adres": "adres",
            "omschrijving": "omschrijving",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertIsNone(data["betrokkene"])
        self.assertEqual(data["soortDigitaalAdres"], "soortDigitaalAdres")
        self.assertEqual(data["adres"], "adres")
        self.assertEqual(data["omschrijving"], "omschrijving")

        with self.subTest("with_betrokkene"):
            betrokkene = BetrokkeneFactory.create()
            data = {
                "betrokkene": {"uuid": str(betrokkene.uuid)},
                "soortDigitaalAdres": "soortDigitaalAdres",
                "adres": "adres",
                "omschrijving": "omschrijving",
            }

            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            data = response.json()

            self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene.uuid))
            self.assertEqual(data["soortDigitaalAdres"], "soortDigitaalAdres")
            self.assertEqual(data["adres"], "adres")
            self.assertEqual(data["omschrijving"], "omschrijving")

    def test_update_digitaal_adres(self):
        betrokkene, betrokkene2 = BetrokkeneFactory.create_batch(2)
        digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=betrokkene,
            soort_digitaal_adres="soortDigitaalAdres",
            adres="adres",
            omschrijving="omschrijving",
        )
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["soortDigitaalAdres"], "soortDigitaalAdres")
        self.assertEqual(data["adres"], "adres")
        self.assertEqual(data["omschrijving"], "omschrijving")

        data = {
            "betrokkene": {"uuid": str(betrokkene2.uuid)},
            "soortDigitaalAdres": "changed",
            "adres": "changed",
            "omschrijving": "changed",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene2.uuid))
        self.assertEqual(data["soortDigitaalAdres"], "changed")
        self.assertEqual(data["adres"], "changed")
        self.assertEqual(data["omschrijving"], "changed")

        with self.subTest("update_betrokkene_to_none"):
            data = {
                "betrokkene": None,
                "soortDigitaalAdres": "changed",
                "adres": "changed",
                "omschrijving": "changed",
            }

            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertIsNone(data["betrokkene"])
            self.assertEqual(data["soortDigitaalAdres"], "changed")
            self.assertEqual(data["adres"], "changed")
            self.assertEqual(data["omschrijving"], "changed")

    def test_partial_update_digitaal_adres(self):
        betrokkene = BetrokkeneFactory.create()
        digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=betrokkene,
            soort_digitaal_adres="soortDigitaalAdres",
            adres="adres",
            omschrijving="omschrijving",
        )
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["soortDigitaalAdres"], "soortDigitaalAdres")
        self.assertEqual(data["adres"], "adres")
        self.assertEqual(data["omschrijving"], "omschrijving")

        data = {
            "soortDigitaalAdres": "changed",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["betrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["soortDigitaalAdres"], "changed")
        self.assertEqual(data["adres"], "adres")
        self.assertEqual(data["omschrijving"], "omschrijving")

    def test_destroy_digitaal_adres(self):
        digitaal_adres = DigitaalAdresFactory.create()
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:digitaaladres-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
