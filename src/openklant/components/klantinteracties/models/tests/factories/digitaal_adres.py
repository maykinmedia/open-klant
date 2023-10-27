import factory

from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
)


class DigitaalAdresFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    betrokkene = factory.SubFactory(BetrokkeneFactory)
    soort_digitaal_adres = factory.Faker("word")
    adres = factory.Faker("word")
    omschrijving = factory.Faker("word")

    class Meta:
        model = DigitaalAdres
