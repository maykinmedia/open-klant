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


class PartijIdentificatorUniquenessValidator:
    def __init__(self, queryset, partij_identificator, sub_identificator_van, instance):
        self.partij_identificator = partij_identificator
        self.sub_identificator_van = sub_identificator_van
        self.instance = instance
        self.queryset = queryset

    def check(self):
        self.check_self_relation()
        self.check_sub_identificator_van()
        self.check_identificator_partij_unique()
        self.check_identificator_globally_unique()

    def check_self_relation(self):
        """
        Checks that the Identificator, does not refer to itself
        """
        if self.sub_identificator_van and self.sub_identificator_van == self.instance:
            raise ValidationError(
                {
                    "sub_identificator_van": _(
                        "Kan zichzelf niet selecteren als `sub_identificator_van`."
                    )
                }
            )

    def check_sub_identificator_van(self):
        """
        Check the reference to the sub_identificator_van

        Allowed cases:
            - if `sub_identificator_van` exist, it must have the `partij_identificator_code_soort_object_id`
            equal to `kvk_nummer` and the `partij_identificator_code_soort_object_id` must be `vestigingsnummer`.

            - if not `sub_identificator_van` exist, `partij_identificator_code_soort_object_id`
            can't be `vestigingsnummer`.
        """
        if self.sub_identificator_van:
            if (
                self.partij_identificator["code_soort_object_id"]
                != PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value
            ):
                raise ValidationError(
                    {
                        "sub_identificator_van": _(
                            "Alleen een identifier met code_soort_object_id kan een `sub_identificator_van' hebben."
                        )
                    }
                )
            if (
                self.sub_identificator_van.partij_identificator_code_soort_object_id
                != PartijIdentificatorCodeSoortObjectId.kvk_nummer.value
            ):
                raise ValidationError(
                    {
                        "sub_identificator_van": _(
                            "Het is alleen mogelijk om sub_identifier_vans te selecteren"
                            " die CodeSoortObjectId = `kvk_nummer` hebben."
                        )
                    }
                )
        else:
            if (
                self.partij_identificator
                and self.partij_identificator["code_soort_object_id"]
                == PartijIdentificatorCodeSoortObjectId.vestigingsnummer.value
            ):
                raise ValidationError(
                    {
                        "sub_identificator_van": _(
                            "Voor de Identificator met CodeSoortObjectId = `vestigingsnummer` is het verplicht om"
                            " een `sub_identifier_van` met CodeSoortObjectId = `kvk_nummer` te kiezen."
                        )
                    }
                )

    def check_identificator_partij_unique(self):
        return
        if self.queryset.filter(**filters).exists():
            raise ValidationError(
                {
                    "__all__": _(
                        "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie."
                    )
                }
            )

    def check_identificator_globally_unique(self):
        """
        Checks models constraints
        """
        filters = {
            "partij_identificator_code_objecttype": self.partij_identificator[
                "code_objecttype"
            ],
            "partij_identificator_code_soort_object_id": self.partij_identificator[
                "code_soort_object_id"
            ],
            "partij_identificator_object_id": self.partij_identificator["object_id"],
            "partij_identificator_code_register": self.partij_identificator[
                "code_register"
            ],
        }
        if self.sub_identificator_van:
            filters["sub_identificator_van"] = self.sub_identificator_van
        if self.queryset.filter(**filters).exists():
            raise ValidationError(
                {
                    "__all__": _(
                        "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie."
                    )
                }
            )


class PartijIdentificatorTypesValidator:
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

    def __init__(self, partij_identificator: dict) -> None:
        """Initialize validator"""
        self.code_register = partij_identificator["code_register"]
        self.code_objecttype = partij_identificator["code_objecttype"]
        self.code_soort_object_id = partij_identificator["code_soort_object_id"]
        self.object_id = partij_identificator["object_id"]

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
                {
                    "partij_identificator_code_objecttype": _(
                        "voor `codeRegister` {code_register} zijn alleen deze waarden toegestaan: {choices}"
                    ).format(code_register=self.code_register, choices=choices)
                }
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
                {
                    "partij_identificator_code_soort_object_id": _(
                        "voor `codeObjecttype` {code_objecttype} zijn alleen deze waarden toegestaan: {choices}"
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
                {
                    "partij_identificator_object_id": _(
                        "Deze waarde is ongeldig, reden: %s" % (error.message)
                    )
                }
            )
