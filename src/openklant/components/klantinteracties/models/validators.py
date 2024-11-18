from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)


class ObjectIdValidator:
    """
    Validates an ObjectId based on digit check, length, and optional 11-proof check.
    """

    list_size = []
    check_11proefnumber = False

    def __init__(self, value: str):
        self.value = value

    def validate_isdigit(self) -> None:
        """Validates that the value contains only digits."""
        if not self.value.isdigit():
            raise ValidationError("Expected a numerical value", code="invalid")

    def validate_length(self) -> None:
        """Validates that the length of the value is within the allowed sizes."""
        if len(self.value) not in self.list_size:
            raise ValidationError(
                "The length must be in: %s" % self.list_size, code="invalid"
            )

    def validate_11proefnumber(self) -> None:
        """Validates the value based on the 11-proof check."""
        total = 0
        for multiplier, char in enumerate(reversed(self.value), start=1):
            if multiplier == 1:
                total += -multiplier * int(char)
            else:
                total += multiplier * int(char)

        if total % 11 != 0:
            raise ValidationError("Invalid code", code="invalid")

    def validate(self) -> None:
        self.validate_isdigit()
        self.validate_length()
        if self.check_11proefnumber:
            self.validate_11proefnumber()


class PartijIdentificatorValidator:
    REGISTERS = {
        PartijIdentificatorCodeRegister.brp: {
            PartijIdentificatorCodeObjectType.natuurlijk_persoon: [
                PartijIdentificatorCodeSoortObjectId.bsn,
                PartijIdentificatorCodeSoortObjectId.overige,
            ],
            PartijIdentificatorCodeObjectType.overige: [],
        },
        PartijIdentificatorCodeRegister.hr: {
            PartijIdentificatorCodeObjectType.vestiging: [
                PartijIdentificatorCodeSoortObjectId.vestigingsnummer,
                PartijIdentificatorCodeSoortObjectId.overige,
            ],
            PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon: [
                PartijIdentificatorCodeSoortObjectId.rsin,
                PartijIdentificatorCodeSoortObjectId.kvknummer,
                PartijIdentificatorCodeSoortObjectId.overige,
            ],
            PartijIdentificatorCodeObjectType.overige: [],
        },
        PartijIdentificatorCodeRegister.overige: {},
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
            or self.code_register == PartijIdentificatorCodeRegister.overige
        ):
            return

        if self.code_objecttype not in self.REGISTERS.get(self.code_register, {}):
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
            or self.code_objecttype == PartijIdentificatorCodeObjectType.overige
        ):
            return

        if not any(
            self.code_soort_object_id in d.get(self.code_objecttype, [])
            for d in self.REGISTERS.values()
        ):
            raise ValidationError(
                {
                    "partij_identificator_code_soort_object_id": _(
                        "codeSoortObjectId keuzes zijn beperkt op basis van codeObjecttype."
                    )
                }
            )

    def validate_object_id(self) -> None:
        """Validates the object_id based on the codeSoortObjectId"""
        if not self.object_id:
            return

        if (
            not self.code_soort_object_id
            or self.code_soort_object_id == PartijIdentificatorCodeSoortObjectId.overige
        ):
            return

        try:
            getattr(self, f"_validate_{self.code_soort_object_id}")()
        except ValidationError as error:
            raise ValidationError(
                {
                    "partij_identificator_object_id": _(
                        "ObjectId ongeldig, reden: %s" % (error.message)
                    )
                }
            )

    def _validate_bsn(self) -> None:
        """Validate BSN"""
        validator = ObjectIdValidator(self.object_id)
        validator.list_size = [8, 9]
        validator.check_11proefnumber = True
        validator.validate()

    def _validate_vestigingsnummer(self) -> None:
        """Validate Vestigingsnummer"""
        validator = ObjectIdValidator(self.object_id)
        validator.list_size = [12]
        validator.validate()

    def _validate_rsin(self) -> None:
        """Validate RSIN"""
        validator = ObjectIdValidator(self.object_id)
        validator.list_size = [8, 9]
        validator.check_11proefnumber = True
        validator.validate()

    def _validate_kvknummer(self) -> None:
        """Validate Kvk_nummer"""
        validator = ObjectIdValidator(self.object_id)
        validator.list_size = [8]
        validator.validate()
