import random
import string

import factory.fuzzy

from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)

from ...constants import Klantcontrol
from ...klantcontacten import Betrokkene, Klantcontact


class KlantcontactFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    kanaal = factory.Faker("word")
    onderwerp = factory.Faker("word")
    inhoud = factory.Faker("word")
    indicatie_contact_gelukt = factory.Faker("pybool")
    taal = factory.Faker("word")
    vertrouwelijk = factory.Faker("pybool")

    class Meta:
        model = Klantcontact

    @factory.post_generation
    def actoren(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for actoren in extracted:
                self.actoren.add(actoren)


class BetrokkeneFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    klantcontact = factory.SubFactory(KlantcontactFactory)
    digitaal_adres = factory.SubFactory(DigitaalAdresFactory)
    rol = factory.fuzzy.FuzzyChoice(Klantcontrol.values)
    organisatienaam = factory.Faker("word")
    initiator = factory.Faker("pybool")
    contactnaam_voorletters = ".".join(random.choices(string.ascii_uppercase, k=2))

    class Meta:
        model = Betrokkene
