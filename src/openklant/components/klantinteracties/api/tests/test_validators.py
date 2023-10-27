from uuid import uuid4

from django.test import TestCase

from rest_framework import serializers

from openklant.components.klantinteracties.api.validators import (
    actor_exists,
    betrokkene_exists,
    bijlage_exists,
    contactpersoon_exists,
    digitaal_adres_exists,
    internetaak_exists,
    klantcontact_exists,
    onderwerpobject_exists,
    organisatie_exists,
    partij_exists,
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
)


class FieldValidatorsTests(TestCase):
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

    def test_partij(self):
        partij = PartijFactory.create()
        with self.subTest("exists"):
            self.assertIsNone(partij_exists(partij.uuid))
        with self.subTest("doesn't_exist"):
            with self.assertRaises(serializers.ValidationError):
                partij_exists(str(uuid4()))
