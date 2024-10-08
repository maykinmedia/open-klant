from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.klantinteracties.api.serializers.constants import (
    SERIALIZER_PATH,
)
from openklant.components.klantinteracties.api.validators import digitaal_adres_exists
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.klantcontacten import Betrokkene
from openklant.components.klantinteracties.models.partijen import Partij


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
            "omschrijving",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:digitaaladres-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van dit digitaal adres binnen deze API."),
            },
        }

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
