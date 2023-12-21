from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from . import factories


class KanalenTests(APITestCase):
    def test_getkanalen(self):
        url = reverse("referentielijsten:kanaal-list")
        factories.KanaalFactory.create_batch(6)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 6)

    def test_postkanaal(self):
        url = reverse("referentielijsten:kanaal-list")
        data = {
            "code": "ARK",
            "indicatieActief": True,
            "naam": "Amsterdam-Rijnkanaal",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnkanaal")

    def test_delkanaal(self):
        kanaal, other = factories.KanaalFactory.create_batch(2)
        url = reverse(
            "referentielijsten:kanaal-detail",
            kwargs={"code": kanaal.code},
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
            "referentielijsten:kanaal-detail",
            kwargs={"code": other.code},
        )
        other_response = self.client.get(other_url)
        self.assertEqual(other_response.status_code, status.HTTP_200_OK)

    def test_getkanaal(self):
        factories.KanaalFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijnkanaal",
        )

        url = reverse("referentielijsten:kanaal-detail", kwargs={"code": "ARK"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnkanaal")

    def test_putkanaal(self):
        factories.KanaalFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijnkanaal",
        )

        data = {
            "code": "ARK",
            "indicatie_actief": True,
            "naam": "Amsterdam-Rijnkanaal",
        }

        url = reverse("referentielijsten:kanaal-detail", kwargs={"code": "ARK"})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnkanaal")
