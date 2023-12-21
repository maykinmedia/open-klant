from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from . import factories


class ExterneRegistersTests(APITestCase):
    def test_getexterneregisters(self):
        url = reverse("referentielijsten:externregister-list")
        factories.ExternRegisterFactory.create_batch(1000)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1000)
        self.assertLess(len(response_data["results"]), 1000)

    def test_postregister(self):
        url = reverse("referentielijsten:externregister-list")
        data = {
            "code": "XKX",
            "locatie": "Kosovo",
            "naam": "2013-04-19",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data["code"], "XKX")
        self.assertEqual(response_data["locatie"], "Kosovo")
        self.assertEqual(response_data["naam"], "2013-04-19")

    def test_delregister(self):
        extern_register, other = factories.ExternRegisterFactory.create_batch(2)
        url = reverse(
            "referentielijsten:externregister-detail",
            kwargs={"code": extern_register.code},
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
            "referentielijsten:externregister-detail",
            kwargs={"code": other.code},
        )
        other_response = self.client.get(other_url)
        self.assertEqual(other_response.status_code, status.HTTP_200_OK)

    def test_getregister(self):
        factories.ExternRegisterFactory.create(
            code="XKX",
            locatie="Kosovo",
            naam="2013-04-19",
        )

        url = reverse("referentielijsten:externregister-detail", kwargs={"code": "XKX"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["code"], "XKX")
        self.assertEqual(response_data["locatie"], "Kosovo")
        self.assertEqual(response_data["naam"], "2013-04-19")

    def test_putregister(self):
        factories.ExternRegisterFactory.create(
            code="BFA",
            locatie="Boven-Volta",
            naam="1966-01-03",
        )

        data = {
            "code": "BFA",
            "locatie": "Burkina Faso",
            "naam": "2014-11-03",
        }

        url = reverse("referentielijsten:externregister-detail", kwargs={"code": "BFA"})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["code"], "BFA")
        self.assertEqual(response_data["locatie"], "Burkina Faso")
        self.assertEqual(response_data["naam"], "2014-11-03")
