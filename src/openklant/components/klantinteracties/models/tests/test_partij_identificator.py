from django.core.exceptions import ValidationError
from django.test import TestCase

from openklant.components.klantinteracties.models.constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)
from openklant.components.klantinteracties.models.partijen import (
    Partij,
    PartijIdentificator,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijFactory,
)

"""
# ALLOWED only one time, because it does not exist in any partij
- partij_identificator(partij=partij, soortObjectId='bsn', object_id=123) 

# NOT ALLOWED because already exists one bsn for the same partij
- partij_identificator(partij=partij, soortObjectId='bsn', object_id=456)

# NOT ALLOWED because already exists one bsn=123 for another partij
- partij_identificator(partij=partij1, soortObjectId='bsn', object_id=123)

# ALLOWED only one time because vestigingsnummer=None
- partij_identificator(partij=partij1, soortObjectId='kvk', object_id=123)

# NOT ALLOWED because already exist one kvk_nummer=123 without vestigingsnummer in any partij
- partij_identificator(partij=partij2, soortObjectId='kvk', object_id=123)

# ALLOWED only one time, SAME kvk (123) NEW vestigingsnummer(123)
- partij_identificator(partij=partij3, soortObjectId='kvk', object_id=123)
- partij_identificator(partij=partij3, soortObjectId='vestigingsnummer', object_id=123)

# NOT ALLOWED beacuse arleady exists this combination
- partij_identificator(partij=partij4, soortObjectId='kvk', object_id=123)
- partij_identificator(partij=partij4, soortObjectId='vestigingsnummer', object_id=123)

# ALLOWED only one time, SAME kvk (123) NEW vestigingsnummer(456)
- partij_identificator(partij=partij5, soortObjectId='kvk', object_id=123)
- partij_identificator(partij=partij5, soortObjectId='vestigingsnummer', object_id=456)

# ALLOWED only one time, NEW kvk (456) SAME vestigingsnummer(456)
- partij_identificator(partij=partij6, soortObjectId='kvk', object_id=456)
- partij_identificator(partij=partij6, soortObjectId='vestigingsnummer', object_id=456)

    Specificando Partij
        test_bsn 
            test_1_bsn_in_partij
            test_n_bsn_in_partij
            test_1_bsn_in_multiple_partij
            test_n_bsn_in_multiple_partij
            test_diversin_bsn_in_diversi_partij
            test_same_bsn_in_diversi_partij
            test_bsn_non_deve_avere_il_parent
            
        
        test_kvk (uguali a bsn)
            test_kvk_in_partij
            test_kvk_in_partij_in_multiple_parti
            
        
                
        
        
    Senza specificare il partij
        test_constraint_partij_identificator (prova a fare lo stesso object_id)
        test_constraint_partij_identificator (prova a fare con diversi object_id)
        
        

        validator = PartijIdentificatorTypeValidator(
            code_objecttype="natuurlijk_persoon",
            code_soort_object_id="bsn",
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp,
        )
        validator.validate()
"""


class PartijIdentificatorModelConstraints(TestCase):
    def setUp(self):
        super().setUp()
        self.partij = PartijFactory.create(voorkeurs_digitaal_adres=None)

    def test_valid_scoped_identificator_globally_unique(self):
        PartijIdentificator.objects.create(
            sub_identificator_van=None,
            partij_identificator_code_objecttype="natuurlijk_persoon",
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="296648875",
            partij_identificator_code_register="brp",
        )
        PartijIdentificator.objects.create(
            sub_identificator_van=None,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="rsin",
            partij_identificator_object_id="296648875",
            partij_identificator_code_register="hr",
        )

    def test_valid_non_scoped_identificator_globally_unique_different_sub_identificator_van(
        self,
    ):
        partij_identificator_a = PartijIdentificator.objects.create(
            sub_identificator_van=None,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="12345678",
            partij_identificator_code_register="hr",
        )
        partij_identificator_b = PartijIdentificator.objects.create(
            sub_identificator_van=None,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="87654321",
            partij_identificator_code_register="hr",
        )

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

    def test_valid_non_scoped_identificator_globally_unique_different_values(self):
        partij_identificator = PartijIdentificator.objects.create(
            sub_identificator_van=None,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="kvk_nummer",
            partij_identificator_object_id="12345678",
            partij_identificator_code_register="hr",
        )

        PartijIdentificator.objects.create(
            sub_identificator_van=partij_identificator,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="123412341234",
            partij_identificator_code_register="hr",
        )

        PartijIdentificator.objects.create(
            sub_identificator_van=partij_identificator,
            partij_identificator_code_objecttype="vestiging",
            partij_identificator_code_soort_object_id="vestigingsnummer",
            partij_identificator_object_id="987698769876",
            partij_identificator_code_register="hr",
        )

    def test_invalid_scoped_identificator_globally_unique(self):
        return
        PartijIdentificator.objects.create(
            sub_identificator_van=None,
            partij_identificator_code_objecttype="natuurlijk_persoon",
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="296648875",
            partij_identificator_code_register="brp",
        )
        PartijIdentificator.objects.create(
            sub_identificator_van=None,
            partij_identificator_code_objecttype="natuurlijk_persoon",
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="296648875",
            partij_identificator_code_register="brp",
        )
