from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from . import factories


class SoortenObjectTests(APITestCase):
    def test_getsoortenobject(self):
        url = reverse("referentielijsten:soortobject-list")
        factories.SoortObjectFactory.create_batch(6)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 6)

    def test_postsoortobject(self):
        url = reverse("referentielijsten:soortobject-list")
        data = {
            "code": "ARK",
            "indicatieActief": True,
            "naam": "Amsterdam-Rijnsoort_object",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_object")

    def test_delsoortobject(self):
        soort_object, other = factories.SoortObjectFactory.create_batch(2)
        url = reverse(
            "referentielijsten:soortobject-detail",
            kwargs={"code": soort_object.code},
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
            "referentielijsten:soortobject-detail",
            kwargs={"code": other.code},
        )
        other_response = self.client.get(other_url)
        self.assertEqual(other_response.status_code, status.HTTP_200_OK)

    def test_getsoortobject(self):
        factories.SoortObjectFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijnsoort_object",
        )

        url = reverse("referentielijsten:soortobject-detail", kwargs={"code": "ARK"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_object")

    def test_putsoortobject(self):
        factories.SoortObjectFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijnsoort_object",
        )

        data = {
            "code": "ARK",
            "indicatie_actief": True,
            "naam": "Amsterdam-Rijnsoort_object",
        }

        url = reverse("referentielijsten:soortobject-detail", kwargs={"code": "ARK"})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_object")
