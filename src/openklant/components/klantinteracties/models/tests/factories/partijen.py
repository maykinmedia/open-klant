import random
import string

import factory.fuzzy

from openklant.components.klantinteracties.models.partijen import (
    Categorie,
    CategorieRelatie,
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
    Persoon,
    Vertegenwoordigden,
)
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)

from ...constants import SoortPartij


class PartijFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    voorkeurs_digitaal_adres = factory.SubFactory(DigitaalAdresFactory)
    nummer = factory.Sequence(lambda n: str(n))
    soort_partij = factory.fuzzy.FuzzyChoice(SoortPartij.values)
    indicatie_geheimhouding = factory.Faker("pybool")
    indicatie_actief = factory.Faker("pybool")

    class Meta:
        model = Partij


class VertegenwoordigdenFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    vertegenwoordigende_partij = factory.SubFactory(PartijFactory)
    vertegenwoordigde_partij = factory.SubFactory(PartijFactory)

    class Meta:
        model = Vertegenwoordigden


class CategorieRelatieFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")

    class Meta:
        model = CategorieRelatie


class CategorieFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    naam = factory.Faker("word")

    class Meta:
        model = Categorie


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
