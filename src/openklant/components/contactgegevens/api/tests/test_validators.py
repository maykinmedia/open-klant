from uuid import uuid4

from django.test import TestCase

from rest_framework import serializers

from openklant.components.contactgegevens.api.tests.factories import (
    ContactgegevensFactory,
    OrganisatieFactory,
    PersoonFactory,
)
from openklant.components.contactgegevens.api.validators import (
    contactgegevens_exists,
    organisatie_exists,
    persoon_exists,
)


class FieldValidatorsTests(TestCase):
    def test_contactgegevens_exists(self):
        contactgegevens = ContactgegevensFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(contactgegevens_exists(contactgegevens.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                contactgegevens_exists(str(uuid4()))

    def test_organisatie_exists(self):
        organisatie = OrganisatieFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(organisatie_exists(organisatie.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                organisatie_exists(str(uuid4()))

    def test_persoon_exists(self):
        persoon = PersoonFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(persoon_exists(persoon.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                persoon_exists(str(uuid4()))
