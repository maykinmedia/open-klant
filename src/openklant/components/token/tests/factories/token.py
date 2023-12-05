import factory
from factory.django import DjangoModelFactory

from openklant.components.token.models import TokenAuth


class TokenAuthFactory(DjangoModelFactory):
    contact_person = factory.Faker("name")
    email = factory.Faker("email")
    organization = factory.Faker("name")
    application = factory.Faker("word")
    administration = factory.Faker("word")

    class Meta:
        model = TokenAuth
