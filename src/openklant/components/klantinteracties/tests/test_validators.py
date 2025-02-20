from django.core.exceptions import ValidationError
from django.test import TestCase

from openklant.components.klantinteracties.models.constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)
from openklant.components.klantinteracties.models.partijen import PartijIdentificator
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijIdentificatorFactory,
)
from openklant.components.klantinteracties.models.validators import (
    PartijIdentificatorTypesValidator,
    PartijIdentificatorUniquenessValidator,
)


class PartijIdentificatorTypesValidatorTests(TestCase):
    def test_valid(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )
        validator.validate()

    # Start section validate_code_objecttype

    def test_valid_code_objecttype_null(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": "",
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )
        validator.validate_code_objecttype()

    def test_valid_code_objecttype_top_level_null_or_overig(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": "",
            }
        )
        validator.validate_code_objecttype()

        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.overig.value,
            }
        )
        validator.validate_code_objecttype()

    def test_invalid_code_objecttype_not_found_in_top_level(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorTypesValidator(
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "296648875",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )
            validator.validate_code_objecttype()

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_code_objecttype"][0],
            "voor `codeRegister` brp zijn alleen deze waarden toegestaan: ['natuurlijk_persoon']",
        )

    # Start section validate_code_soort_object_id

    def test_valid_code_soort_object_id_null(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": "",
                "object_id": "12345678",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )
        validator.validate_code_soort_object_id()

    def test_invalid_code_soort_object_id_not_found_in_top_level(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorTypesValidator(
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
                    "object_id": "296648875",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )
            validator.validate_code_soort_object_id()

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_code_soort_object_id"][0],
            "voor `codeObjecttype` natuurlijk_persoon zijn alleen deze waarden toegestaan: ['bsn', 'overig']",
        )

    # Start section validate_object_id

    def test_valid_object_id_null(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )
        validator.validate_object_id()

    def test_valid_object_id_top_level_null_or_overig(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": "",
                "object_id": "1123",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )
        validator.validate_object_id()

        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.overig.value,
                "object_id": "1123",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )
        validator.validate_object_id()

    def test_valid_object_id_bsn(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            }
        )
        validator.validate_object_id()

    def test_valid_object_id_vestigingsnummer(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
                "object_id": "296648875154",
                "code_register": PartijIdentificatorCodeRegister.hr.value,
            }
        )
        validator.validate_object_id()

    def test_valid_object_id_rsin(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.rsin.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.hr.value,
            }
        )
        validator.validate_object_id()

    def test_valid_object_id_kvk_nummer(self):
        validator = PartijIdentificatorTypesValidator(
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
                "object_id": "12345678",
                "code_register": PartijIdentificatorCodeRegister.hr.value,
            }
        )
        validator.validate_object_id()

    def test_invalid_object_id_len_bsn(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorTypesValidator(
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "123",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )
            validator.validate_object_id()

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "Deze waarde is ongeldig, reden: Waarde moet 9 tekens lang zijn",
        )

    def test_invalid_object_id_digit_bsn(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorTypesValidator(
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "123TEST123",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )
            validator.validate_object_id()

        details = error.exception.message_dict
        self.assertEqual(
            details["partij_identificator_object_id"][0],
            "Deze waarde is ongeldig, reden: Voer een numerieke waarde in",
        )

    def test_invalid_object_id_proef11_bsn(self):
        with self.assertRaises(ValidationError) as error:
            validator = PartijIdentificatorTypesValidator(
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "123456789",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                }
            )
            validator.validate_object_id()

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
            validator = PartijIdentificatorTypesValidator(
                partij_identificator={
                    "code_register": case[0],
                    "code_objecttype": case[1],
                    "code_soort_object_id": case[2],
                    "object_id": case[3],
                },
            )
            validator.validate()

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
                validator = PartijIdentificatorTypesValidator(
                    partij_identificator={
                        "code_register": case[0],
                        "code_objecttype": case[1],
                        "code_soort_object_id": case[2],
                        "object_id": case[3],
                    }
                )
                validator.validate()


class PartijIdentificatorUniquenessValidatorTests(TestCase):

    def test_valid_global_uniqueness(self):
        PartijIdentificatorUniquenessValidator(
            queryset=PartijIdentificator.objects.all(),
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                "object_id": "296648875",
                "code_register": PartijIdentificatorCodeRegister.brp.value,
            },
            sub_identificator_van=None,
            instance=None,
        ).check()

    def test_valid_relation_sub_identificator_van(self):
        # check self relation and sub_identificator_van allowed cases
        sub_identificator_van = PartijIdentificatorFactory.create(
            partij_identificator_code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            partij_identificator_code_soort_object_id=PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
            partij_identificator_object_id="12345678",
            partij_identificator_code_register=PartijIdentificatorCodeRegister.hr.value,
        )
        PartijIdentificatorUniquenessValidator(
            queryset=PartijIdentificator.objects.all(),
            partij_identificator={
                "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
                "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
                "object_id": "296648875154",
                "code_register": PartijIdentificatorCodeRegister.hr.value,
            },
            sub_identificator_van=sub_identificator_van,
            instance=None,
        ).check()

    def test_invalid_self_relation_sub_identificator_van(self):
        partij_identificator = PartijIdentificatorFactory.create(
            partij_identificator_code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            partij_identificator_code_soort_object_id=PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
            partij_identificator_object_id="12345678",
            partij_identificator_code_register=PartijIdentificatorCodeRegister.hr.value,
        )
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorUniquenessValidator(
                queryset=PartijIdentificator.objects.all(),
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
                    "object_id": "296648875154",
                    "code_register": PartijIdentificatorCodeRegister.hr.value,
                },
                sub_identificator_van=partij_identificator,
                instance=partij_identificator,
            ).check()

        details = error.exception.message_dict
        self.assertEqual(
            details["sub_identificator_van"][0],
            "Kan zichzelf niet selecteren als `sub_identificator_van`.",
        )

    def test_invalid_sub_identificator_van_type_not_allowed(self):
        # sub_identificator_van type not allowed
        sub_identificator_van = PartijIdentificatorFactory.create(
            partij_identificator_code_objecttype=PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
            partij_identificator_code_soort_object_id=PartijIdentificatorCodeSoortObjectId.bsn.value,
            partij_identificator_object_id="296648875",
            partij_identificator_code_register=PartijIdentificatorCodeRegister.brp.value,
        )
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorUniquenessValidator(
                queryset=PartijIdentificator.objects.all(),
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
                    "object_id": "296648875154",
                    "code_register": PartijIdentificatorCodeRegister.hr.value,
                },
                sub_identificator_van=sub_identificator_van,
                instance=None,
            ).check()

        details = error.exception.message_dict
        self.assertEqual(
            details["sub_identificator_van"][0],
            "Het is alleen mogelijk om sub_identifier_vans te selecteren die CodeSoortObjectId = `kvk_nummer` hebben.",
        )

    def test_invalid_partij_identificator_type_not_allowed_for_sub_identificator_van(
        self,
    ):
        # partij identificator type not allowed for sub_identificator_van
        sub_identificator_van = PartijIdentificatorFactory.create(
            partij_identificator_code_objecttype=PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
            partij_identificator_code_soort_object_id=PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
            partij_identificator_object_id="12345678",
            partij_identificator_code_register=PartijIdentificatorCodeRegister.hr.value,
        )
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorUniquenessValidator(
                queryset=PartijIdentificator.objects.all(),
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.bsn.value,
                    "object_id": "296648875",
                    "code_register": PartijIdentificatorCodeRegister.brp.value,
                },
                sub_identificator_van=sub_identificator_van,
                instance=None,
            ).check()

        details = error.exception.message_dict
        self.assertEqual(
            details["sub_identificator_van"][0],
            "Alleen een identifier met code_soort_object_id kan een `sub_identificator_van' hebben.",
        )

    def test_invalid_partij_identificator_vestigingsnummer_require_sub_identificator_van(
        self,
    ):
        with self.assertRaises(ValidationError) as error:
            PartijIdentificatorUniquenessValidator(
                queryset=PartijIdentificator.objects.all(),
                partij_identificator={
                    "code_objecttype": PartijIdentificatorCodeObjectType.vestiging.value,
                    "code_soort_object_id": PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
                    "object_id": "296648875154",
                    "code_register": PartijIdentificatorCodeRegister.hr.value,
                },
                sub_identificator_van=None,
                instance=None,
            ).check()

        details = error.exception.message_dict
        self.assertTrue(
            "`sub_identifier_van` met CodeSoortObjectId = `kvk_nummer` te kiezen."
            in details["sub_identificator_van"][0]
        )
