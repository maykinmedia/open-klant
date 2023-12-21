import datetime

import factory
import factory.random

from ... import models


class ExternRegisterFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: f"code-{n}")
    locatie = factory.Faker("name")
    naam = factory.Faker("name")

    class Meta:
        model = models.ExternRegister


class KanaalFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: f"code-{n}")
    indicatie_actief = factory.Faker("pybool")
    naam = factory.Faker("name")

    class Meta:
        model = models.Kanaal


class LandFactory(factory.django.DjangoModelFactory):
    landcode = factory.Sequence(lambda n: f"landcode-{n}")
    landnaam = factory.Faker("country")
    ingangsdatum_land = factory.Faker("date_object")
    einddatum_land = factory.LazyAttribute(
        lambda land: land.ingangsdatum_land
        + datetime.timedelta(factory.random.randgen.randint(0, 2e6))
    )

    class Meta:
        model = models.Land


class SoortDigitaalAdresFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: f"code-{n}")
    indicatie_actief = factory.Faker("pybool")
    naam = factory.Faker("name")

    class Meta:
        model = models.SoortDigitaalAdres


class SoortObjectFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: f"code-{n}")
    indicatie_actief = factory.Faker("pybool")
    naam = factory.Faker("name")

    class Meta:
        model = models.SoortObject


class SoortObjectidFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: f"code-{n}")
    indicatie_actief = factory.Faker("pybool")
    naam = factory.Faker("name")

    class Meta:
        model = models.SoortObjectid


class TaalFactory(factory.django.DjangoModelFactory):
    code = factory.Sequence(lambda n: f"code-{n}")
    indicatie_actief = factory.Faker("pybool")
    naam = factory.Faker("language_name")

    class Meta:
        model = models.Taal
