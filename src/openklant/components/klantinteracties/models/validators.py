from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from vng_api_common.validators import BaseValidator, validate_bsn, validate_rsin

from .constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)


class PartijIdentificatorValidator:

    NATUURLIJK_PERSOON = [
        PartijIdentificatorCodeSoortObjectId.bsn.value,
    ]
    VESTIGING = [
        PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
    ]
    NIET_NATUURLIJK_PERSOON = [
        PartijIdentificatorCodeSoortObjectId.rsin.value,
        PartijIdentificatorCodeSoortObjectId.kvknummer.value,
    ]

    REGISTERS = {
        PartijIdentificatorCodeRegister.brp: {
            PartijIdentificatorCodeObjectType.natuurlijk_persoon: NATUURLIJK_PERSOON,
        },
        PartijIdentificatorCodeRegister.hr: {
            PartijIdentificatorCodeObjectType.vestiging: VESTIGING,
            PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon: NIET_NATUURLIJK_PERSOON,
        },
        PartijIdentificatorCodeRegister.overig: {
            PartijIdentificatorCodeObjectType.natuurlijk_persoon: NATUURLIJK_PERSOON,
            PartijIdentificatorCodeObjectType.vestiging: VESTIGING,
            PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon: NIET_NATUURLIJK_PERSOON,
        },
    }

    def __init__(
        self,
        code_register: str,
        code_objecttype: str,
        code_soort_object_id: str,
        object_id: str,
    ) -> None:
        """Initialize validator"""
        self.code_register = code_register
        self.code_objecttype = code_objecttype
        self.code_soort_object_id = code_soort_object_id
        self.object_id = object_id

    def validate(self) -> None:
        """Run all validations"""
        self.validate_code_objecttype()
        self.validate_code_soort_object_id()
        self.validate_object_id()

    def validate_code_objecttype(self) -> None:
        """Validates the codeObjecttype based on the provided codeRegister"""
        if not self.code_objecttype:
            return

        if (
            not self.code_register
            or self.code_register == PartijIdentificatorCodeRegister.overig
        ):
            return

        if self.code_objecttype not in self.REGISTERS[self.code_register]:
            raise ValidationError(
                {
                    "partij_identificator_code_objecttype": _(
                        "codeObjecttype keuzes zijn beperkt op basis van codeRegister."
                    )
                }
            )

    def validate_code_soort_object_id(self) -> None:
        """Validates the codeSoortObjectId based on register and codeObjecttype"""
        if not self.code_soort_object_id:
            return

        if (
            not self.code_objecttype
            or self.code_objecttype == PartijIdentificatorCodeObjectType.overig
        ):
            return

        if not self.code_soort_object_id in (
            choices := self.REGISTERS[self.code_register].get(self.code_objecttype, [])
        ):

            raise ValidationError(
                {
                    "partij_identificator_code_soort_object_id": _(
                        "voor `codeObjecttype` {code_objecttype} zijn alleen deze waarden toegestaan: {choices}."
                    ).format(code_objecttype=self.code_objecttype, choices=choices)
                }
            )

    def validate_object_id(self) -> None:
        """Validates the object_id based on the codeSoortObjectId"""
        if not self.object_id:
            return

        try:
            match self.code_soort_object_id:
                case PartijIdentificatorCodeSoortObjectId.bsn:
                    validate_bsn(self.object_id)
                case PartijIdentificatorCodeSoortObjectId.vestigingsnummer:
                    validator = BaseValidator(self.object_id, list_size=[12])
                    validator.validate()
                case PartijIdentificatorCodeSoortObjectId.rsin:
                    validate_rsin(self.object_id)
                case PartijIdentificatorCodeSoortObjectId.kvknummer:
                    validator = BaseValidator(self.object_id, list_size=[8])
                    validator.validate()
                case PartijIdentificatorCodeSoortObjectId.overig:
                    return
        except ValidationError as error:
            raise ValidationError(
                {
                    "partij_identificator_object_id": _(
                        "ObjectId ongeldig, reden: %s" % (error.message)
                    )
                }
            )