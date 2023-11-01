import factory

from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres


class DigitaalAdresFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    soort_digitaal_adres = factory.Faker("word")
    adres = factory.Faker("word")
    omschrijving = factory.Faker("word")

    class Meta:
        model = DigitaalAdres
