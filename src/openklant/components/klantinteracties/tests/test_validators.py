from django.core.exceptions import ValidationError
from django.test import TestCase

from openklant.components.klantinteracties.models.constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)
from openklant.components.klantinteracties.models.validators import (
    PartijIdentificatorValidator,
)


class PartijIdentificatorValidatorTests(TestCase):
    def test_valid(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate()

    # Start section validate_code_objecttype

    def test_valid_code_objecttype_null(self):
        validator = PartijIdentificatorValidator(
            code_objecttype="",
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_code_objecttype()

    def test_valid_code_objecttype_top_level_null_or_overig(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register="",
        )
        validator.validate_code_objecttype()

        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.overig.value,
        )
        validator.validate_code_objecttype()

    def test_invalid_code_objecttype_not_found_in_top_level(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(
                code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
                object_id="296648875",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )
            validator.validate_code_objecttype()

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_code_objecttype"][0],
            "codeObjecttype keuzes zijn beperkt op basis van codeRegister.",
        )

    # Start section validate_code_soort_object_id

    def test_valid_code_soort_object_id_null(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id="",
            object_id="12345678",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_code_soort_object_id()

    def test_valid_code_soort_object_id_top_level_null_or_overig(self):
        validator = PartijIdentificatorValidator(
            code_objecttype="",
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_code_soort_object_id()

        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.overig.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_code_soort_object_id()

    def test_invalid_code_soort_object_id_not_found_in_top_level(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(
                code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.rsin.value,
                object_id="296648875",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )
            validator.validate_code_soort_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_code_soort_object_id"][0],
            "voor `codeObjecttype` natuurlijk_persoon zijn alleen deze waarden toegestaan: ['bsn']",
        )

    # Start section validate_object_id

    def test_valid_object_id_null(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_object_id()

    def test_valid_object_id_top_level_null_or_overig(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id="",
            object_id="1123",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_object_id()

        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.overig.value,
            object_id="1123",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_object_id()

    def test_valid_object_id_bsn(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_object_id()

    def test_valid_object_id_vestigingsnummer(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.vestiging.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
            object_id="296648875154",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_object_id()

    def test_valid_object_id_rsin(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.rsin.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_object_id()

    def test_valid_object_id_kvk_nummer(self):
        validator = PartijIdentificatorValidator(
            code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
            object_id="12345678",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        validator.validate_object_id()

    def test_invalid_object_id_len_bsn(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(
                code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
                object_id="123",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: Waarde moet 9 tekens lang zijn",
        )

    def test_invalid_object_id_digit_bsn(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(
                code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
                object_id="123TEST123",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: Voer een numerieke waarde in",
        )

    def test_invalid_object_id_proef11_bsn(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(
                code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
                object_id="123456789",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: Onjuist BSN nummer",
        )
