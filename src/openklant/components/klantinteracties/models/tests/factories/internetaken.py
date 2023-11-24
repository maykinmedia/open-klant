import random

import factory.fuzzy

from openklant.components.klantinteracties.models.constants import Taakstatus
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    KlantcontactFactory,
)


class InterneTaakFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    actor = factory.SubFactory(ActorFactory)
    klantcontact = factory.SubFactory(KlantcontactFactory)
    nummer = "".join(random.choice("0123456789") for i in range(10))
    gevraagde_handeling = factory.Faker("word")
    toelichting = factory.Faker("word")
    status = factory.fuzzy.FuzzyChoice(Taakstatus.values)
    toegewezen_op = factory.Faker("date_object")

    class Meta:
        model = InterneTaak
