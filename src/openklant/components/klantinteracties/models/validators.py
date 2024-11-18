from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
)


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
    ):
        """Init fields"""
        self.code_register = code_register
        self.code_objecttype = code_objecttype
        self.code_soort_object_id = code_soort_object_id
        self.object_id = object_id

    def validate(self) -> None:
        """Validate all fields"""
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
            raise serializers.ValidationError(
                {
                    "partijIdentificator.codeObjecttype": _(
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
            raise serializers.ValidationError(
                {
                    "partijIdentificator.codeSoortObjectId": _(
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

        if validator := getattr(self, f"_validate_{self.code_soort_object_id}", None):
            validator()
        else:
            raise serializers.ValidationError(
                {"partijIdentificator.objectId": _("Ongeldige codeSoortObjectId.")}
            )

    def _validate_bsn(self) -> None:
        """Validates the bsn object_id"""
        if len(self.object_id) not in [8, 9]:
            raise serializers.ValidationError(
                {
                    "partijIdentificator.objectId": _(
                        "De lengte van de objectId moet tussen 8 en 9 liggen."
                    )
                }
            )

    def _validate_vestigingsnummer(self) -> None:
        """Validates the vestigingsNummer object_id"""
        if len(self.object_id) not in [12]:
            raise serializers.ValidationError(
                {
                    "partijIdentificator.objectId": _(
                        "De lengte van de objectId moet 12 tekens zijn."
                    )
                }
            )

    def _validate_rsin(self) -> None:
        """Validates the rsin object_id"""
        if len(self.object_id) not in [8, 9]:
            raise serializers.ValidationError(
                {
                    "partijIdentificator.objectId": _(
                        "De lengte van de objectId moet tussen 8 en 9 liggen."
                    )
                }
            )

    def _validate_kvknummer(self) -> None:
        """Validates the kvkNummer object_id"""
        if len(self.object_id) not in [8]:
            raise serializers.ValidationError(
                {
                    "partijIdentificator.objectId": _(
                        "De lengte van de objectId moet 8 tekens zijn."
                    )
                }
            )
