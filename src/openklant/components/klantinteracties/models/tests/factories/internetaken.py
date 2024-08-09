import factory.fuzzy

from openklant.components.klantinteracties.models.constants import Taakstatus
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    KlantcontactFactory,
)


class InterneTaakFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    klantcontact = factory.SubFactory(KlantcontactFactory)
    nummer = factory.Sequence(lambda n: str(n))
    gevraagde_handeling = factory.Faker("word")
    toelichting = factory.Faker("word")
    status = factory.fuzzy.FuzzyChoice(Taakstatus.values)
    toegewezen_op = factory.Faker("date_object")

    class Meta:
        model = InterneTaak

    @factory.post_generation
    def actoren(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for actor in extracted:
                self.actoren.add(actor)
