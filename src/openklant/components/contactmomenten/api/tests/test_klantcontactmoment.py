from datetime import datetime

from django.utils.timezone import make_aware

import requests_mock
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from openklant.components.contactmomenten.models.constants import (
    InitiatiefNemer,
    Rol,
)
from openklant.components.contactmomenten.models.contactmomenten import KlantContactMoment
from openklant.components.contactmomenten.models.tests.factories import (
    ContactMomentFactory,
    KlantContactMomentFactory,
)


class KlantContactMomentTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_klantcontactmomenten(self):
        list_url = reverse(KlantContactMoment)
        KlantContactMomentFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_klantcontactmoment(self):
        cmc = ContactMomentFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
        )
        cmc_url = reverse(cmc)
        klantcontactmoment = KlantContactMomentFactory.create(
            contactmoment=cmc,
            rol=Rol.belanghebbende,
        )
        detail_url = reverse(klantcontactmoment)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "klant": klantcontactmoment.klant,
                "contactmoment": f"http://testserver{cmc_url}",
                "rol": Rol.belanghebbende,
                "gelezen": False,
            },
        )

    def test_create_klantcontactmoment(self):
        cmc = ContactMomentFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
        )
        cmc_url = reverse(cmc)

        list_url = reverse(KlantContactMoment)
        data = {
            "klant": "http://testserver.com/klant/1",
            "contactmoment": f"http://testserver{cmc_url}",
            "rol": Rol.gesprekspartner,
        }

        with requests_mock.Mocker() as m:
            m.get("http://testserver.com/klant/1", json={})
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klantcontactmoment = KlantContactMoment.objects.get()

        self.assertEqual(klantcontactmoment.klant, "http://testserver.com/klant/1")
        self.assertEqual(klantcontactmoment.contactmoment, cmc)
        self.assertEqual(klantcontactmoment.rol, Rol.gesprekspartner)
        self.assertEqual(klantcontactmoment.gelezen, False)

    def test_create_klantcontactmoment_klant_url_invalid(self):
        cmc = ContactMomentFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
        )
        cmc_url = reverse(cmc)

        list_url = reverse(KlantContactMoment)
        data = {
            "klant": "http://testserver.com/klant/1",
            "contactmoment": f"http://testserver{cmc_url}",
            "rol": Rol.gesprekspartner,
        }

        with requests_mock.Mocker() as m:
            m.get("http://testserver.com/klant/1", status_code=404)
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(KlantContactMoment.objects.count(), 0)

        error = get_validation_errors(response, "klant")
        self.assertEqual(error["code"], "bad-url")

    def test_create_klantcontactmoment_unique_klant_contactmoment_and_rol(self):
        cmc = ContactMomentFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
        )
        cmc_url = reverse(cmc)

        KlantContactMomentFactory.create(
            klant="http://testserver.com/klant/1",
            contactmoment=cmc,
            rol=Rol.gesprekspartner,
        )

        list_url = reverse(KlantContactMoment)
        data = {
            "klant": "http://testserver.com/klant/1",
            "contactmoment": f"http://testserver{cmc_url}",
            "rol": Rol.gesprekspartner,
        }

        with requests_mock.Mocker() as m:
            m.get("http://testserver.com/klant/1", json={})
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unique")

    def test_update_klantcontactmoment(self):
        cmc = ContactMomentFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
        )
        cmc_url = reverse(cmc)
        klantcontactmoment = KlantContactMomentFactory.create(contactmoment=cmc)
        url = reverse(klantcontactmoment)

        data = {
            "klant": "http://testserver.com/klant/1",
            "contactmoment": f"http://testserver{cmc_url}",
            "rol": Rol.gesprekspartner,
            "gelezen": True,
        }

        with requests_mock.Mocker() as m:
            m.get("http://testserver.com/klant/1", json={})
            response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klantcontactmoment = KlantContactMoment.objects.get()

        self.assertEqual(klantcontactmoment.klant, "http://testserver.com/klant/1")
        self.assertEqual(klantcontactmoment.contactmoment, cmc)
        self.assertEqual(klantcontactmoment.rol, Rol.gesprekspartner)
        self.assertEqual(klantcontactmoment.gelezen, True)

    def test_partial_update_klantcontactmoment(self):
        cmc = ContactMomentFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
        )
        klantcontactmoment = KlantContactMomentFactory.create(contactmoment=cmc)
        url = reverse(klantcontactmoment)

        with requests_mock.Mocker() as m:
            m.get("http://testserver.com/klant/1", json={})
            response = self.client.patch(url, {"gelezen": True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klantcontactmoment = KlantContactMoment.objects.get()

        self.assertEqual(klantcontactmoment.gelezen, True)

    def test_destroy_klantcontactmoment(self):
        klantcontactmoment = KlantContactMomentFactory.create()
        detail_url = reverse(klantcontactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(KlantContactMoment.objects.count(), 0)


class KlantContactMomentFilterTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True
    list_url = reverse(KlantContactMoment)

    def test_filter_klant(self):
        KlantContactMomentFactory.create(klant="https://testserver.com/klant/1")
        KlantContactMomentFactory.create()

        response = self.client.get(
            self.list_url,
            {"klant": "https://testserver.com/klant/1"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["klant"], "https://testserver.com/klant/1"
        )

    def test_filter_contactmoment(self):
        klantcontactmoment = KlantContactMomentFactory.create()
        KlantContactMomentFactory.create()
        cmc_url = reverse(klantcontactmoment.contactmoment)

        response = self.client.get(
            self.list_url,
            {"contactmoment": f"http://testserver.com{cmc_url}"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["contactmoment"],
            f"http://testserver.com{cmc_url}",
        )

    def test_filter_rol(self):
        klantcontactmoment = KlantContactMomentFactory.create(
            rol=Rol.belanghebbende,
        )
        KlantContactMomentFactory.create(
            rol=Rol.gesprekspartner,
        )

        response = self.client.get(
            self.list_url,
            {"rol": klantcontactmoment.rol},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["rol"], klantcontactmoment.rol)

    def test_pagination_default(self):
        KlantContactMomentFactory.create_batch(2)
        url = reverse(KlantContactMoment)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
