from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from vng_api_common.validators import (
    BaseIdentifierValidator,
    validate_bsn,
    validate_rsin,
)

from .constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)

VESTIGINGSNUMMER_LENGTH = 12
KVK_NUMMER_LENGTH = 8


class SubIdentificatorValidator:
    """
    Validator to check the reference to the sub_identificator_van

    Allowed cases:
        - if `sub_identificator_van` exist, it must have the `partij_identificator_code_soort_object_id`
          equal to `kvk_nummer` and the `partij_identificator_code_soort_object_id` must be `vestigingsnummer`.

        - if not `sub_identificator_van` exist, `partij_identificator_code_soort_object_id`
          can't be `vestigingsnummer`.
    """

    def __call__(self, attrs):
        sub_identificator_van = attrs.get("sub_identificator_van", None)
        partij_identificator = attrs.get("partij_identificator", None)

        if sub_identificator_van:
            if (
                sub_identificator_van.partij_identificator_code_soort_object_id
                != PartijIdentificatorCodeSoortObjectId.kvk_nummer.value
            ):
                raise ValidationError(
                    _(
                        "Je kunt de `sub_identificator_van` alleen koppelen als deze "
                        "een `CodeSoortObjectId` van `kvk_nummer` heeft."
                    )
                )

            if (
                partij_identificator
                and partij_identificator["code_soort_object_id"]
                != PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value
            ):
                raise ValidationError(
                    _(
                        "Je kunt de `sub_identificator_van` alleen koppelen als je een"
                        "`CodeTypeObjectId` van `vestigingsnummer` hebt."
                    )
                )
        else:
            if (
                partij_identificator
                and partij_identificator["code_soort_object_id"]
                == PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value
            ):
                raise ValidationError(
                    _(
                        "verplicht om een `sub_identificator_van` te selecteren voor de "
                        "identifier met `CodeSoortObjectId` naar `vestigingsnummer`."
                    )
                )


class PartijIdentificatorValidator:
    """
    Validator for `partij_identificator` fields which checks that the basic hierarchy is respected

    REGISTRIES = {
        "brp": {
            "natuurlijk_persoon": ["bsn", "overig"],
        },
        "hr": {
            "niet_natuurlijk_persoon": ["rsin", "kvk_nummer", "overig"],
            "vestiging": ["vestigingsnummer", "overig"],
        },
        "overig": {},
    }
    """

    NATUURLIJK_PERSOON = [
        PartijIdentificatorCodeSoortObjectId.bsn.value,
        PartijIdentificatorCodeSoortObjectId.overig.value,
    ]
    VESTIGING = [
        PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value,
        PartijIdentificatorCodeSoortObjectId.overig.value,
    ]
    NIET_NATUURLIJK_PERSOON = [
        PartijIdentificatorCodeSoortObjectId.rsin.value,
        PartijIdentificatorCodeSoortObjectId.kvk_nummer.value,
        PartijIdentificatorCodeSoortObjectId.overig.value,
    ]

    ALLOWED_OBJECT_TYPES_FOR_CODE_OBJECTTYPE = {
        PartijIdentificatorCodeObjectType.natuurlijk_persoon.value: NATUURLIJK_PERSOON,
        PartijIdentificatorCodeObjectType.vestiging.value: VESTIGING,
        PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value: NIET_NATUURLIJK_PERSOON,
    }

    ALLOWED_OBJECT_TYPES_FOR_REGISTRIES = {
        PartijIdentificatorCodeRegister.brp: [
            PartijIdentificatorCodeObjectType.natuurlijk_persoon.value,
        ],
        PartijIdentificatorCodeRegister.hr: [
            PartijIdentificatorCodeObjectType.vestiging.value,
            PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon.value,
        ],
    }

    def __call__(self, attrs):
        self.code_register = attrs.get("code_register", "")
        self.code_objecttype = attrs.get("code_objecttype", "")
        self.code_soort_object_id = attrs.get("code_soort_object_id", "")
        self.object_id = attrs.get("object_id", "")

        self.validate()

    def validate(self) -> None:
        """Run all validations"""
        self.validate_code_objecttype()
        self.validate_code_soort_object_id()
        self.validate_object_id()

    def validate_code_objecttype(self) -> None:
        """Validates the codeObjecttype based on the provided codeRegister"""
        if not self.code_objecttype:
            return

        # pass if top level is null or 'overig'
        if (
            not self.code_register
            or self.code_register == PartijIdentificatorCodeRegister.overig
        ):
            return
        if self.code_objecttype not in (
            choices := self.ALLOWED_OBJECT_TYPES_FOR_REGISTRIES[self.code_register]
        ):
            raise ValidationError(
                _(
                    "voor `codeRegister` {code_register} zijn alleen deze waarden toegestaan: {choices}"
                ).format(code_register=self.code_register, choices=choices)
            )

    def validate_code_soort_object_id(self) -> None:
        """Validates the codeSoortObjectId based on register and codeObjecttype"""
        if not self.code_soort_object_id:
            return

        # pass if top level is null or 'overig'
        if (
            not self.code_objecttype
            or self.code_objecttype == PartijIdentificatorCodeObjectType.overig
        ):
            return

        if self.code_soort_object_id not in (
            choices := self.ALLOWED_OBJECT_TYPES_FOR_CODE_OBJECTTYPE.get(
                self.code_objecttype, []
            )
        ):

            raise ValidationError(
                _(
                    "voor `codeObjecttype` {code_objecttype} zijn alleen deze waarden toegestaan: {choices}"
                ).format(code_objecttype=self.code_objecttype, choices=choices)
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
                    validator = BaseIdentifierValidator(
                        self.object_id,
                        identifier_length=VESTIGINGSNUMMER_LENGTH,
                    )
                    validator.validate()
                case PartijIdentificatorCodeSoortObjectId.rsin:
                    validate_rsin(self.object_id)
                case PartijIdentificatorCodeSoortObjectId.kvk_nummer:
                    validator = BaseIdentifierValidator(
                        self.object_id,
                        identifier_length=KVK_NUMMER_LENGTH,
                    )
                    validator.validate()
                case PartijIdentificatorCodeSoortObjectId.overig:
                    return
        except ValidationError as error:
            raise ValidationError(
                _("Deze waarde is ongeldig, reden: %s" % (error.message))
            )
