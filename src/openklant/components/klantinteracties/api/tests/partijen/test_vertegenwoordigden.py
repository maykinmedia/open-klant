from rest_framework import status
from vng_api_common.tests import get_validation_errors, reverse

from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijFactory,
    VertegenwoordigdenFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class VertegenwoordigdenTests(APITestCase):
    def test_list_vertegenwoordigden(self):
        list_url = reverse("klantinteracties:vertegenwoordigden-list")
        VertegenwoordigdenFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_vertegenwoordigden(self):
        vertegenwoordigden = VertegenwoordigdenFactory.create()
        detail_url = reverse(
            "klantinteracties:vertegenwoordigden-detail",
            kwargs={"uuid": str(vertegenwoordigden.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create_vertegenwoordigden(self):
        list_url = reverse("klantinteracties:vertegenwoordigden-list")
        partij, partij2 = PartijFactory.create_batch(2)
        data = {
            "vertegenwoordigendePartij": {"uuid": str(partij.uuid)},
            "vertegenwoordigdePartij": {"uuid": str(partij2.uuid)},
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["vertegenwoordigendePartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["vertegenwoordigdePartij"]["uuid"], str(partij2.uuid))

        with self.subTest("test_unique_together"):
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "nonFieldErrors")
            self.assertEqual(error["code"], "unique")
            self.assertEqual(
                error["reason"],
                "De velden vertegenwoordigende_partij, vertegenwoordigde_partij moeten een unieke set zijn.",
            )

        with self.subTest("test_partij_can_not_vertegenwoordig_it_self"):
            data = {
                "vertegenwoordigendePartij": {"uuid": str(partij.uuid)},
                "vertegenwoordigdePartij": {"uuid": str(partij.uuid)},
            }
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "vertegenwoordigdePartij")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "De partij kan niet zichzelf vertegenwoordigen.",
            )

    def test_update_vertegenwoordigden(self):
        partij, partij2, partij3, partij4 = PartijFactory.create_batch(4)
        vertegenwoordigden = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij,
            vertegenwoordigde_partij=partij2,
        )
        detail_url = reverse(
            "klantinteracties:vertegenwoordigden-detail",
            kwargs={"uuid": str(vertegenwoordigden.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["vertegenwoordigendePartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["vertegenwoordigdePartij"]["uuid"], str(partij2.uuid))

        data = {
            "vertegenwoordigendePartij": {"uuid": str(partij3.uuid)},
            "vertegenwoordigdePartij": {"uuid": str(partij4.uuid)},
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["vertegenwoordigendePartij"]["uuid"], str(partij3.uuid))
        self.assertEqual(data["vertegenwoordigdePartij"]["uuid"], str(partij4.uuid))

    def test_update_partial_vertegenwoordigden(self):
        partij, partij2, partij3 = PartijFactory.create_batch(3)
        vertegenwoordigden = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij,
            vertegenwoordigde_partij=partij2,
        )
        detail_url = reverse(
            "klantinteracties:vertegenwoordigden-detail",
            kwargs={"uuid": str(vertegenwoordigden.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["vertegenwoordigendePartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["vertegenwoordigdePartij"]["uuid"], str(partij2.uuid))

        data = {
            "vertegenwoordigendePartij": {"uuid": str(partij3.uuid)},
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["vertegenwoordigendePartij"]["uuid"], str(partij3.uuid))
        self.assertEqual(data["vertegenwoordigdePartij"]["uuid"], str(partij2.uuid))

        with self.subTest("test_partij_can_not_vertegenwoordig_it_self"):
            data = {
                "vertegenwoordigendePartij": {"uuid": str(partij2.uuid)},
            }
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "vertegenwoordigdePartij")
            self.assertEqual(error["code"], "invalid")
            self.assertEqual(
                error["reason"],
                "De partij kan niet zichzelf vertegenwoordigen.",
            )

        with self.subTest("test_unique_together"):
            vertegenwoordigden = VertegenwoordigdenFactory.create(
                vertegenwoordigende_partij=partij,
                vertegenwoordigde_partij=partij2,
            )
            detail_url = reverse(
                "klantinteracties:vertegenwoordigden-detail",
                kwargs={"uuid": str(vertegenwoordigden.uuid)},
            )
            data = {
                "vertegenwoordigendePartij": {"uuid": str(partij3.uuid)},
            }

            # update new vertegenwoordigde object to have same data as the existing one.
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "nonFieldErrors")
            self.assertEqual(error["code"], "unique")
            self.assertEqual(
                error["reason"],
                "De velden vertegenwoordigende_partij, vertegenwoordigde_partij moeten een unieke set zijn.",
            )

    def test_destroy_vertegenwoordigden(self):
        vertegenwoordigden = VertegenwoordigdenFactory.create()
        detail_url = reverse(
            "klantinteracties:vertegenwoordigden-detail",
            kwargs={"uuid": str(vertegenwoordigden.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:vertegenwoordigden-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
