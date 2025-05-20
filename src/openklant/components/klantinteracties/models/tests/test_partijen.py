from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase

from openklant.components.klantinteracties.models.partijen import PartijIdentificator
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijFactory,
)


class PartijIdentificatorModelConstraints(TestCase):
    def test_valid_globally_unique(self):
        partij_a = PartijFactory.create()
        partij_identificator_a = PartijIdentificator.objects.create(
            partij=partij_a,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="12345678",
            partij_identificator_code_register="hr",
        )

        partij_b = PartijFactory.create()
        partij_identificator_b = PartijIdentificator.objects.create(
            partij=partij_b,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )

        # different sub_identificator_van same values
        PartijIdentificator.objects.create(
            partij=partij_a,
            sub_identificator_van=partij_identificator_a,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="123412341234",
            partij_identificator_code_register="hr",
        )

        PartijIdentificator.objects.create(
            partij=partij_b,
            sub_identificator_van=partij_identificator_b,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="123412341234",
            partij_identificator_code_register="hr",
        )

        # different partij and different sub_identificator_van
        partij_c = PartijFactory.create()
        PartijIdentificator.objects.create(
            partij=partij_c,
            sub_identificator_van=partij_identificator_b,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="4567456745674567",
            partij_identificator_code_register="hr",
        )

        # different values same sub_identificator_van
        PartijIdentificator.objects.create(
            partij=partij_a,
            sub_identificator_van=partij_identificator_a,
            partij_identificator_code_objecttype="natuurlijk_persoon",
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="123456782",
            partij_identificator_code_register="brp",
        )
        PartijIdentificator.objects.create(
            partij=partij_b,
            sub_identificator_van=partij_identificator_b,
            partij_identificator_code_objecttype="natuurlijk_persoon",
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="123456782",
            partij_identificator_code_register="brp",
        )

    def test_non_scoped_identificator_globally_unique(self):
        partij = PartijFactory.create()
        PartijIdentificator.objects.create(
            partij=partij,
            sub_identificator_van=None,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )
        with self.assertRaises(ValidationError) as error:
            PartijIdentificator.objects.create(
                partij=partij,
                sub_identificator_van=None,
                partij_identificator_code_objecttype="niet_natuurlijk_persoon",
                partij_identificator_code_soort_object_id="kvk_nummer",
                partij_identificator_object_id="87654321",
                partij_identificator_code_register="hr",
            )
        self.assertEqual(
            error.exception.message_dict,
            {
                "__all__": [
                    "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie.",
                    "Partij identificator met deze Partij en Soort object ID bestaat al.",
                ]
            },
        )

    def test_scoped_identificator_globally_unique(self):
        partij = PartijFactory.create()
        sub_identificator_van = PartijIdentificator.objects.create(
            partij=partij,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )
        PartijIdentificator.objects.create(
            partij=partij,
            sub_identificator_van=sub_identificator_van,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="112233440001",
            partij_identificator_code_register="hr",
        )

        with self.assertRaises(ValidationError) as error:
            PartijIdentificator.objects.create(
                partij=partij,
                sub_identificator_van=sub_identificator_van,
                partij_identificator_code_objecttype="vestiging",
                partij_identificator_code_soort_object_id="vestigingsnummer",
                partij_identificator_object_id="112233440001",
                partij_identificator_code_register="hr",
            )
        self.assertEqual(
            error.exception.message_dict,
            {
                "__all__": [
                    "Partij identificator met deze Partij en Soort object ID bestaat al.",
                    "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie.",
                ]
            },
        )

    def test_non_scoped_identificator_locally_unique(self):
        partij = PartijFactory.create()
        PartijIdentificator.objects.create(
            partij=partij,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )

        with self.assertRaises(ValidationError) as error:
            PartijIdentificator.objects.create(
                partij=partij,
                partij_identificator_code_objecttype="niet_natuurlijk_persoon",
                partij_identificator_code_soort_object_id="kvk_nummer",
                partij_identificator_object_id="11112222",
                partij_identificator_code_register="hr",
            )

        self.assertEqual(
            error.exception.message_dict,
            {
                "__all__": [
                    "Partij identificator met deze Partij en Soort object ID bestaat al."
                ]
            },
        )

    def test_protected_delete(self):
        partij = PartijFactory.create()
        sub_identificator_van = PartijIdentificator.objects.create(
            partij=partij,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )
        PartijIdentificator.objects.create(
            partij=partij,
            sub_identificator_van=sub_identificator_van,
            partij_identificator_code_objecttype="natuurlijk_persoon",
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="123456782",
            partij_identificator_code_register="brp",
        )
        with self.assertRaises(ProtectedError) as error:
            PartijIdentificator.objects.filter(uuid=sub_identificator_van.uuid).delete()

        self.assertTrue(
            "Cannot delete some instances of model 'PartijIdentificator'"
            in error.exception.args[0],
        )


class PartijIdentificatorModelClean(TestCase):
    def test_clean_sub_identificator_van_different_self_related(self):
        partij_identificator = PartijIdentificator.objects.create(
            partij=PartijFactory.create(),
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )
        with self.assertRaises(ValidationError) as error:
            partij_identificator.sub_identificator_van = partij_identificator
            partij_identificator.save()
        self.assertEqual(
            error.exception.message_dict,
            {
                "sub_identificator_van": [
                    "Een `Partijidentificator` kan geen `subIdentificatorVan` zijn van zichzelf."
                ]
            },
        )
