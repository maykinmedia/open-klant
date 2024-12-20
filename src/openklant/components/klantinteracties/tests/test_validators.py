from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework import serializers

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
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate()

    # Start section validate_code_objecttype

    def test_valid_empty_code_objecttype(self):
        data = {
            "code_objecttype": "",
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_code_objecttype()

    def test_empty_code_register_ok_code_objecttype(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": "",
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_code_objecttype()

    def test_overige_code_register_ok_code_objecttype(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.overige.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_code_objecttype()

    def test_code_objecttype_not_found_in_code_register(self):
        data = {
            "code_objecttype": "niet_natuurlijk_persoon",
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(serializers.ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_code_objecttype()

        details = error.exception.get_full_details()
        self.assertEqual(
            details["partijIdentificator.codeObjecttype"]["message"],
            "codeObjecttype keuzes zijn beperkt op basis van codeRegister.",
        )
        self.assertEqual(
            details["partijIdentificator.codeObjecttype"]["code"], "invalid"
        )

    # Start section validate_code_soort_object_id

    def test_valid_empty_code_soort_object_id(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": "",
            "object_id": "12345678",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_code_soort_object_id()

    def test_empty_code_objecttype_ok_code_soort_object_id(self):
        data = {
            "code_objecttype": "",
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_code_soort_object_id()

    def test_oveirige_code_objecttype_ok_code_soort_object_id(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.overige.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_code_soort_object_id()

    def test_code_soort_object_id_not_found_in_code_objecttype(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(serializers.ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_code_soort_object_id()

        details = error.exception.get_full_details()
        self.assertEqual(
            details["partijIdentificator.codeSoortObjectId"]["message"],
            "codeSoortObjectId keuzes zijn beperkt op basis van codeObjecttype.",
        )
        self.assertEqual(
            details["partijIdentificator.codeSoortObjectId"]["code"], "invalid"
        )

    # Start section validate_object_id

    def test_valid_empty_object_id(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_object_id()

    def test_empty_code_soort_object_id_ok_object_id(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": "",
            "object_id": "1123",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_object_id()

    def test_overige_code_soort_object_id_ok_object_id(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": "overige",
            "object_id": "1123",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_object_id()

    def test_object_id_valid_bsn(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_object_id()

    def test_object_id_valid_vestigingsnummer(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
            "object_id": "296648875154",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_object_id()

    def test_object_id_valid_rsin(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_object_id()

    def test_object_id_valid_kvknummer(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.kvknummer.value,
            "object_id": "12345678",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_object_id()

    def test_object_id_invalid_len_bsn(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "123",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(serializers.ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.get_full_details()
        self.assertEqual(
            details["partijIdentificator.objectId"]["message"],
            "Ongeldig BSN.",
        )
        self.assertEqual(details["partijIdentificator.objectId"]["code"], "invalid")

    def test_object_id_invalid_digit_bsn(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "123TEST123",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(serializers.ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.get_full_details()
        self.assertEqual(
            details["partijIdentificator.objectId"]["message"],
            "Ongeldig BSN.",
        )
        self.assertEqual(details["partijIdentificator.objectId"]["code"], "invalid")

    def test_object_id_invalid_proef11_bsn(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "123456789",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(serializers.ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.get_full_details()
        self.assertEqual(
            details["partijIdentificator.objectId"]["message"],
            "Ongeldig BSN.",
        )
        self.assertEqual(details["partijIdentificator.objectId"]["code"], "invalid")

    def test_object_id_invalid_vestigingsnummer(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
            "object_id": "1234",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(serializers.ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.get_full_details()
        self.assertEqual(details[0]["message"], "Ongeldige veldlengte")
        self.assertEqual(details[0]["code"], "invalid")

    def test_object_id_invalid_rsin(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
            "object_id": "1234",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(serializers.ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.get_full_details()
        self.assertEqual(
            details["partijIdentificator.objectId"]["message"],
            "Ongeldig RSIN.",
        )
        self.assertEqual(details["partijIdentificator.objectId"]["code"], "invalid")

    def test_object_id_invalid_kvknummer(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.kvknummer.value,
            "object_id": "1234",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(serializers.ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.get_full_details()
        self.assertEqual(details[0]["message"], "Ongeldige veldlengte")
        self.assertEqual(details[0]["code"], "invalid")
