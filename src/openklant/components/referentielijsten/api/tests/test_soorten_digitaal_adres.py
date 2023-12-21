from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from . import factories


class SoortenDigitaalAdresTests(APITestCase):
    def test_getsoortendigitaaladres(self):
        url = reverse("referentielijsten:soortdigitaaladres-list")
        factories.SoortDigitaalAdresFactory.create_batch(6)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 6)

    def test_postsoortdigitaaladres(self):
        url = reverse("referentielijsten:soortdigitaaladres-list")
        data = {
            "code": "ARK",
            "indicatieActief": True,
            "naam": "Amsterdam-Rijnsoort_digitaal_adres",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_digitaal_adres")

    def test_delsoortdigitaaladres(self):
        soort_digitaal_adres, other = factories.SoortDigitaalAdresFactory.create_batch(
            2
        )
        url = reverse(
            "referentielijsten:soortdigitaaladres-detail",
            kwargs={"code": soort_digitaal_adres.code},
        )

        response = self.client.delete(url)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT],
        )

        # assert it's gone
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

        # assert other still exists
        other_url = reverse(
            "referentielijsten:soortdigitaaladres-detail",
            kwargs={"code": other.code},
        )
        other_response = self.client.get(other_url)
        self.assertEqual(other_response.status_code, status.HTTP_200_OK)

    def test_getsoortdigitaaladres(self):
        factories.SoortDigitaalAdresFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijnsoort_digitaal_adres",
        )

        url = reverse(
            "referentielijsten:soortdigitaaladres-detail", kwargs={"code": "ARK"}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_digitaal_adres")

    def test_putsoortdigitaaladres(self):
        factories.SoortDigitaalAdresFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijnsoort_digitaal_adres",
        )

        data = {
            "code": "ARK",
            "indicatie_actief": True,
            "naam": "Amsterdam-Rijnsoort_digitaal_adres",
        }

        url = reverse(
            "referentielijsten:soortdigitaaladres-detail", kwargs={"code": "ARK"}
        )

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_digitaal_adres")
