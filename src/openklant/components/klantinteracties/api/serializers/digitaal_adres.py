from rest_framework import serializers

from openklant.components.klantinteracties.api.validators import digitaal_adres_exists
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres


class DigitaalAdresForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DigitaalAdres
        fields = (
            "uuid",
            "url",
            "adres",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [digitaal_adres_exists]},
            "url": {
                "view_name": "digitaaladres-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van dit digitaal adres binnen deze API.",
            },
            "adres": {"read_only": True},
        }


class DigitaalAdresSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DigitaalAdres
        fields = (
            "uuid",
            "url",
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
