from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from . import factories


class TalenTests(APITestCase):
    def test_gettalen(self):
        url = reverse("referentielijsten:taal-list")
        factories.TaalFactory.create_batch(6)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 6)

    def test_posttaal(self):
        url = reverse("referentielijsten:taal-list")
        data = {
            "code": "ARK",
            "indicatieActief": True,
            "naam": "Amsterdam-Rijntaal",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijntaal")

    def test_deltaal(self):
        taal, other = factories.TaalFactory.create_batch(2)
        url = reverse(
            "referentielijsten:taal-detail",
            kwargs={"code": taal.code},
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
            "referentielijsten:taal-detail",
            kwargs={"code": other.code},
        )
        other_response = self.client.get(other_url)
        self.assertEqual(other_response.status_code, status.HTTP_200_OK)

    def test_gettaal(self):
        factories.TaalFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijntaal",
        )

        url = reverse("referentielijsten:taal-detail", kwargs={"code": "ARK"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijntaal")

    def test_puttaal(self):
        factories.TaalFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijntaal",
        )

        data = {
            "code": "ARK",
            "indicatie_actief": True,
            "naam": "Amsterdam-Rijntaal",
        }

        url = reverse("referentielijsten:taal-detail", kwargs={"code": "ARK"})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijntaal")
