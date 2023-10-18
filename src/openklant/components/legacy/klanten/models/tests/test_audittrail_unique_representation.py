from django.test import TestCase

from .factories import KlantFactory


class UniqueRepresentationTests(TestCase):
    def test_klant(self):
        klant = KlantFactory(bronorganisatie="950428139", klantnummer="1234")

        self.assertEqual(klant.unique_representation(), "950428139 - 1234")
