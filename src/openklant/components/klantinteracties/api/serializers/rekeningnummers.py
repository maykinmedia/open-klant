from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.klantinteracties.api.validators import Rekeningnummer_exists
from openklant.components.klantinteracties.models.partijen import Partij
from openklant.components.klantinteracties.models.rekeningnummers import Rekeningnummer


class RekeningnummerForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rekeningnummer
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [Rekeningnummer_exists]},
            "url": {
                "view_name": "klantinteracties:rekeningnummer-detail",
                "lookup_field": "uuid",
                "help_text": _(
                    "De unieke URL van deze rekeningnummer binnen deze API."
                ),
            },
        }


class RekeningnummerSerializer(serializers.HyperlinkedModelSerializer):
    from openklant.components.klantinteracties.api.serializers.partijen import (
        PartijForeignKeySerializer,
    )

    partij = PartijForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_("Rekeningnummer van een partij"),
    )

    class Meta:
        model = Rekeningnummer
        fields = ("uuid", "url", "partij", "iban", "bic")
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:rekeningnummer-detail",
                "lookup_field": "uuid",
                "help_text": _(
                    "De unieke URL van deze rekeningnummer binnen deze API."
                ),
            },
        }

    @transaction.atomic
    def create(self, validated_data):
        if partij := validated_data.pop("partij", None):
            validated_data["partij"] = Partij.objects.get(uuid=str(partij.get("uuid")))

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        if "partij" in validated_data:
            if partij := validated_data.pop("partij", None):
                partij = Partij.objects.get(uuid=str(partij.get("uuid")))

            validated_data["partij"] = partij

        return super().update(instance, validated_data)
