from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

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
            "uuid": {"required": True},
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
