import datetime

from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories.partijen import (
    CategorieFactory,
    CategorieRelatieFactory,
    PartijFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class CategorieRelatieTests(APITestCase):
    def test_list_categorie_relatie(self):
        list_url = reverse("klantinteracties:categorierelatie-list")
        CategorieRelatieFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_categorie_relatie(self):
        categorie_relatie = CategorieRelatieFactory.create()
        detail_url = reverse(
            "klantinteracties:categorierelatie-detail",
            kwargs={"uuid": str(categorie_relatie.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create_categorie_relatie(self):
        list_url = reverse("klantinteracties:categorierelatie-list")
        partij = PartijFactory.create()
        categorie = CategorieFactory.create(naam="naam")
        data = {
            "partij": {"uuid": str(partij.uuid)},
            "categorie": {"uuid": str(categorie.uuid)},
            "beginDatum": "2024-01-11",
            "eindDatum": "2024-01-12",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["categorie"]["uuid"], str(categorie.uuid))
        self.assertEqual(data["categorie"]["naam"], "naam")
        self.assertEqual(data["beginDatum"], "2024-01-11")
        self.assertEqual(data["eindDatum"], "2024-01-12")

        with self.subTest("fill_begin_datum_when_empty_with_todays_date"):
            today = datetime.datetime.today().strftime("%Y-%m-%d")
            data["beginDatum"] = None

            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            data = response.json()

            self.assertEqual(data["beginDatum"], today)

    def test_update_categorie_relatie(self):
        partij, partij2 = PartijFactory.create_batch(2)
        categorie, categorie2 = CategorieFactory.create_batch(2)
        categorie_relatie = CategorieRelatieFactory.create(
            partij=partij,
            categorie=categorie,
            begin_datum="2024-01-11",
            eind_datum=None,
        )
        detail_url = reverse(
            "klantinteracties:categorierelatie-detail",
            kwargs={"uuid": str(categorie_relatie.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["categorie"]["uuid"], str(categorie.uuid))
        self.assertEqual(data["categorie"]["naam"], categorie.naam)
        self.assertEqual(data["beginDatum"], "2024-01-11")
        self.assertEqual(data["eindDatum"], None)

        data = {
            "partij": {"uuid": str(partij2.uuid)},
            "categorie": {"uuid": str(categorie2.uuid)},
            "beginDatum": "2024-01-12",
            "eindDatum": "2024-01-14",
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij2.uuid))
        self.assertEqual(data["categorie"]["uuid"], str(categorie2.uuid))
        self.assertEqual(data["categorie"]["naam"], categorie2.naam)
        self.assertEqual(data["beginDatum"], "2024-01-12")
        self.assertEqual(data["eindDatum"], "2024-01-14")

    def test_update_partial_categorie_relatie(self):
        partij = PartijFactory.create()
        categorie = CategorieFactory.create(naam="naam")
        categorie_relatie = CategorieRelatieFactory.create(
            partij=partij,
            categorie=categorie,
            begin_datum="2024-01-11",
            eind_datum=None,
        )
        detail_url = reverse(
            "klantinteracties:categorierelatie-detail",
            kwargs={"uuid": str(categorie_relatie.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["categorie"]["uuid"], str(categorie.uuid))
        self.assertEqual(data["categorie"]["naam"], categorie.naam)
        self.assertEqual(data["beginDatum"], "2024-01-11")
        self.assertEqual(data["eindDatum"], None)

        data = {
            "eindDatum": "2024-01-14",
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["partij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["categorie"]["uuid"], str(categorie.uuid))
        self.assertEqual(data["categorie"]["naam"], "naam")
        self.assertEqual(data["beginDatum"], "2024-01-11")
        self.assertEqual(data["eindDatum"], "2024-01-14")

    def test_destroy_categorie_relatie(self):
        categorie_relatie = CategorieRelatieFactory.create()
        detail_url = reverse(
            "klantinteracties:categorierelatie-detail",
            kwargs={"uuid": str(categorie_relatie.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:categorierelatie-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class CategorieTests(APITestCase):
    def test_list_categorie(self):
        list_url = reverse("klantinteracties:categorie-list")
        CategorieFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_categorie(self):
        partij_identificator = CategorieFactory.create()
        detail_url = reverse(
            "klantinteracties:categorie-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create_categorie(self):
        list_url = reverse("klantinteracties:categorie-list")
        data = {
            "naam": "naam",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["naam"], "naam")

    def test_update_categorie(self):
        categorie = CategorieFactory.create(naam="naam")

        detail_url = reverse(
            "klantinteracties:categorie-detail",
            kwargs={"uuid": str(categorie.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["naam"], "naam")

        data = {
            "naam": "changed",
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["naam"], "changed")

    def test_partial_update_categorie(self):
        categorie = CategorieFactory.create(
            naam="naam",
        )

        detail_url = reverse(
            "klantinteracties:categorie-detail",
            kwargs={"uuid": str(categorie.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["naam"], "naam")

        data = {"naam": "changed"}
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["naam"], "changed")

    def test_destroy_categorie(self):
        categorie = CategorieFactory.create()
        detail_url = reverse(
            "klantinteracties:categorie-detail",
            kwargs={"uuid": str(categorie.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:categorie-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
