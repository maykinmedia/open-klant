"""
Guarantee that the proper authorization machinery is in place.
"""
import requests_mock
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import AuthCheckMixin, JWTAuthMixin, reverse

from openklant.components.legacy.klanten.api.scopes import SCOPE_KLANTEN_ALLES_LEZEN
from openklant.components.legacy.klanten.models.constants import KlantType
from openklant.components.legacy.klanten.models.klanten import Klant
from openklant.components.legacy.klanten.models.tests.factories import KlantFactory

SUBJECT = "http://example.com/subject/1"


class KlantScopeForbiddenTests(AuthCheckMixin, APITestCase):
    def test_cannot_create_klant_without_correct_scope(self):
        url = reverse("klant-list")
        self.assertForbidden(url, method="post")

    def test_cannot_read_without_correct_scope(self):
        klant = KlantFactory.create()
        urls = [
            reverse("klant-list"),
            reverse(klant),
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertForbidden(url, method="get")


class KlantScopeTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = False
    scopes = [SCOPE_KLANTEN_ALLES_LEZEN]
    maxDiff = None

    def test_list_klanten(self):
        list_url = reverse(Klant)
        KlantFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_create_klant_url(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Xavier",
            "achternaam": "Jackson",
            "emailadres": "test@gmail.com",
            "adres": {
                "straatnaam": "Keizersgracht",
                "huisnummer": "117",
                "huisletter": "A",
                "postcode": "1015CJ",
                "woonplaatsnaam": "test",
                "landcode": "1234",
            },
            "subjectType": KlantType.natuurlijk_persoon,
            "subject": SUBJECT,
        }

        with requests_mock.Mocker() as m:
            m.get(SUBJECT, json={})
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
