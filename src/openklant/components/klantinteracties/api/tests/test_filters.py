from uuid import uuid4

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
    KlantcontactFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijFactory,
)


class KlantcontactFilterTests(JWTAuthMixin, APITestCase):
    url = reverse("klantinteracties:klantcontact-list")

    def setUp(self):
        super().setUp()
        (
            klantcontact,
            klantcontact2,
            klantcontact3,
            klantcontact4,
            self.klantcontact5,
        ) = KlantcontactFactory.create_batch(5)
        for betrokkene_klantcontact in [
            klantcontact,
            klantcontact2,
            klantcontact3,
            klantcontact4,
            self.klantcontact5,
        ]:
            self.betrokkene = BetrokkeneFactory.create(
                klantcontact=betrokkene_klantcontact
            )

    def test_filter_betrokkene_uuid(self):
        response = self.client.get(
            self.url, {"had_betrokkene__uuid": f"{self.betrokkene.uuid}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_empty_query"):
            response = self.client.get(self.url, {"had_betrokkene__uuid": str(uuid4())})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"had_betrokkene__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_betrokkene_url(self):
        response = self.client.get(
            self.url,
            {
                "had_betrokkene__url": f"http://testserver/klantinteracties/api/v1/klantcontact/{self.betrokkene.uuid}"
            },
        )
        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "had_betrokkene__url": f"http://testserver/klantinteracties/api/v1/klantcontact/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"had_betrokkene__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class BetrokkeneFilterTests(JWTAuthMixin, APITestCase):
    url = reverse("klantinteracties:betrokkene-list")

    def setUp(self):
        super().setUp()

        self.klantcontact = KlantcontactFactory.create(nummer="6237172371")
        self.betrokkene = BetrokkeneFactory.create(klantcontact=self.klantcontact)
        self.digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=self.betrokkene, adres="search_param_adres"
        )
        self.partij = PartijFactory.create(
            betrokkene=self.betrokkene, nummer="8123973457"
        )

        (
            betrokkene2,
            betrokkene3,
            betrokkene4,
            betrokkene5,
        ) = BetrokkeneFactory.create_batch(4)

        DigitaalAdresFactory.create(betrokkene=betrokkene2)
        PartijFactory.create(betrokkene=betrokkene2)

        DigitaalAdresFactory.create(betrokkene=betrokkene3)
        PartijFactory.create(betrokkene=betrokkene3)

        DigitaalAdresFactory.create(betrokkene=betrokkene4)
        PartijFactory.create(betrokkene=betrokkene4)

        DigitaalAdresFactory.create(betrokkene=betrokkene5)
        PartijFactory.create(betrokkene=betrokkene5)

    def test_filter_klantcontact_url(self):
        response = self.client.get(
            self.url,
            {
                "klantcontact__url": f"http://testserver/klantinteracties/api/v1/klantcontact/{self.klantcontact.uuid}"
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "klantcontact__url": f"http://testserver/klantinteracties/api/v1/klantcontact/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"klantcontact__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_klantcontact_uuid(self):
        response = self.client.get(
            self.url,
            {"klantcontact__uuid": str(self.klantcontact.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"klantcontact__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"klantcontact__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_klantcontact_nummer(self):
        response = self.client.get(
            self.url,
            {"klantcontact__nummer": str(6237172371)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"klantcontact__nummer": "8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrektedigitaal_adres_url(self):
        digitaal_adres_url = f"http://testserver/klantinteracties/api/v1/digitaal_adres/{self.digitaal_adres.uuid}"
        response = self.client.get(
            self.url,
            {"verstrektedigitaal_adres__url": digitaal_adres_url},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            none_existing_url = f"http://testserver/klantinteracties/api/v1/digitaal_adres/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"verstrektedigitaal_adres__url": none_existing_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"verstrektedigitaal_adres__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrektedigitaal_adres_uuid(self):
        response = self.client.get(
            self.url,
            {"verstrektedigitaal_adres__uuid": str(self.digitaal_adres.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"verstrektedigitaal_adres__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"verstrektedigitaal_adres__uuid": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrektedigitaal_adres_adres(self):
        response = self.client.get(
            self.url,
            {"verstrektedigitaal_adres__adres": "search_param_adres"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"verstrektedigitaal_adres__adres": "none_existing_adres"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_url(self):
        response = self.client.get(
            self.url,
            {
                "was_partij__url": f"http://testserver/klantinteracties/api/v1/partij/{self.partij.uuid}"
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "was_partij__url": f"http://testserver/klantinteracties/api/v1/partij/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"was_partij__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_uuid(self):
        response = self.client.get(
            self.url,
            {"was_partij__uuid": str(self.partij.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"was_partij__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"was_partij__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_nummer(self):
        response = self.client.get(
            self.url,
            {"was_partij__nummer": "8123973457"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"was_partij__nummer": "2348238482"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)
