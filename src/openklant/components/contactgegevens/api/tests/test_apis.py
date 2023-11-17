from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from openklant.components.contactgegevens.api.tests.factories import (
    ContactgegevensFactory,
    OrganisatieFactory,
    PersoonFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijIdentificatorFactory,
)


class ContactgegevensTests(JWTAuthMixin, APITestCase):
    def test_list_contactgegevens(self):
        list_url = reverse("contactgegevens:contactgegevens-list")
        ContactgegevensFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_contactgegevens(self):
        contactgegevens = ContactgegevensFactory.create()
        detail_url = reverse(
            "contactgegevens:contactgegevens-detail",
            kwargs={"id": str(contactgegevens.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_contactgegevens_with_organisatie_and_persoon(self):
        contactgegevens = ContactgegevensFactory.create()
        organsiatie = OrganisatieFactory.create(contactgegevens=contactgegevens)
        persoon = PersoonFactory.create(contactgegevens=contactgegevens)

        detail_url = reverse(
            "contactgegevens:contactgegevens-detail",
            kwargs={"id": str(contactgegevens.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["organisaties"][0]["id"], organsiatie.id)
        self.assertEqual(data["personen"][0]["id"], persoon.id)

    def test_create_contactgegevens(self):
        list_url = reverse("contactgegevens:contactgegevens-list")
        partij_identificator = PartijIdentificatorFactory.create()
        partij_identificator_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        data = {"partijIdentificator": f"http://testserver{partij_identificator_url}"}

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(
            data["partijIdentificator"],
            f"http://testserver/klantinteracties/api/v1/partij_identificator/{str(partij_identificator.uuid)}",
        )

    def test_update_contactgegevens(self):
        (
            partij_identificator,
            partij_identificator2,
        ) = PartijIdentificatorFactory.create_batch(2)
        partij_identificator_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        partij_identificator_url2 = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator2.uuid)},
        )

        contactgegevens = ContactgegevensFactory.create(
            partij_identificator=partij_identificator,
        )

        detail_url = reverse(
            "contactgegevens:contactgegevens-detail",
            kwargs={"id": str(contactgegevens.id)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["partijIdentificator"],
            f"http://testserver/klantinteracties/api/v1/partij_identificator/{str(partij_identificator.uuid)}",
        )

        data = {"partijIdentificator": f"http://testserver{partij_identificator_url2}"}

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(
            data["partijIdentificator"],
            f"http://testserver/klantinteracties/api/v1/partij_identificator/{str(partij_identificator2.uuid)}",
        )

    def test_destroy_contactgegevens(self):
        contactgegevens = ContactgegevensFactory.create()
        detail_url = reverse(
            "contactgegevens:contactgegevens-detail",
            kwargs={"id": str(contactgegevens.id)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("contactgegevens:contactgegevens-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class PersoonTests(JWTAuthMixin, APITestCase):
    def test_create_persoon(self):
        list_url = reverse("contactgegevens:persoon-list")
        contactgegevens = ContactgegevensFactory.create()

        data = {
            "contactgegevens": {"id": str(contactgegevens.id)},
            "geboortedatum": "1972-05-05",
            "geslachtsnaam": "Townsend",
            "geslacht": "m",
            "voornamen": "Devin",
            "adres": {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
            "land": {"code": "Canada"},
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["contactgegevens"]["id"], contactgegevens.id)
        self.assertEqual(data["geboortedatum"], "1972-05-05")
        self.assertEqual(data["overlijdensdatum"], None)
        self.assertEqual(data["geslachtsnaam"], "Townsend")
        self.assertEqual(data["geslacht"], "m")
        self.assertEqual(data["voorvoegsel"], "")
        self.assertEqual(data["voornamen"], "Devin")
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], {"code": "Canada"})

    def test_update_persoon(self):
        contactgegevens, contactgegevens2 = ContactgegevensFactory.create_batch(2)
        persoon = PersoonFactory(
            contactgegevens=contactgegevens,
            geboortedatum="1972-05-05",
            overlijdensdatum=None,
            geslachtsnaam="Townsend",
            geslacht="m",
            voorvoegsel="",
            voornamen="Devin",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="5001",
            land_code="Canada",
        )
        detail_url = reverse(
            "contactgegevens:persoon-detail",
            kwargs={"id": str(persoon.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["contactgegevens"]["id"], contactgegevens.id)
        self.assertEqual(data["geboortedatum"], "1972-05-05")
        self.assertEqual(data["overlijdensdatum"], None)
        self.assertEqual(data["geslachtsnaam"], "Townsend")
        self.assertEqual(data["geslacht"], "m")
        self.assertEqual(data["voorvoegsel"], "")
        self.assertEqual(data["voornamen"], "Devin")
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], {"code": "Canada"})

        data = {
            "contactgegevens": {"id": str(contactgegevens2.id)},
            "geboortedatum": "1972-05-06",
            "overlijdensdatum": "2023-11-22",
            "geslachtsnaam": "changed",
            "geslacht": "v",
            "voorvoegsel": "changed",
            "voornamen": "changed",
            "adres": {
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "6713",
            },
            "land": {"code": "changed"},
        }
        response = self.client.put(detail_url, data)
        data = response.json()
        self.assertEqual(data["contactgegevens"]["id"], contactgegevens2.id)
        self.assertEqual(data["geboortedatum"], "1972-05-06")
        self.assertEqual(data["overlijdensdatum"], "2023-11-22")
        self.assertEqual(data["geslachtsnaam"], "changed")
        self.assertEqual(data["geslacht"], "v")
        self.assertEqual(data["voorvoegsel"], "changed")
        self.assertEqual(data["voornamen"], "changed")
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "6713",
            },
        )
        self.assertEqual(data["land"], {"code": "changed"})

    def test_update_partial_persoon(self):
        contactgegevens = ContactgegevensFactory.create()
        persoon = PersoonFactory(
            contactgegevens=contactgegevens,
            geboortedatum="1972-05-05",
            overlijdensdatum=None,
            geslachtsnaam="Townsend",
            geslacht="m",
            voorvoegsel="",
            voornamen="Devin",
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="5001",
            land_code="Canada",
        )
        detail_url = reverse(
            "contactgegevens:persoon-detail",
            kwargs={"id": str(persoon.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["contactgegevens"]["id"], contactgegevens.id)
        self.assertEqual(data["geboortedatum"], "1972-05-05")
        self.assertEqual(data["overlijdensdatum"], None)
        self.assertEqual(data["geslachtsnaam"], "Townsend")
        self.assertEqual(data["geslacht"], "m")
        self.assertEqual(data["voorvoegsel"], "")
        self.assertEqual(data["voornamen"], "Devin")
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], {"code": "Canada"})

        data = {
            "overlijdensdatum": "2023-11-22",
        }

        response = self.client.patch(detail_url, data)
        data = response.json()
        self.assertEqual(data["contactgegevens"]["id"], contactgegevens.id)
        self.assertEqual(data["geboortedatum"], "1972-05-05")
        self.assertEqual(data["overlijdensdatum"], "2023-11-22")
        self.assertEqual(data["geslachtsnaam"], "Townsend")
        self.assertEqual(data["geslacht"], "m")
        self.assertEqual(data["voorvoegsel"], "")
        self.assertEqual(data["voornamen"], "Devin")
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], {"code": "Canada"})


class OrganisatiesTests(JWTAuthMixin, APITestCase):
    def test_create_organisatie(self):
        list_url = reverse("contactgegevens:organisatie-list")
        contactgegevens = ContactgegevensFactory.create()

        data = {
            "contactgegevens": {"id": str(contactgegevens.id)},
            "handelsnaam": "Devin Townsend",
            "oprichtingsdatum": "1996-03-12",
            "adres": {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
            "land": {"code": "Canada"},
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["contactgegevens"]["id"], contactgegevens.id)
        self.assertEqual(data["handelsnaam"], "Devin Townsend")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-12")
        self.assertEqual(data["opheffingsdatum"], None)
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], {"code": "Canada"})

    def test_update_organisatie(self):
        contactgegevens, contactgegevens2 = ContactgegevensFactory.create_batch(2)
        organisatie = OrganisatieFactory(
            contactgegevens=contactgegevens,
            handelsnaam="Devin Townsend",
            oprichtingsdatum="1996-03-12",
            opheffingsdatum=None,
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="5001",
            land_code="Canada",
        )
        detail_url = reverse(
            "contactgegevens:organisatie-detail",
            kwargs={"id": str(organisatie.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["contactgegevens"]["id"], contactgegevens.id)
        self.assertEqual(data["handelsnaam"], "Devin Townsend")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-12")
        self.assertEqual(data["opheffingsdatum"], None)
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], {"code": "Canada"})

        data = {
            "contactgegevens": {"id": str(contactgegevens2.id)},
            "handelsnaam": "changed",
            "oprichtingsdatum": "1996-03-13",
            "opheffingsdatum": "2023-11-22",
            "adres": {
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "6713",
            },
            "land": {"code": "changed"},
        }
        response = self.client.put(detail_url, data)
        data = response.json()
        self.assertEqual(data["contactgegevens"]["id"], contactgegevens2.id)
        self.assertEqual(data["handelsnaam"], "changed")
        self.assertEqual(data["opheffingsdatum"], "2023-11-22")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-13")
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "6713",
            },
        )
        self.assertEqual(data["land"], {"code": "changed"})

    def test_update_partial_organisatie(self):
        contactgegevens = ContactgegevensFactory.create()
        organisatie = OrganisatieFactory(
            contactgegevens=contactgegevens,
            handelsnaam="Devin Townsend",
            oprichtingsdatum="1996-03-12",
            opheffingsdatum=None,
            adres_adresregel1="adresregel1",
            adres_adresregel2="adresregel2",
            adres_adresregel3="adresregel3",
            adres_land="5001",
            land_code="Canada",
        )
        detail_url = reverse(
            "contactgegevens:organisatie-detail",
            kwargs={"id": str(organisatie.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["contactgegevens"]["id"], contactgegevens.id)
        self.assertEqual(data["handelsnaam"], "Devin Townsend")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-12")
        self.assertEqual(data["opheffingsdatum"], None)
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], {"code": "Canada"})

        data = {
            "opheffingsdatum": "2023-11-22",
        }

        response = self.client.patch(detail_url, data)
        data = response.json()

        self.assertEqual(data["contactgegevens"]["id"], contactgegevens.id)
        self.assertEqual(data["handelsnaam"], "Devin Townsend")
        self.assertEqual(data["oprichtingsdatum"], "1996-03-12")
        self.assertEqual(data["opheffingsdatum"], "2023-11-22")
        self.assertEqual(
            data["adres"],
            {
                "adresregel1": "adresregel1",
                "adresregel2": "adresregel2",
                "adresregel3": "adresregel3",
                "land": "5001",
            },
        )
        self.assertEqual(data["land"], {"code": "Canada"})
