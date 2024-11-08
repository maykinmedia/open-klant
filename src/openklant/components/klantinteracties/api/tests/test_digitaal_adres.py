from django.test import tag
from django.utils.translation import gettext as _

from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models import DigitaalAdres
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class DigitaalAdresTests(APITestCase):
    def test_list_digitaal_adres(self):
        list_url = reverse("klantinteracties:digitaaladres-list")
        DigitaalAdresFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_list_pagination_pagesize_param(self):
        list_url = reverse("klantinteracties:digitaaladres-list")
        DigitaalAdresFactory.create_batch(10)

        response = self.client.get(list_url, {"pageSize": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 10)
        self.assertEqual(len(data["results"]), 5)
        self.assertEqual(data["next"], f"http://testserver{list_url}?page=2&pageSize=5")

    def test_read_digitaal_adres(self):
        digitaal_adres = DigitaalAdresFactory.create()
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_digitaal_adres(self):
        list_url = reverse("klantinteracties:digitaaladres-list")
        data = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": None,
            "soortDigitaalAdres": SoortDigitaalAdres.email,
            "adres": "foobar@example.com",
            "omschrijving": "omschrijving",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertIsNone(data["verstrektDoorBetrokkene"])
        self.assertEqual(data["soortDigitaalAdres"], SoortDigitaalAdres.email)
        self.assertEqual(data["verstrektDoorPartij"], None)
        self.assertEqual(data["adres"], "foobar@example.com")
        self.assertEqual(data["omschrijving"], "omschrijving")
        self.assertEqual(data["isStandaardAdres"], False)

        with self.subTest("with_betrokkene_and_partij"):
            partij = PartijFactory.create()
            betrokkene = BetrokkeneFactory.create()
            data["verstrektDoorBetrokkene"] = {"uuid": str(betrokkene.uuid)}
            data["verstrektDoorPartij"] = {"uuid": str(partij.uuid)}

            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            data = response.json()

            self.assertEqual(
                data["verstrektDoorBetrokkene"]["uuid"], str(betrokkene.uuid)
            )
            self.assertEqual(data["verstrektDoorPartij"]["uuid"], str(partij.uuid))
            self.assertEqual(data["soortDigitaalAdres"], SoortDigitaalAdres.email)
            self.assertEqual(data["adres"], "foobar@example.com")
            self.assertEqual(data["omschrijving"], "omschrijving")

    @tag("gh-234")
    def test_create_digitaal_adres_email_validation(self):
        list_url = reverse("klantinteracties:digitaaladres-list")
        data = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": None,
            "soortDigitaalAdres": SoortDigitaalAdres.email,
            "adres": "invalid",
            "omschrijving": "omschrijving",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "adres",
                    "code": "invalid",
                    "reason": _("Voer een geldig e-mailadres in."),
                }
            ],
        )

        digitaal_adres = DigitaalAdresFactory.create(
            soort_digitaal_adres=SoortDigitaalAdres.email, adres="foo@bar.com"
        )
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )

        response = self.client.patch(detail_url, {"adres": "invalid"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "adres",
                    "code": "invalid",
                    "reason": _("Voer een geldig e-mailadres in."),
                }
            ],
        )

        with self.subTest("no validation applied if soort is not email"):
            response = self.client.patch(
                detail_url,
                {
                    "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
                    "adres": "0612345678",
                },
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            digitaal_adres.refresh_from_db()

            self.assertEqual(
                digitaal_adres.soort_digitaal_adres, SoortDigitaalAdres.telefoonnummer
            )
            self.assertEqual(digitaal_adres.adres, "0612345678")

    def test_create_digitaal_adres_is_standaard_adres(self):
        """
        Creating a DigitaalAdres with isStandaardAdres=True should make other existing
        DigitaalAdressen no longer the default
        """
        # Since this has a different Partij, the value of `is_standaard_adres` should stay `True`
        partij1, partij2 = PartijFactory.create_batch(2)
        existing_adres_different_partij = DigitaalAdresFactory.create(
            partij=partij1, is_standaard_adres=True, soort_digitaal_adres="email"
        )
        # This adres has the same `soort_digitaal_adres` and `partij`, so the value of
        # `is_standaard_adres` should be changed to `False` if we change another one to `True`
        existing_adres = DigitaalAdresFactory.create(
            is_standaard_adres=True, soort_digitaal_adres="email", partij=partij2
        )

        list_url = reverse("klantinteracties:digitaaladres-list")
        data = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": {"uuid": str(partij2.uuid)},
            "soortDigitaalAdres": "email",
            "adres": "foo@bar.com",
            "omschrijving": "omschrijving",
            "isStandaardAdres": True,
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["isStandaardAdres"], True)

        existing_adres_different_partij.refresh_from_db()
        existing_adres.refresh_from_db()
        new_adres = DigitaalAdres.objects.last()

        self.assertEqual(existing_adres_different_partij.is_standaard_adres, True)
        self.assertEqual(existing_adres.is_standaard_adres, False)
        self.assertEqual(new_adres.is_standaard_adres, True)

    def test_update_digitaal_adres(self):
        betrokkene, betrokkene2 = BetrokkeneFactory.create_batch(2)
        partij, partij2 = PartijFactory.create_batch(2)
        digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=betrokkene,
            partij=partij2,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="foobar@example.com",
            omschrijving="omschrijving",
        )
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["verstrektDoorBetrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["verstrektDoorPartij"]["uuid"], str(partij2.uuid))
        self.assertEqual(data["soortDigitaalAdres"], SoortDigitaalAdres.email)
        self.assertEqual(data["adres"], "foobar@example.com")
        self.assertEqual(data["omschrijving"], "omschrijving")

        data = {
            "verstrektDoorBetrokkene": {"uuid": str(betrokkene2.uuid)},
            "verstrektDoorPartij": {"uuid": str(partij.uuid)},
            "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
            "adres": "0721434543",
            "omschrijving": "changed",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["verstrektDoorBetrokkene"]["uuid"], str(betrokkene2.uuid))
        self.assertEqual(data["verstrektDoorPartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["soortDigitaalAdres"], SoortDigitaalAdres.telefoonnummer)
        self.assertEqual(data["adres"], "0721434543")
        self.assertEqual(data["omschrijving"], "changed")

        with self.subTest("update_betrokkene_partij_to_none"):
            data = {
                "verstrektDoorBetrokkene": None,
                "verstrektDoorPartij": None,
                "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
                "adres": "0721434543",
                "omschrijving": "changed",
            }

            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertIsNone(data["verstrektDoorBetrokkene"])
            self.assertIsNone(data["verstrektDoorPartij"])
            self.assertEqual(
                data["soortDigitaalAdres"], SoortDigitaalAdres.telefoonnummer
            )
            self.assertEqual(data["adres"], "0721434543")
            self.assertEqual(data["omschrijving"], "changed")

    def test_update_digitaal_adres_is_standaard_adres(self):
        """
        Creating a DigitaalAdres with isStandaardAdres=True should make other existing
        DigitaalAdressen no longer the default
        """
        partij1, partij2 = PartijFactory.create_batch(2)
        # Since this has a different Partij, the value of `is_standaard_adres` should stay `True`
        existing_adres_different_partij = DigitaalAdresFactory.create(
            partij=partij1, is_standaard_adres=True, soort_digitaal_adres="email"
        )
        # This adres has the same `soort_digitaal_adres` and `partij`, so the value of
        # `is_standaard_adres` should be changed to `False` if we change another one to `True`
        existing_adres = DigitaalAdresFactory.create(
            is_standaard_adres=True, soort_digitaal_adres="email", partij=partij2
        )
        digitaal_adres = DigitaalAdresFactory.create(
            partij=partij2,
            soort_digitaal_adres="email",
            adres="adres",
            omschrijving="omschrijving",
        )
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )

        data = {
            "verstrektDoorBetrokkene": {"uuid": str(digitaal_adres.betrokkene.uuid)},
            "verstrektDoorPartij": {"uuid": str(partij2.uuid)},
            "soortDigitaalAdres": "email",
            "isStandaardAdres": True,
            "adres": "foo@bar.com",
            "omschrijving": "changed",
        }

        response = self.client.put(detail_url, data)

        data = response.json()

        self.assertEqual(data["isStandaardAdres"], True)

        existing_adres_different_partij.refresh_from_db()
        existing_adres.refresh_from_db()
        digitaal_adres.refresh_from_db()

        self.assertEqual(existing_adres_different_partij.is_standaard_adres, True)
        self.assertEqual(existing_adres.is_standaard_adres, False)
        self.assertEqual(digitaal_adres.is_standaard_adres, True)

    def test_partial_update_digitaal_adres(self):
        betrokkene = BetrokkeneFactory.create()
        partij = PartijFactory.create()
        digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=betrokkene,
            partij=partij,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="foobar@example.com",
            omschrijving="omschrijving",
        )
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["verstrektDoorBetrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["verstrektDoorPartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["soortDigitaalAdres"], SoortDigitaalAdres.email)
        self.assertEqual(data["adres"], "foobar@example.com")
        self.assertEqual(data["omschrijving"], "omschrijving")

        data = {
            "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
            "adres": "0721434543",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["verstrektDoorBetrokkene"]["uuid"], str(betrokkene.uuid))
        self.assertEqual(data["verstrektDoorPartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["soortDigitaalAdres"], SoortDigitaalAdres.telefoonnummer)
        self.assertEqual(data["adres"], "0721434543")
        self.assertEqual(data["omschrijving"], "omschrijving")

    def test_destroy_digitaal_adres(self):
        digitaal_adres = DigitaalAdresFactory.create()
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:digitaaladres-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
