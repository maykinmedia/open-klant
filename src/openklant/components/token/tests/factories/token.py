import factory

from django_otp.util import random_hex
from factory.django import DjangoModelFactory

from openklant.components.token.models import TokenAuth


class TokenAuthFactory(DjangoModelFactory):
    identifier = factory.LazyAttribute(lambda: f"token-{random_hex()}")
    contact_person = factory.Faker("name")
    email = factory.Faker("email")

    class Meta:
        model = TokenAuth
