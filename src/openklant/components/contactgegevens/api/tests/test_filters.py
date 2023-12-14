from uuid import uuid4

from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.contactgegevens.api.tests.factories import (
    ContactgegevensFactory,
    OrganisatieFactory,
    PersoonFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class OrganisatieFilterTests(APITestCase):
    url = reverse("contactgegevens:organisatie-list")

    def setUp(self):
        super().setUp()
        (
            contactgegevens,
            contactgegevens2,
            contactgegevens3,
            contactgegevens4,
            self.contactgegevens5,
        ) = ContactgegevensFactory.create_batch(5)
        for obj in [
            contactgegevens,
            contactgegevens2,
            contactgegevens3,
            contactgegevens4,
            self.contactgegevens5,
        ]:
            self.organisatie = OrganisatieFactory.create(contactgegevens=obj)

    def test_filter_contactgegevens_id(self):
        response = self.client.get(
            self.url, {"contactgegevens__uuid": f"{self.contactgegevens5.uuid}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(self.organisatie.uuid, data[0]["uuid"])

        with self.subTest("no_matches_found_return_empty_query"):
            response = self.client.get(
                self.url, {"contactgegevens__uuid": str(uuid4())}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"contactgegevens__uuid": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_contactgegevens_url(self):
        url = f"http://testserver/contactgegevens/api/v1/contactgegevens/{str(self.contactgegevens5.uuid)}"
        response = self.client.get(
            self.url,
            {"contactgegevens__url": url},
        )
        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(self.organisatie.uuid, data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "contactgegevens__url": f"http://testserver/klantinteracties/api/v1/contactgegevens/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"contactgegevens__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class PersoonFilterTests(APITestCase):
    url = reverse("contactgegevens:persoon-list")

    def setUp(self):
        super().setUp()
        (
            contactgegevens,
            contactgegevens2,
            contactgegevens3,
            contactgegevens4,
            self.contactgegevens5,
        ) = ContactgegevensFactory.create_batch(5)
        for obj in [
            contactgegevens,
            contactgegevens2,
            contactgegevens3,
            contactgegevens4,
            self.contactgegevens5,
        ]:
            self.persoon = PersoonFactory.create(contactgegevens=obj)

    def test_filter_contactgegevens_id(self):
        response = self.client.get(
            self.url, {"contactgegevens__uuid": f"{self.contactgegevens5.uuid}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(self.persoon.uuid, data[0]["uuid"])

        with self.subTest("no_matches_found_return_empty_query"):
            response = self.client.get(
                self.url, {"contactgegevens__uuid": str(uuid4())}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"contactgegevens__uuid": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_contactgegevens_url(self):
        url = f"http://testserver/contactgegevens/api/v1/contactgegevens/{str(self.contactgegevens5.uuid)}"
        response = self.client.get(
            self.url,
            {"contactgegevens__url": url},
        )
        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(self.persoon.uuid, data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "contactgegevens__url": f"http://testserver/klantinteracties/api/v1/contactgegevens/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"contactgegevens__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)
