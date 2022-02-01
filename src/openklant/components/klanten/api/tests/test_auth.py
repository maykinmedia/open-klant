"""
Guarantee that the proper authorization machinery is in place.
"""
from rest_framework.test import APITestCase
from vng_api_common.tests import AuthCheckMixin, reverse

from openklant.components.klanten.models.tests.factories import KlantFactory


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
