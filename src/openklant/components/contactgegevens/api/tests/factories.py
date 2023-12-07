import string

import factory.fuzzy

from openklant.components.contactgegevens.constants import GeslachtChoices
from openklant.components.contactgegevens.models import (
    Contactgegevens,
    Organisatie,
    Persoon,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijIdentificatorFactory,
)


class ContactgegevensFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    partij_identificator = factory.SubFactory(PartijIdentificatorFactory)

    class Meta:
        model = Contactgegevens


class OrganisatieFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    contactgegevens = factory.SubFactory(ContactgegevensFactory)
    handelsnaam = factory.Faker("word")
    oprichtingsdatum = factory.Faker("date")
    opheffingsdatum = factory.Faker("date")

    class Meta:
        model = Organisatie


class PersoonFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    contactgegevens = factory.SubFactory(ContactgegevensFactory)
    geboortedatum = factory.Faker("date")
    overlijdensdatum = factory.Faker("date")
    geslachtsnaam = factory.Faker("word")
    geslacht = factory.fuzzy.FuzzyChoice(GeslachtChoices.values)
    voorvoegsel = factory.fuzzy.FuzzyText(
        length=10, chars=string.ascii_uppercase + string.digits
    )
    voornamen = factory.Faker("word")

    class Meta:
        model = Persoon