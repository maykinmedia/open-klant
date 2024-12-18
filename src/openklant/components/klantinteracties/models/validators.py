from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)


class PartijIdentificatorValidator:
    OBJECT_TYPE_BRP = {
        PartijIdentificatorCodeObjectType.natuurlijk_persoon: [
            PartijIdentificatorCodeSoortObjectId.bsn,
        ],
    }
    OBJECT_TYPE_HR = {
        PartijIdentificatorCodeObjectType.vestiging: [
            PartijIdentificatorCodeSoortObjectId.vestigingsnummer,
        ],
        PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon: [
            PartijIdentificatorCodeSoortObjectId.rsin,
            PartijIdentificatorCodeSoortObjectId.kvknummer,
        ],
    }
    REGISTER_MAPPINGS = {
        PartijIdentificatorCodeRegister.brp: OBJECT_TYPE_BRP,
        PartijIdentificatorCodeRegister.hr: OBJECT_TYPE_HR,
        PartijIdentificatorCodeRegister.overige: {},
    }

    def __init__(
        self,
        code_register: str,
        code_object_type: str,
        code_soort_object_id: str,
        object_id: str,
    ):
        self.code_register = code_register
        self.code_object_type = code_object_type
        self.code_soort_object_id = code_soort_object_id
        self.object_id = object_id

    def validate_code_object_type(self) -> None:
        """Validates the CodeObjectType based on the provided CodeRegister"""
        if not self.code_object_type:
            return

        if self.code_register == PartijIdentificatorCodeRegister.overige:
            return

        if self.code_object_type not in self.REGISTER_MAPPINGS.get(
            self.code_register, {}
        ):
            raise ValidationError(
                _("ObjectType keuzes zijn beperkt op basis van CodeRegister.")
            )

    def validate_code_soort_object_id(self) -> None:
        """Validates the CodeSoortObjectId based on register and CodeObjectType"""
        if not self.code_soort_object_id:
            return

        if self.code_object_type == PartijIdentificatorCodeObjectType.overige:
            return

        register = self.REGISTER_MAPPINGS.get(self.code_register)
        allowed_codes = register.get(self.code_object_type, []) if register else []

        if self.code_soort_object_id not in allowed_codes:
            raise ValidationError(
                _("CodeSoortObjectId keuzes zijn beperkt op basis van CodeObjectType.")
            )

    def validate_object_id(self) -> None:
        """Validates the object ID based on the SoortObjectId"""
        if not self.object_id:
            return
        if self.code_soort_object_id == PartijIdentificatorCodeSoortObjectId.overige:
            return

        method_name = f"_validate_{self.code_soort_object_id}"
        validator = getattr(self, method_name, None)
        if validator:
            validator()
        else:
            raise ValidationError("Ongeldige Partij Identificator CodeSoortObjectId.")

    def _validate_bsn(self) -> None:
        """Validates the BSN Object ID length"""
        if len(self.object_id) not in [8, 9]:
            raise ValidationError(
                _("De lengte van de ObjectId moet tussen 8 en 9 liggen.")
            )

    def _validate_vestigingsnummer(self) -> None:
        """Validates the VestigingsNummer Object ID length"""
        if len(self.object_id) not in [12]:
            raise ValidationError(_("De lengte van de ObjectId moet 12 tekens zijn."))

    def _validate_rsin(self) -> None:
        """Validates the Rsin Object ID length"""
        if len(self.object_id) not in [8, 9]:
            raise ValidationError(
                _("De lengte van de ObjectId moet tussen 8 en 9 liggen.")
            )

    def _validate_kvknummer(self) -> None:
        """Validates the KvkNummer Object ID length"""
        if len(self.object_id) not in [8]:
            raise ValidationError(_("De lengte van de ObjectId moet 8 tekens zijn."))
