from django.core.exceptions import ValidationError
from django.test import TestCase

from openklant.components.klantinteracties.models.constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)
from openklant.components.klantinteracties.models.validators import (
    PartijIdentificatorTypesValidator,
    validate_metadata,
)


class PartijIdentificatorTypesValidatorTests(TestCase):
    def test_valid(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )

    # Start section validate_code_objecttype

    def test_valid_code_objecttype_null(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype="",
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )

    def test_valid_code_objecttype_top_level_null(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register="",
        )

    def test_invalid_code_objecttype_not_found_in_top_level(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorTypesValidator()(
                code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
                object_id="296648875",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_code_objecttype"][0],
            "voor `codeRegister` brp zijn alleen deze waarden toegestaan: ['natuurlijk_persoon']",
        )

    # Start section validate_code_soort_object_id

    def test_valid_code_soort_object_id_null(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id="",
            object_id="12345678",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )

    def test_invalid_code_soort_object_id_not_found_in_top_level(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorTypesValidator()(
                code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.rsin.value,
                object_id="296648875",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_code_soort_object_id"][0],
            "voor `codeObjecttype` natuurlijk_persoon zijn alleen deze waarden toegestaan: ['bsn']",
        )

    # Start section validate_object_id

    def test_valid_object_id_null(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )

    def test_valid_object_id_top_level_null(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id="",
            object_id="1123",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )

    def test_valid_object_id_bsn(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.brp.value,
        )

    def test_valid_object_id_vestigingsnummer(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.vestiging.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
            object_id="296648875154",
            code_register=PartijIdentificatorCodeRegister.hr.value,
        )

    def test_valid_object_id_rsin(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.rsin.value,
            object_id="296648875",
            code_register=PartijIdentificatorCodeRegister.hr.value,
        )

    def test_valid_object_id_kvk_nummer(self):
        PartijIdentificatorTypesValidator()(
            code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            code_soort_object_id=PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
            object_id="12345678",
            code_register=PartijIdentificatorCodeRegister.hr.value,
        )

    def test_invalid_object_id_len_bsn(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorTypesValidator()(
                code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
                object_id="123",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "Deze waarde is ongeldig, reden: Waarde moet 9 tekens lang zijn",
        )

    def test_invalid_object_id_digit_bsn(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorTypesValidator()(
                code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
                object_id="123TEST12",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "Deze waarde is ongeldig, reden: Voer een numerieke waarde in",
        )

    def test_invalid_object_id_proef11_bsn(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorTypesValidator()(
                code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
                object_id="123456789",
                code_register=PartijIdentificatorCodeRegister.brp.value,
            )

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "Deze waarde is ongeldig, reden: Onjuist BSN nummer",
        )

    def test_allowed_cases(self):
        valid_cases = [
            [
                PartijIdentificatorCodeRegister.brp.value,
                PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                PartijIdentificatorCodeSoortObjectId.bsn.value,
                "296648875",
            ],
            [
                PartijIdentificatorCodeRegister.hr.value,
                PartijIdentificatorCodeObjectType.vestiging.value,
                PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
                "123456789878",
            ],
            [
                PartijIdentificatorCodeRegister.hr.value,
                PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                PartijIdentificatorCodeSoortObjectId.rsin.value,
                "296648875",
            ],
            [
                PartijIdentificatorCodeRegister.hr.value,
                PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
                "12345678",
            ],
            [
                "",
                "",
                "",
                "",
            ],
            [
                PartijIdentificatorCodeRegister.brp.value,
                "",
                "",
                "",
            ],
            [
                "",
                PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "",
                "",
            ],
        ]
        for case in valid_cases:
            PartijIdentificatorTypesValidator()(
                code_register=case[0],
                code_objecttype=case[1],
                code_soort_object_id=case[2],
                object_id=case[3],
            )

    def test_not_allowed_cases(self):
        invalid_cases = [
            [
                PartijIdentificatorCodeRegister.brp.value,
                PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                PartijIdentificatorCodeSoortObjectId.bsn.value,
                "296648875",
            ],
            [
                PartijIdentificatorCodeRegister.brp.value,
                PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
                "296648875",
            ],
        ]
        for case in invalid_cases:
            with self.assertRaises(ValidationError):
                PartijIdentificatorTypesValidator()(
                    code_register=case[0],
                    code_objecttype=case[1],
                    code_soort_object_id=case[2],
                    object_id=case[3],
                )


class ValidateMetadataTests(TestCase):
    def test_valid_metadata(self):
        metadata = {
            "Betreft": "Paspoortaanvraag",
            "Type": "Vraag",
            "Opmerking": "Dit is een geldige korte string",
        }
        validate_metadata(metadata)

    def test_empty_metadata(self):
        validate_metadata({})

    def test_invalid_type_list(self):
        with self.assertRaisesMessage(
            ValidationError, "Metadata moet een JSON-object / dict zijn."
        ):
            validate_metadata([])

    def test_invalid_type_string(self):
        with self.assertRaisesMessage(
            ValidationError, "Metadata moet een JSON-object / dict zijn."
        ):
            validate_metadata("string")

    def test_invalid_value_not_string(self):
        metadata = {"Betreft": 123, "Type": "Vraag"}
        with self.assertRaisesMessage(
            ValidationError,
            "Alle values moeten strings zijn. Key 'Betreft' heeft type int.",
        ):
            validate_metadata(metadata)

    def test_value_too_long(self):
        metadata = {"Betreft": "x" * 101, "Type": "Vraag"}
        with self.assertRaisesMessage(
            ValidationError, "Value van key 'Betreft' mag maximaal 100 tekens bevatten."
        ):
            validate_metadata(metadata)

    def test_multiple_invalid_keys(self):
        metadata = {"Betreft": "x" * 101, "Type": 123}
        with self.assertRaises(ValidationError) as cm:
            validate_metadata(metadata)
        error_msg = str(cm.exception)
        self.assertTrue("Betreft" in error_msg or "Type" in error_msg)
