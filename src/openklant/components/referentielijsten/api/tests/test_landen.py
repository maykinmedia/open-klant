from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from . import factories


class LandenTests(APITestCase):
    def test_getlanden(self):
        url = reverse("referentielijsten:land-list")
        factories.LandFactory.create_batch(6)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 6)

    def test_postland(self):
        url = reverse("referentielijsten:land-list")
        data = {
            "landcode": "XKX",
            "landnaam": "Kosovo",
            "ingangsdatumLand": "2013-04-19",
            "einddatumLand": "9999-12-31",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data["landcode"], "XKX")
        self.assertEqual(response_data["landnaam"], "Kosovo")
        self.assertEqual(response_data["ingangsdatumLand"], "2013-04-19")
        self.assertEqual(response_data["einddatumLand"], "9999-12-31")

    def test_delland(self):
        land, other = factories.LandFactory.create_batch(2)
        url = reverse(
            "referentielijsten:land-detail", kwargs={"landcode": land.landcode}
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
            "referentielijsten:land-detail", kwargs={"landcode": other.landcode}
        )
        other_response = self.client.get(other_url)
        self.assertEqual(other_response.status_code, status.HTTP_200_OK)

    def test_getland(self):
        factories.LandFactory.create(
            landcode="XKX",
            landnaam="Kosovo",
            ingangsdatum_land="2013-04-19",
            einddatum_land="9999-12-31",
        )

        url = reverse("referentielijsten:land-detail", kwargs={"landcode": "XKX"})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["landcode"], "XKX")
        self.assertEqual(response_data["landnaam"], "Kosovo")
        self.assertEqual(response_data["ingangsdatumLand"], "2013-04-19")
        self.assertEqual(response_data["einddatumLand"], "9999-12-31")

    def test_putland(self):
        factories.LandFactory.create(
            landcode="BFA",
            landnaam="Boven-Volta",
            ingangsdatum_land="1966-01-03",
            einddatum_land="9999-12-31",
        )

        data = {
            "landcode": "BFA",
            "landnaam": "Burkina Faso",
            "ingangsdatumLand": "2014-11-03",
            "einddatumLand": "9999-12-31",
        }

        url = reverse("referentielijsten:land-detail", kwargs={"landcode": "BFA"})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["landcode"], "BFA")
        self.assertEqual(response_data["landnaam"], "Burkina Faso")
        self.assertEqual(response_data["ingangsdatumLand"], "2014-11-03")
        self.assertEqual(response_data["einddatumLand"], "9999-12-31")
