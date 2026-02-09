import random
import string

import factory.fuzzy

from ...constants import Klantcontrol
from ...klantcontacten import Betrokkene, Bijlage, Klantcontact, Onderwerpobject


class KlantcontactFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    nummer = factory.Sequence(lambda n: str(n))
    referentienummer = factory.Sequence(lambda n: str(n))
    kanaal = factory.Faker("word")
    onderwerp = factory.Faker("word")
    inhoud = factory.Faker("word")
    indicatie_contact_gelukt = factory.Faker("pybool")
    taal = factory.fuzzy.FuzzyText(length=3, chars=string.ascii_uppercase)
    vertrouwelijk = factory.Faker("pybool")

    class Meta:
        model = Klantcontact


class BetrokkeneFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    klantcontact = factory.SubFactory(KlantcontactFactory)
    rol = factory.fuzzy.FuzzyChoice(Klantcontrol.values)
    organisatienaam = factory.Faker("word")
    initiator = factory.Faker("pybool")
    contactnaam_voorletters = ".".join(random.choices(string.ascii_uppercase, k=2))

    class Meta:
        model = Betrokkene


class OnderwerpobjectFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    klantcontact = factory.SubFactory(KlantcontactFactory)
    was_klantcontact = factory.SubFactory(KlantcontactFactory)

    class Meta:
        model = Onderwerpobject


class BijlageFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    klantcontact = factory.SubFactory(KlantcontactFactory)

    class Meta:
        model = Bijlage
