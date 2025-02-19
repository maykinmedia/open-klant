from django.db import IntegrityError
from django.test import TestCase

from openklant.components.klantinteracties.models.partijen import PartijIdentificator


class PartijIdentificatorModelConstraints(TestCase):
    def test_valid_scoped_identificator_globally_unique(self):
        partij_identificator_a = PartijIdentificator.objects.create(
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="12345678",
            partij_identificator_code_register="hr",
        )
        partij_identificator_b = PartijIdentificator.objects.create(
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )

        # different sub_identificator_van same identificator_values
        PartijIdentificator.objects.create(
            sub_identificator_van=partij_identificator_a,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="123412341234",
            partij_identificator_code_register="hr",
        )

        PartijIdentificator.objects.create(
            sub_identificator_van=partij_identificator_b,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="123412341234",
            partij_identificator_code_register="hr",
        )

        # different identificator_values same sub_identificator_van
        PartijIdentificator.objects.create(
            sub_identificator_van=partij_identificator_a,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="456745674567",
            partij_identificator_code_register="hr",
        )
        PartijIdentificator.objects.create(
            sub_identificator_van=partij_identificator_a,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="567856785678",
            partij_identificator_code_register="hr",
        )

    def test_valid_non_scoped_identificator_globally_unique(self):
        PartijIdentificator.objects.create(
            partij_identificator_code_objecttype="natuurlijk_persoon",
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="296648875",
            partij_identificator_code_register="brp",
        )
        PartijIdentificator.objects.create(
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="rsin",
            partij_identificator_object_id="296648875",
            partij_identificator_code_register="hr",
        )

    def test_invalid_check_sub_identificator_van_not_self(self):
        partij_identificator = PartijIdentificator.objects.create(
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )
        with self.assertRaises(IntegrityError):
            partij_identificator.sub_identificator_van = partij_identificator
            partij_identificator.save()
