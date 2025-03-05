import random
import string

import factory.fuzzy

from openklant.components.klantinteracties.models.partijen import (
    Categorie,
    CategorieRelatie,
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
    Persoon,
    Vertegenwoordigden,
)
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)

from ...constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
    SoortPartij,
)


class PartijFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    voorkeurs_digitaal_adres = factory.SubFactory(DigitaalAdresFactory)
    nummer = factory.Sequence(lambda n: str(n))
    soort_partij = factory.fuzzy.FuzzyChoice(SoortPartij.values)
    indicatie_geheimhouding = factory.Faker("pybool")
    indicatie_actief = factory.Faker("pybool")

    class Meta:
        model = Partij


class VertegenwoordigdenFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    vertegenwoordigende_partij = factory.SubFactory(PartijFactory)
    vertegenwoordigde_partij = factory.SubFactory(PartijFactory)

    class Meta:
        model = Vertegenwoordigden


class CategorieRelatieFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")

    class Meta:
        model = CategorieRelatie


class CategorieFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    naam = factory.Faker("word")

    class Meta:
        model = Categorie


class OrganisatieFactory(factory.django.DjangoModelFactory):
    partij = factory.SubFactory(PartijFactory, soort_partij=SoortPartij.organisatie)
    naam = factory.Faker("word")

    class Meta:
        model = Organisatie


class PersoonFactory(factory.django.DjangoModelFactory):
    partij = factory.SubFactory(PartijFactory, soort_partij=SoortPartij.persoon)
    contactnaam_voorletters = ".".join(random.choices(string.ascii_uppercase, k=2))

    class Meta:
        model = Persoon


class ContactpersoonFactory(factory.django.DjangoModelFactory):
    partij = factory.SubFactory(PartijFactory, soort_partij=SoortPartij.contactpersoon)
    contactnaam_voorletters = ".".join(random.choices(string.ascii_uppercase, k=2))

    class Meta:
        model = Contactpersoon


class PartijIdentificatorFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4")
    partij = factory.SubFactory(PartijFactory)
    andere_partij_identificator = factory.Faker("word")
    sub_identificator_van = None

    class Meta:
        model = PartijIdentificator


class BsnPartijIdentificatorFactory(PartijIdentificatorFactory):
    partij_identificator_code_objecttype = (
        PartijIdentificatorCodeObjectType.natuurlijk_persoon.value
    )
    partij_identificator_code_soort_object_id = (
        PartijIdentificatorCodeSoortObjectId.bsn.value
    )
    partij_identificator_code_register = PartijIdentificatorCodeRegister.brp.value


class KvkNummerPartijIdentificatorFactory(PartijIdentificatorFactory):
    partij_identificator_code_objecttype = (
        PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value
    )
    partij_identificator_code_soort_object_id = (
        PartijIdentificatorCodeSoortObjectId.kvk_nummer.value
    )
    partij_identificator_code_register = PartijIdentificatorCodeRegister.hr.value


class VestigingsnummerPartijIdentificatorFactory(PartijIdentificatorFactory):
    partij_identificator_code_objecttype = (
        PartijIdentificatorCodeObjectType.vestiging.value
    )
    partij_identificator_code_soort_object_id = (
        PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value
    )
    partij_identificator_code_register = PartijIdentificatorCodeRegister.hr.value
