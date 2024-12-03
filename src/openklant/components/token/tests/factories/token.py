import factory
from factory.django import DjangoModelFactory

from openklant.components.token.models import TokenAuth


class TokenAuthFactory(DjangoModelFactory):
    identifier = factory.Sequence(lambda sequence: f"token-{sequence}")
    contact_person = factory.Faker("name")
    email = factory.Faker("email")

    class Meta:
        model = TokenAuth
