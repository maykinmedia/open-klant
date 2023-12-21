from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from . import factories


class SoortenObjectidTests(APITestCase):
    def test_getsoortenobjectid(self):
        url = reverse("referentielijsten:soortobjectid-list")
        factories.SoortObjectidFactory.create_batch(6)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 6)

    def test_postsoortobjectid(self):
        url = reverse("referentielijsten:soortobjectid-list")
        data = {
            "code": "ARK",
            "indicatieActief": True,
            "naam": "Amsterdam-Rijnsoort_objectid",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_objectid")

    def test_delsoortobjectid(self):
        soort_objectid, other = factories.SoortObjectidFactory.create_batch(2)
        url = reverse(
            "referentielijsten:soortobjectid-detail",
            kwargs={"code": soort_objectid.code},
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
            "referentielijsten:soortobjectid-detail",
            kwargs={"code": other.code},
        )
        other_response = self.client.get(other_url)
        self.assertEqual(other_response.status_code, status.HTTP_200_OK)

    def test_getsoortobjectid(self):
        factories.SoortObjectidFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijnsoort_objectid",
        )

        url = reverse("referentielijsten:soortobjectid-detail", kwargs={"code": "ARK"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_objectid")

    def test_putsoortobjectid(self):
        factories.SoortObjectidFactory.create(
            code="ARK",
            indicatie_actief=True,
            naam="Amsterdam-Rijnsoort_objectid",
        )

        data = {
            "code": "ARK",
            "indicatie_actief": True,
            "naam": "Amsterdam-Rijnsoort_objectid",
        }

        url = reverse("referentielijsten:soortobjectid-detail", kwargs={"code": "ARK"})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["code"], "ARK")
        self.assertEqual(response_data["indicatieActief"], True)
        self.assertEqual(response_data["naam"], "Amsterdam-Rijnsoort_objectid")
