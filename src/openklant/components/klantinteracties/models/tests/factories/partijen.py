import random
import string

import factory.fuzzy

from openklant.components.klantinteracties.models.partijen import (
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
    Persoon,
)
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)

from ...constants import SoortPartij


class PartijFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    voorkeurs_digitaal_adres = factory.SubFactory(DigitaalAdresFactory)
    nummer = "".join(random.choice("0123456789") for i in range(10))
    soort_partij = factory.fuzzy.FuzzyChoice(SoortPartij.values)
    indicatie_geheimhouding = factory.Faker("pybool")
    indicatie_actief = factory.Faker("pybool")

    class Meta:
        model = Partij

    @factory.post_generation
    def vertegenwoordigde(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, do nothing.
            return

        self.vertegenwoordigde.add(*extracted)


class OrganisatieFactory(factory.django.DjangoModelFactory):
    partij = factory.SubFactory(PartijFactory)
    naam = factory.Faker("word")

    class Meta:
        model = Organisatie


class PersoonFactory(factory.django.DjangoModelFactory):
    partij = factory.SubFactory(PartijFactory)
    contactnaam_voorletters = ".".join(random.choices(string.ascii_uppercase, k=2))

    class Meta:
        model = Persoon


class ContactpersoonFactory(factory.django.DjangoModelFactory):
    partij = factory.SubFactory(PartijFactory)
    contactnaam_voorletters = ".".join(random.choices(string.ascii_uppercase, k=2))

    class Meta:
        model = Contactpersoon


class PartijIdentificatorFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    partij = factory.SubFactory(PartijFactory)
    andere_partij_identificator = factory.Faker("word")

    class Meta:
        model = PartijIdentificator
