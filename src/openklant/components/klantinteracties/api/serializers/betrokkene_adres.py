from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.klantinteracties.api.serializers.constants import (
    SERIALIZER_PATH,
)
from openklant.components.klantinteracties.api.validators import (
    OptionalEmailValidator,
    betrokkene_adres_exists,
)
from openklant.components.klantinteracties.models.digitaal_adres import BetrokkeneAdres
from openklant.components.klantinteracties.models.klantcontacten import Betrokkene
from openklant.utils.serializers import get_field_value


class BetrokkeneAdresForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BetrokkeneAdres
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [betrokkene_adres_exists]},
            "url": {
                "view_name": "klantinteracties:betrokkeneadres-detail",
                "lookup_field": "uuid",
                "help_text": _(
                    "De unieke URL van dit betrokkene adres binnen deze API."
                ),
            },
        }


class BetrokkeneAdresSerializer(serializers.HyperlinkedModelSerializer):
    from openklant.components.klantinteracties.api.serializers.klantcontacten import (
        BetrokkeneForeignKeySerializer,
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
        model = BetrokkeneAdres
        fields = (
            "uuid",
            "url",
            "verstrekt_door_betrokkene",
            "adres",
            "soort_digitaal_adres",
            "omschrijving",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:betrokkeneadres-detail",
                "lookup_field": "uuid",
                "help_text": _(
                    "De unieke URL van dit betrokkene adres binnen deze API."
                ),
            },
        }

    def validate_adres(self, adres):
        """
        Define the validator here, to avoid DRF spectacular marking the format for
        `adres` as `email`
        """
        soort_digitaal_adres = get_field_value(
            self, self.initial_data, "soort_digitaal_adres"
        )
        OptionalEmailValidator()(adres, soort_digitaal_adres)
        return adres

    @transaction.atomic
    def update(self, instance, validated_data):
        if "betrokkene" in validated_data:
            if betrokkene := validated_data.pop("betrokkene", None):
                betrokkene = Betrokkene.objects.get(uuid=str(betrokkene.get("uuid")))

            validated_data["betrokkene"] = betrokkene

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        if betrokkene := validated_data.pop("betrokkene", None):
            validated_data["betrokkene"] = Betrokkene.objects.get(
                uuid=str(betrokkene.get("uuid"))
            )

        return super().create(validated_data)
