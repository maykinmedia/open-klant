import factory

from openklant.components.klantinteracties.models.rekeningnummers import Rekeningnummer


class RekeningnummerFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    iban = factory.Sequence(lambda n: f"NL18{n}")
    bic = factory.Sequence(lambda n: f"1234567{n}")

    class Meta:
        model = Rekeningnummer
