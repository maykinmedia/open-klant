from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, validators

from openklant.components.klantinteracties.api.serializers.constants import (
    SERIALIZER_PATH,
)
from openklant.components.klantinteracties.api.validators import (
    SoortDigitaalAdresValidator,
    digitaal_adres_exists,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.klantcontacten import Betrokkene
from openklant.components.klantinteracties.models.partijen import Partij
from openklant.utils.serializers import get_field_value


class DigitaalAdresForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DigitaalAdres
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [digitaal_adres_exists]},
            "url": {
                "view_name": "klantinteracties:digitaaladres-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van dit digitaal adres binnen deze API."),
            },
        }


class DigitaalAdresSerializer(serializers.HyperlinkedModelSerializer):
    from openklant.components.klantinteracties.api.serializers.klantcontacten import (
        BetrokkeneForeignKeySerializer,
    )
    from openklant.components.klantinteracties.api.serializers.partijen import (
        PartijForeignKeySerializer,
    )

    verstrekt_door_partij = PartijForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_(
            "Digitaal adres dat een partij verstrekte voor gebruik bij "
            "toekomstig contact met de gemeente."
        ),
        source="partij",
    )
    verstrekt_door_betrokkene = BetrokkeneForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_(
            "Digitaal adres dat een betrokkene bij klantcontact verstrekte voor gebruik bij "
            "opvolging van een klantcontact."
        ),
        source="betrokkene",
    )

    inclusion_serializers = {
        # 1 level
        "verstrekt_door_betrokkene": f"{SERIALIZER_PATH}.klantcontacten.BetrokkeneSerializer",
        # 2 levels
        "verstrekt_door_betrokkene.had_klantcontact": f"{SERIALIZER_PATH}.klantcontacten.KlantcontactSerializer",
        # 3 levels
        "verstrekt_door_betrokkene.had_klantcontact.leidde_tot_interne_taken": f"{SERIALIZER_PATH}"
        ".internetaken.InterneTaakSerializer",
    }

    class Meta:
        model = DigitaalAdres
        fields = (
            "uuid",
            "url",
            "verstrekt_door_betrokkene",
            "verstrekt_door_partij",
            "adres",
            "soort_digitaal_adres",
            "is_standaard_adres",
            "omschrijving",
            "referentie",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "adres": {
                "help_text": _(
                    "Validatie van dit veld is afhankelijk van het opgegeven "
                    "`soortDigitaalAdres`. De validatie die toegepast wordt voor "
                    " e-mailadressen is te lezen via de volgende URL: "
                    "https://github.com/django/django/blob/4.2/django/core/validators.py#L174."
                    "Voor telefoonnummers wordt de volgende regex expressie toegepast ter "
                    "validatie: `(0[8-9]00[0-9]{4,7})|(0[1-9][0-9]{8})|(\\+[0-9]{9,20}|1400|140[0-9]{2,3})`."
                )
            },
            "url": {
                "view_name": "klantinteracties:digitaaladres-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van dit digitaal adres binnen deze API."),
            },
            "referentie": {
                "default": "",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "soort_digitaal_adres" in self.fields:
            # Avoid validating the UniqueConstraint for `soort_digitaal_adres` with
            # `is_standaard_adres=True`. We want to enforce the constraint at the database
            # level, but not via the API, because setting a new default sets all other
            # `is_standaard_adres=False` (via DigitaalAdres.save)
            self.fields["soort_digitaal_adres"].validators = [
                validator
                for validator in self.fields["soort_digitaal_adres"].validators
                if not isinstance(validator, validators.UniqueValidator)
            ]

    def validate_adres(self, adres):
        """
        Define the validator here, to avoid DRF spectacular marking the format for
        `adres` as `email`
        """
        soort_digitaal_adres = get_field_value(
            self, self.initial_data, "soort_digitaal_adres"
        )
        SoortDigitaalAdresValidator()(
            soort_digitaal_adres=soort_digitaal_adres, value=adres
        )
        return adres

    def validate(self, attrs):
        partij = get_field_value(self, attrs, "partij")
        is_standaard_adres = get_field_value(self, attrs, "is_standaard_adres")
        if is_standaard_adres and not partij:
            raise serializers.ValidationError(
                {
                    "is_standaard_adres": _(
                        "`is_standaard_adres` kan alleen gezet worden "
                        "als `verstrekt_door_partij` niet leeg is."
                    )
                }
            )

        return super().validate(attrs)

    @transaction.atomic
    def update(self, instance, validated_data):
        if "partij" in validated_data:
            if partij := validated_data.pop("partij", None):
                partij = Partij.objects.get(uuid=str(partij.get("uuid")))

            validated_data["partij"] = partij

        if "betrokkene" in validated_data:
            if betrokkene := validated_data.pop("betrokkene", None):
                betrokkene = Betrokkene.objects.get(uuid=str(betrokkene.get("uuid")))

            validated_data["betrokkene"] = betrokkene

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        if partij := validated_data.pop("partij", None):
            validated_data["partij"] = Partij.objects.get(uuid=str(partij.get("uuid")))

        if betrokkene := validated_data.pop("betrokkene", None):
            validated_data["betrokkene"] = Betrokkene.objects.get(
                uuid=str(betrokkene.get("uuid"))
            )

        return super().create(validated_data)
