from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.klantinteracties.api.validators import digitaal_adres_exists
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres


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
                "view_name": "digitaaladres-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van dit digitaal adres binnen deze API.",
            },
        }


class DigitaalAdresSerializer(serializers.HyperlinkedModelSerializer):
    from openklant.components.klantinteracties.api.serializers.klantcontacten import (
        BetrokkeneForeignKeySerializer,
    )

    betrokkene = BetrokkeneForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_(
            "Digitaal adres dat een betrokkene bij klantcontact verstrekte voor gebruik bij "
            "opvolging van een klantcontact."
        ),
    )

    class Meta:
        model = DigitaalAdres
        fields = (
            "uuid",
            "url",
            "betrokkene",
            "adres",
            "soort_digitaal_adres",
            "omschrijving",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "digitaaladres-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van dit digitaal adres binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        from openklant.components.klantinteracties.models.klantcontacten import (
            Betrokkene,
        )

        if "betrokkene" in validated_data:
            if betrokkene := validated_data.pop("betrokkene", None):
                betrokkene = Betrokkene.objects.get(uuid=str(betrokkene.get("uuid")))

            validated_data["betrokkene"] = betrokkene

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        from openklant.components.klantinteracties.models.klantcontacten import (
            Betrokkene,
        )

        if betrokkene := validated_data.pop("betrokkene", None):
            validated_data["betrokkene"] = Betrokkene.objects.get(
                uuid=str(betrokkene.get("uuid"))
            )

        return super().create(validated_data)
