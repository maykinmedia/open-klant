from django.test import tag
from django.utils.translation import gettext as _

from rest_framework import status
from vng_api_common.tests import get_validation_errors, reverse

from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models import DigitaalAdres
from openklant.components.klantinteracties.models.tests.factories import (
    BetrokkeneFactory,
    DigitaalAdresFactory,
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
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create_only_required(self):
        response = self.client.post(reverse("klantinteracties:digitaaladres-list"), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "adres",
                    "code": "required",
                    "reason": "Dit veld is vereist.",
                },
                {
                    "name": "soortDigitaalAdres",
                    "code": "required",
                    "reason": "Dit veld is vereist.",
                },
            ],
        )

    def test_update_only_required(self):
        digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=BetrokkeneFactory.create(),
            partij=PartijFactory.create(),
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="foobar@example.com",
            omschrijving="omschrijving",
            referentie="referentie",
        )
        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )
        # PUT
        response = self.client.put(detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "adres",
                    "code": "required",
                    "reason": "Dit veld is vereist.",
                },
                {
                    "name": "soortDigitaalAdres",
                    "code": "required",
                    "reason": "Dit veld is vereist.",
                },
            ],
        )
        # PATCH
        response = self.client.patch(detail_url, {})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_digitaal_adres(self):
        list_url = reverse("klantinteracties:digitaaladres-list")
        data = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": None,
            "soortDigitaalAdres": SoortDigitaalAdres.email,
            "adres": "foobar@example.com",
            "omschrijving": "omschrijving",
            "referentie": "my-referentie",
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertIsNone(data["verstrektDoorBetrokkene"])
        self.assertEqual(data["soortDigitaalAdres"], SoortDigitaalAdres.email)
        self.assertEqual(data["verstrektDoorPartij"], None)
        self.assertEqual(data["adres"], "foobar@example.com")
        self.assertEqual(data["omschrijving"], "omschrijving")
        self.assertEqual(data["referentie"], "my-referentie")
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
            self.assertEqual(data["referentie"], "my-referentie")

    @tag("gh-234")
    def test_create_digitaal_adres_email_validation(self):
        list_url = reverse("klantinteracties:digitaaladres-list")

        with self.subTest("invalid email create"):
            data = {
                "verstrektDoorBetrokkene": None,
                "verstrektDoorPartij": None,
                "soortDigitaalAdres": SoortDigitaalAdres.email,
                "adres": "invalid",
                "omschrijving": "omschrijving",
                "referentie": "my-referentie",
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

        with self.subTest("invalid email update"):
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

    @tag("gh-234")
    def test_create_digitaal_adres_telefoon_validation(self):
        list_url = reverse("klantinteracties:digitaaladres-list")

        with self.subTest("create telefeoonnummer"):
            data = {
                "verstrektDoorBetrokkene": None,
                "verstrektDoorPartij": None,
                "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
                "adres": "invalid",
                "omschrijving": "omschrijving",
                "referentie": "my-referentie",
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
                        "reason": _("Het opgegeven telefoonnummer is ongeldig."),
                    }
                ],
            )

        with self.subTest("invalid telefoonnummer update"):
            digitaal_adres = DigitaalAdresFactory.create(
                soort_digitaal_adres=SoortDigitaalAdres.telefoonnummer, adres="+311234"
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
                        "reason": _("Het opgegeven telefoonnummer is ongeldig."),
                    }
                ],
            )

    @tag("gh-234")
    def test_create_digitaal_adres_overig_no_validation(self):
        list_url = reverse("klantinteracties:digitaaladres-list")

        with self.subTest(
            "no validation applied if soort is not email or telefoonnummer create"
        ):
            data = {
                "verstrektDoorBetrokkene": None,
                "verstrektDoorPartij": None,
                "soortDigitaalAdres": SoortDigitaalAdres.overig,
                "adres": "whatever",
                "omschrijving": "omschrijving",
                "referentie": "my-referentie",
            }

            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            response_data = response.json()

            self.assertEqual(
                response_data["soortDigitaalAdres"], SoortDigitaalAdres.overig
            )
            self.assertEqual(response_data["adres"], "whatever")

        with self.subTest(
            "no validation applied if soort is not email or telefoonnummer update"
        ):
            digitaal_adres = DigitaalAdresFactory.create(
                soort_digitaal_adres=SoortDigitaalAdres.overig, adres="overig"
            )
            detail_url = reverse(
                "klantinteracties:digitaaladres-detail",
                kwargs={"uuid": str(digitaal_adres.uuid)},
            )

            response = self.client.patch(
                detail_url,
                {
                    "soortDigitaalAdres": SoortDigitaalAdres.overig,
                    "adres": "whatever",
                },
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            digitaal_adres.refresh_from_db()

            self.assertEqual(
                digitaal_adres.soort_digitaal_adres, SoortDigitaalAdres.overig
            )
            self.assertEqual(digitaal_adres.adres, "whatever")

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
            "referentie": "my-referentie",
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

    def test_create_digitaal_adres_is_standaard_adres_without_partij_not_possible(self):
        """
        Creating a DigitaalAdres with isStandaardAdres=True should not be possible with
        verstrektDoorPartij=None
        """
        betrokkene = BetrokkeneFactory.create()

        list_url = reverse("klantinteracties:digitaaladres-list")
        data = {
            "verstrektDoorBetrokkene": {"uuid": str(betrokkene.uuid)},
            "verstrektDoorPartij": None,
            "soortDigitaalAdres": "email",
            "adres": "foo@bar.com",
            "omschrijving": "omschrijving",
            "referentie": "referentie",
            "isStandaardAdres": True,
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "isStandaardAdres",
                    "code": "invalid",
                    "reason": _(
                        "`is_standaard_adres` kan alleen gezet worden als `verstrekt_door_partij` niet leeg is."
                    ),
                }
            ],
        )
        self.assertEqual(DigitaalAdres.objects.count(), 0)

    def test_update_digitaal_adres(self):
        betrokkene, betrokkene2 = BetrokkeneFactory.create_batch(2)
        partij, partij2 = PartijFactory.create_batch(2)
        digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=betrokkene,
            partij=partij2,
            soort_digitaal_adres=SoortDigitaalAdres.email,
            adres="foobar@example.com",
            omschrijving="omschrijving",
            referentie="referentie",
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
        self.assertEqual(data["referentie"], "referentie")

        data = {
            "verstrektDoorBetrokkene": {"uuid": str(betrokkene2.uuid)},
            "verstrektDoorPartij": {"uuid": str(partij.uuid)},
            "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
            "adres": "0721434543",
            "omschrijving": "changed",
            "referentie": "new-referentie",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["verstrektDoorBetrokkene"]["uuid"], str(betrokkene2.uuid))
        self.assertEqual(data["verstrektDoorPartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["soortDigitaalAdres"], SoortDigitaalAdres.telefoonnummer)
        self.assertEqual(data["adres"], "0721434543")
        self.assertEqual(data["omschrijving"], "changed")
        self.assertEqual(data["referentie"], "new-referentie")

        with self.subTest("update_betrokkene_partij_to_none"):
            data = {
                "verstrektDoorBetrokkene": None,
                "verstrektDoorPartij": None,
                "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
                "adres": "0721434543",
                "omschrijving": "changed",
                "referentie": "new-referentie",
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
            self.assertEqual(data["referentie"], "new-referentie")

        with self.subTest("without specifying referentie"):
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
            # Verify that referentie is unchanged
            self.assertEqual(data["referentie"], "new-referentie")

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
            "referentie": "new-referentie",
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
            referentie="foo",
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
        # Verify that the referentie is unchanged
        self.assertEqual(data["referentie"], "foo")

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

    def test_create_digitaal_adres_referentie_empty_string(self):
        """
        Ensure that UniqueConstraint does not apply when `referentie` is an empty string.
        """
        partij = PartijFactory.create()
        list_url = reverse("klantinteracties:digitaaladres-list")
        data1 = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": {"uuid": str(partij.uuid)},
            "soortDigitaalAdres": SoortDigitaalAdres.email,
            "adres": "foobar@example.com",
            "omschrijving": "omschrijving",
            "referentie": "",  # Empty string referentie
        }
        data2 = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": {"uuid": str(partij.uuid)},
            "soortDigitaalAdres": SoortDigitaalAdres.email,
            "adres": "barfoo@example.com",
            "omschrijving": "another omschrijving",
            "referentie": "",  # Another empty string referentie
        }

        response1 = self.client.post(list_url, data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(list_url, data2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        response_data1 = response1.json()

        self.assertEqual(response_data1["adres"], "foobar@example.com")
        self.assertEqual(response_data1["referentie"], "")

        response_data2 = response2.json()

        self.assertEqual(response_data2["adres"], "barfoo@example.com")
        self.assertEqual(response_data2["referentie"], "")

    def test_create_digitaal_adres_verstrektDoorPartij_is_null(self):
        """
        Ensure that UniqueConstraint does not apply when `verstrektDoorPartij` is null.
        """
        list_url = reverse("klantinteracties:digitaaladres-list")
        data1 = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": None,
            "soortDigitaalAdres": SoortDigitaalAdres.email,
            "adres": "foobar@example.com",
            "omschrijving": "omschrijving",
            "referentie": "same-ref",
        }
        data2 = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": None,
            "soortDigitaalAdres": SoortDigitaalAdres.email,
            "adres": "barfoo@example.com",
            "omschrijving": "another omschrijving",
            "referentie": "same-ref",
        }

        response1 = self.client.post(list_url, data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(list_url, data2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        response_data1 = response1.json()

        self.assertEqual(response_data1["verstrektDoorPartij"], None)

        self.assertEqual(response_data1["adres"], "foobar@example.com")
        self.assertEqual(response_data1["referentie"], "same-ref")

        response_data2 = response2.json()

        self.assertEqual(response_data2["verstrektDoorPartij"], None)

        self.assertEqual(response_data2["adres"], "barfoo@example.com")
        self.assertEqual(response_data2["referentie"], "same-ref")

    def test_create_digitaal_adres_validate_uniqueness_if_both_verstrektDoorPartij_and_referentie_are_set(
        self,
    ):
        """
        Ensure that UniqueConstraint applies if both verstrektDoorPartij and referentie are set.
        """
        partij = PartijFactory.create(voorkeurs_digitaal_adres=None)
        DigitaalAdresFactory.create(
            partij=partij,
            referentie="unique-ref",
            soort_digitaal_adres=SoortDigitaalAdres.email,
        )

        list_url = reverse("klantinteracties:digitaaladres-list")
        data = {
            "verstrektDoorBetrokkene": None,
            "verstrektDoorPartij": {"uuid": str(partij.uuid)},
            "soortDigitaalAdres": SoortDigitaalAdres.email,
            "adres": "barfoo@example.com",
            "omschrijving": "another omschrijving",
            "referentie": "unique-ref",
        }

        with self.subTest("with the same soort digitaal adres"):
            response = self.client.post(list_url, data)
            self.assertEqual(
                response.status_code, status.HTTP_400_BAD_REQUEST, response.data
            )
            error = get_validation_errors(response, "nonFieldErrors")
            self.assertEqual(error["code"], "unique")

            # Object should not be created due to failing validation
            self.assertEqual(DigitaalAdres.objects.count(), 1)

        with self.subTest("with a different soort digitaal adres"):
            response = self.client.post(
                list_url,
                data
                | {
                    "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
                    "adres": "0721434543",
                },
            )
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, response.data
            )

    def test_update_digitaal_adres_validate_uniqueness_if_both_verstrektDoorPartij_and_referentie(
        self,
    ):
        """
        Ensure that UniqueConstraint applies if both verstrektDoorPartij and referentie are set
        when performing a PATCH
        """
        partij = PartijFactory.create(voorkeurs_digitaal_adres=None)
        DigitaalAdresFactory.create(
            partij=partij,
            referentie="unique-ref",
            soort_digitaal_adres=SoortDigitaalAdres.email,
        )

        digitaal_adres = DigitaalAdresFactory.create(
            partij=partij,
            referentie="old-ref",
            soort_digitaal_adres=SoortDigitaalAdres.email,
        )

        detail_url = reverse(
            "klantinteracties:digitaaladres-detail",
            kwargs={"uuid": str(digitaal_adres.uuid)},
        )

        with self.subTest("explicitly specify partij"):
            response = self.client.patch(detail_url, {"referentie": "unique-ref"})
            self.assertEqual(response.status_code, 400)
            error = get_validation_errors(response, "nonFieldErrors")
            self.assertEqual(error["code"], "unique")

        with self.subTest("without specifying partij"):
            response2 = self.client.patch(
                detail_url,
                {
                    "verstrektDoorPartij": {"uuid": str(partij.uuid)},
                    "referentie": "unique-ref",
                },
            )
            self.assertEqual(response2.status_code, 400)
            error = get_validation_errors(response, "nonFieldErrors")
            self.assertEqual(error["code"], "unique")

        with self.subTest("changing soort digitaal adres"):
            response = self.client.patch(
                detail_url,
                {
                    "referentie": "unique-ref",
                    "soortDigitaalAdres": SoortDigitaalAdres.telefoonnummer,
                    "adres": "0721434543",
                },
            )
            self.assertEqual(response.status_code, 200)
