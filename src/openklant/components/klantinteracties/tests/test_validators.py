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
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )

    # Start section validate_code_objecttype

    def test_valid_code_objecttype_null(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": "",
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )

    def test_valid_code_objecttype_top_level_null_or_overig(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": "",
            }
        )

        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.overig.value,
            }
        )

    def test_invalid_code_objecttype_not_found_in_top_level(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorValidator()(
                {
                    "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "296648875",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )

        details = error.exception.message
        self.assertEqual(
            details,
            "voor `codeRegister` brp zijn alleen deze waarden toegestaan: ['natuurlijk_persoon']",
        )

    # Start section validate_code_soort_object_id

    def test_valid_code_soort_object_id_null(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": "",
                "object_id": "12345678",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )

    def test_invalid_code_soort_object_id_not_found_in_top_level(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorValidator()(
                {
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
                    "object_id": "296648875",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )

        details = error.exception.message
        self.assertEqual(
            details,
            "voor `codeObjecttype` natuurlijk_persoon zijn alleen deze waarden toegestaan: ['bsn', 'overig']",
        )

    # Start section validate_object_id

    def test_valid_object_id_null(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )

    def test_valid_object_id_top_level_null_or_overig(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": "",
                "object_id": "1123",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )

        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.overig.value,
                "object_id": "1123",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )

    def test_valid_object_id_bsn(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )

    def test_valid_object_id_vestigingsnummer(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
                "object_id": "296648875154",
                "code_register": PartijIdentificatorCodeRegister.hr.value,
            }
        )

    def test_valid_object_id_rsin(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.hr.value,
            }
        )

    def test_valid_object_id_kvk_nummer(self):
        PartijIdentificatorValidator()(
            {
                "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
                "object_id": "12345678",
                "code_register": PartijIdentificatorCodeRegister.hr.value,
            }
        )

    def test_invalid_object_id_len_bsn(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorValidator()(
                {
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "123",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )

        details = error.exception.message
        self.assertEqual(
            details,
            "Deze waarde is ongeldig, reden: Waarde moet 9 tekens lang zijn",
        )

    def test_invalid_object_id_digit_bsn(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorValidator()(
                {
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "123TEST123",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )

        details = error.exception.message
        self.assertEqual(
            details,
            "Deze waarde is ongeldig, reden: Voer een numerieke waarde in",
        )

    def test_invalid_object_id_proef11_bsn(self):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorValidator()(
                {
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "123456789",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )

        details = error.exception.message
        self.assertEqual(
            details,
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
                PartijIdentificatorCodeRegister.brp.value,
                PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                PartijIdentificatorCodeSoortObjectId.overig.value,
                "123456",
            ],
            [
                PartijIdentificatorCodeRegister.hr.value,
                PartijIdentificatorCodeObjectType.vestiging.value,
                PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
                "123456789878",
            ],
            [
                PartijIdentificatorCodeRegister.hr.value,
                PartijIdentificatorCodeObjectType.vestiging.value,
                PartijIdentificatorCodeSoortObjectId.overig.value,
                "296648875",
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
                PartijIdentificatorCodeRegister.hr.value,
                PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                PartijIdentificatorCodeSoortObjectId.overig.value,
                "296648875",
            ],
            [
                PartijIdentificatorCodeRegister.overig.value,
                PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                PartijIdentificatorCodeSoortObjectId.bsn.value,
                "296648875",
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
            [
                PartijIdentificatorCodeRegister.overig.value,
                PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "",
                "",
            ],
            [
                PartijIdentificatorCodeRegister.overig.value,
                PartijIdentificatorCodeObjectType.overig.value,
                PartijIdentificatorCodeSoortObjectId.overig.value,
                "296648875",
            ],
        ]
        for case in valid_cases:
            PartijIdentificatorValidator()(
                {
                    "code_register": case[0],
                    "code_objecttype": case[1],
                    "code_soort_object_id": case[2],
                    "object_id": case[3],
                },
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
            [
                PartijIdentificatorCodeRegister.brp.value,
                PartijIdentificatorCodeObjectType.overig.value,
                PartijIdentificatorCodeSoortObjectId.bsn.value,
                "296648875",
            ],
        ]
        for case in invalid_cases:
            with self.assertRaises(ValidationError):
                PartijIdentificatorValidator()(
                    {
                        "code_register": case[0],
                        "code_objecttype": case[1],
                        "code_soort_object_id": case[2],
                        "object_id": case[3],
                    },
                )
