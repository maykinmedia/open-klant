"""
Guarantee that the proper authorization machinery is in place.
"""
from rest_framework.test import APITestCase
from vng_api_common.tests import AuthCheckMixin, reverse

from openklant.components.legacy.contactmomenten.models.tests.factories import (
    ContactMomentFactory,
)


class KlantScopeForbiddenTests(AuthCheckMixin, APITestCase):
    def test_cannot_create_without_correct_scope(self):
        url = reverse("contactmoment-list")
        self.assertForbidden(url, method="post")

    def test_cannot_read_without_correct_scope(self):
        contactmoment = ContactMomentFactory.create()
        urls = [
            reverse("contactmoment-list"),
            reverse(contactmoment),
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertForbidden(url, method="get")
