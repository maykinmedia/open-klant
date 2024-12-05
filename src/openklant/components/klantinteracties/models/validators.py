from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)


class PartijIdentificatorCodeObjectTypeValidator:

    CODE_REGISTER = {
        PartijIdentificatorCodeRegister.brp: [
            PartijIdentificatorCodeObjectType.natuurlijk_persoon,
        ],
        PartijIdentificatorCodeRegister.hr: [
            PartijIdentificatorCodeObjectType.vestiging,
            PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon,
        ],
        PartijIdentificatorCodeRegister.overige: [],
    }

    @staticmethod
    def validate(code_register, code_object_type):
        if not code_object_type:
            return

        if (
            code_object_type
            not in PartijIdentificatorCodeObjectTypeValidator.CODE_REGISTER.get(
                code_register, []
            )
        ):
            raise ValidationError(
                _("ObjectType keuzes zijn beperkt op basis van Register")
            )


class PartijIdentificatorCodeSoortObjectIdValidator:

    CODE_OBJECT_TYPE = {
        PartijIdentificatorCodeObjectType.natuurlijk_persoon: [
            PartijIdentificatorCodeSoortObjectId.bsn,
        ],
        PartijIdentificatorCodeObjectType.vestiging: [
            PartijIdentificatorCodeSoortObjectId.vestigingsnummer,
        ],
        PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon: [
            PartijIdentificatorCodeSoortObjectId.rsin,
            PartijIdentificatorCodeSoortObjectId.kvknummer,
        ],
    }

    @staticmethod
    def validate(code_object_type, code_soort_object_id):
        if not code_soort_object_id:
            return

        if (
            code_soort_object_id
            not in PartijIdentificatorCodeSoortObjectIdValidator.CODE_OBJECT_TYPE.get(
                code_object_type, []
            )
        ):
            raise ValidationError(
                _(
                    "CodeSoortObjectIdValidator keuzes zijn beperkt op basis van CodeObjectType"
                )
            )


class PartijIdentificatorObjectIdValidator:

    @staticmethod
    def validate(code_soort_object_id, object_id):
        if not object_id:
            return

        method_name = f"validate_{code_soort_object_id}"
        if hasattr(PartijIdentificatorObjectIdValidator, method_name):
            method = getattr(PartijIdentificatorObjectIdValidator, method_name)
            method(object_id)
        else:
            raise ValidationError("Ongeldige Partij Identificator CodeSoortObjectId")

    @staticmethod
    def validate_bsn(object_id):
        if len(object_id) not in [8, 9]:
            raise ValidationError(
                _("De lengte van de ObjectId moet tussen 8 en 9 liggen.")
            )

    @staticmethod
    def validate_vestigingsnummer(object_id):
        if len(object_id) != 12:
            raise ValidationError(_("De lengte van de ObjectId moet 12 tekens zijn."))

    @staticmethod
    def validate_rsin(object_id):
        if len(object_id) not in [8, 9]:
            raise ValidationError(
                _("De lengte van de ObjectId moet tussen 8 en 9 liggen.")
            )

    @staticmethod
    def validate_kvknummer(object_id):
        if len(object_id) != 8:
            raise ValidationError(_("De lengte van de ObjectId moet 8 tekens zijn."))
