from uuid import uuid4

from django.test import TestCase

from rest_framework import serializers

from openklant.components.klantinteracties.api.validators import (
    actor_exists,
    actor_is_valid_instance,
    betrokkene_exists,
    bijlage_exists,
    contactpersoon_exists,
    digitaal_adres_exists,
    internetaak_exists,
    klantcontact_exists,
    onderwerpobject_exists,
    organisatie_exists,
    partij_exists,
    partij_identificator_exists,
    partij_is_organisatie,
    partij_is_valid_instance,
)
from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
)
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.internetaken import (
    InterneTaakFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
    BijlageFactory,
    KlantcontactFactory,
    OnderwerpobjectFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    ContactpersoonFactory,
    OrganisatieFactory,
    PartijFactory,
    PartijIdentificatorFactory,
)


class FieldValidatorsTests(TestCase):
    def test_actor_is_valid_instance(self):
        actor = ActorFactory.create()
        betrokkene = BetrokkeneFactory.create()

        with self.subTest("actor_is_correct_instance"):
            self.assertIsNone(actor_is_valid_instance(actor))
        with self.subTest("doesn'actor_is_wrong_instance"):
            with self.assertRaises(serializers.ValidationError):
                self.assertIsNone(actor_is_valid_instance(betrokkene))

    def test_actor(self):
        actor = ActorFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(actor_exists(actor.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                actor_exists(str(uuid4()))

    def test_betrokkene(self):
        betrokkene = BetrokkeneFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(betrokkene_exists(betrokkene.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                betrokkene_exists(str(uuid4()))

    def test_bijlage(self):
        bijlage = BijlageFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(bijlage_exists(bijlage.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                bijlage_exists(str(uuid4()))

    def test_contactpersoon(self):
        contactpersoon = ContactpersoonFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(contactpersoon_exists(contactpersoon.id))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                contactpersoon_exists(contactpersoon.id + 1)

    def test_digitaal_adres(self):
        digitaal_adres = DigitaalAdresFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(digitaal_adres_exists(digitaal_adres.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                digitaal_adres_exists(str(uuid4()))

    def test_internetaak(self):
        internetaak = InterneTaakFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(internetaak_exists(internetaak.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                internetaak_exists(str(uuid4()))

    def test_klantcontact(self):
        klantcontact = KlantcontactFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(klantcontact_exists(klantcontact.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                klantcontact_exists(str(uuid4()))

    def test_onderwerpobject(self):
        onderwerpobject = OnderwerpobjectFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(onderwerpobject_exists(onderwerpobject.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                onderwerpobject_exists(str(uuid4()))

    def test_organisatie(self):
        organisatie = OrganisatieFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(organisatie_exists(organisatie.id))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                organisatie_exists(organisatie.id + 1)

    def test_partij_is_valid_instance(self):
        partij = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create()

        with self.subTest("partij_is_correct_instance"):
            self.assertIsNone(partij_is_valid_instance(partij))
        with self.subTest("doesn'partij_is_wrong_instance"):
            with self.assertRaises(serializers.ValidationError):
                self.assertIsNone(partij_is_valid_instance(betrokkene))

    def test_partij_is_organisatie(self):
        organisatie = PartijFactory.create(soort_partij="organisatie")
        persoon = PartijFactory.create(soort_partij="persoon")

        with self.subTest("partij_is_correct_soort"):
            self.assertIsNone(partij_is_organisatie(organisatie.uuid))
        with self.subTest("partij_is_wrong_soort"):
            with self.assertRaises(serializers.ValidationError):
                self.assertIsNone(partij_is_organisatie(persoon.uuid))

    def test_partij(self):
        partij = PartijFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(partij_exists(partij.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                partij_exists(str(uuid4()))

    def test_partij_identificator(self):
        partij_identificator = PartijIdentificatorFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(partij_identificator_exists(partij_identificator.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                partij_identificator_exists(str(uuid4()))
