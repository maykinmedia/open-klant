import string

import factory.fuzzy

from openklant.components.klantinteracties.models.actoren import (
    Actor,
    ActorKlantcontact,
    GeautomatiseerdeActor,
    Medewerker,
    OrganisatorischeEenheid,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    KlantcontactFactory,
)

from ...constants import SoortActor


class ActorFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    naam = factory.Faker("word")
    soort_actor = factory.fuzzy.FuzzyChoice(SoortActor.values)
    indicatie_actief = factory.Faker("pybool")

    class Meta:
        model = Actor


class ActorKlantcontactFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    actor = factory.SubFactory(ActorFactory)
    klantcontact = factory.SubFactory(KlantcontactFactory)

    class Meta:
        model = ActorKlantcontact


class GeautomatiseerdeActorFactory(factory.django.DjangoModelFactory):
    actor = factory.SubFactory(ActorFactory)
    functie = factory.fuzzy.FuzzyText(
        length=40, chars=string.ascii_uppercase + string.digits
    )
    omschrijving = factory.Faker("word")

    class Meta:
        model = GeautomatiseerdeActor


class MedewerkerFactory(factory.django.DjangoModelFactory):
    actor = factory.SubFactory(ActorFactory)
    functie = factory.fuzzy.FuzzyText(
        length=20, chars=string.ascii_uppercase + string.digits
    )
    emailadres = factory.Faker("email")
    telefoonnummer = factory.fuzzy.FuzzyText(chars=string.digits)

    class Meta:
        model = Medewerker


class OrganisatorischeEenheidFactory(factory.django.DjangoModelFactory):
    actor = factory.SubFactory(ActorFactory)
    omschrijving = factory.Faker("word")
    emailadres = factory.Faker("email")
    faxnummer = factory.fuzzy.FuzzyText(chars=string.digits)
    telefoonnummer = factory.fuzzy.FuzzyText(chars=string.digits)

    class Meta:
        model = OrganisatorischeEenheid
