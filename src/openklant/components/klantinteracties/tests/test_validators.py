from django.core.exceptions import ValidationError
from django.test import TestCase

from openklant.components.klantinteracties.models.constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)
from openklant.components.klantinteracties.models.validators import (
    ObjectIdValidator,
    PartijIdentificatorValidator,
)


class ObjectIdValidatorTests(TestCase):
    def test_valid(self):
        validator = ObjectIdValidator(
            "296648875", list_size=[8, 9], check_11proefnumber=True
        )
        validator.validate()

    def test_invalid_length(self):
        validator = ObjectIdValidator(
            "1234", list_size=[8, 9], check_11proefnumber=True
        )

        with self.assertRaises(ValidationError) as error:
            validator.validate()
        self.assertTrue("The length must be in: [8, 9]" in str(error.exception))

    def test_invalid_isdigit(self):
        validator = ObjectIdValidator(
            "1234TEST", list_size=[8, 9], check_11proefnumber=True
        )

        with self.assertRaises(ValidationError) as error:
            validator.validate()
        self.assertTrue("Expected a numerical value" in str(error.exception))

    def test_invalid_11proefnumber(self):
        validator = ObjectIdValidator(
            "123456789", list_size=[8, 9], check_11proefnumber=True
        )
        with self.assertRaises(ValidationError) as error:
            validator.validate()
        self.assertTrue("Invalid code" in str(error.exception))


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

    def test_overig_code_register_ok_code_objecttype(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.overig.value,
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
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_code_objecttype()

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_code_objecttype"][0],
            "codeObjecttype keuzes zijn beperkt op basis van codeRegister.",
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

    def test_code_soort_object_id_not_found_in_code_objecttype(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_code_soort_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_code_soort_object_id"][0],
            "codeSoortObjectId keuzes zijn beperkt op basis van codeObjecttype.",
        )

    def test_oveirige_code_objecttype_ok_code_soort_object_id(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.overig.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "296648875",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        validator = PartijIdentificatorValidator(**data)
        validator.validate_code_soort_object_id()

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

    def test_overig_code_soort_object_id_ok_object_id(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": "overig",
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
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: The length must be in: [8, 9]",
        )

    def test_object_id_invalid_digit_bsn(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "123TEST123",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: Expected a numerical value",
        )

    def test_object_id_invalid_proef11_bsn(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
            "object_id": "123456789",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: Invalid code",
        )

    def test_object_id_invalid_vestigingsnummer(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
            "object_id": "1234",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: The length must be in: [12]",
        )

    def test_object_id_invalid_rsin(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
            "object_id": "1234",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: The length must be in: [8, 9]",
        )

    def test_object_id_invalid_kvknummer(self):
        data = {
            "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.kvknummer.value,
            "object_id": "1234",
            "code_register": PartijIdentificatorCodeRegister.brp.value,
        }
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorValidator(**data)
            validator.validate_object_id()
        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "ObjectId ongeldig, reden: The length must be in: [8]",
        )
