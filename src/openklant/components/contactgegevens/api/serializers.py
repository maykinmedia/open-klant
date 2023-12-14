from django.db import transaction
from django.utils.translation import gettext_lazy as _

from django_loose_fk.drf import FKOrURLField
from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.contactgegevens.api.validators import (
    contactgegevens_exists,
    organisatie_exists,
    persoon_exists,
)
from openklant.components.contactgegevens.models import (
    Contactgegevens,
    Organisatie,
    Persoon,
)


class ContactgegevensForeignkeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contactgegevens
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {
                "required": True,
                "read_only": False,
                "validators": [contactgegevens_exists],
            },
            "url": {
                "view_name": "contactgegevens:contactgegevens-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze contactgegevens binnen deze API.",
            },
        }


class OrganisatieForeignkeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisatie
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [organisatie_exists]},
            "url": {
                "view_name": "contactgegevens:organisatie-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
        }


class PersoonForeignkeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Persoon
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [persoon_exists]},
            "url": {
                "view_name": "contactgegevens:organisatie-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze persoon binnen deze API.",
            },
        }


class OrganisatieAdresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Organisatie
        gegevensgroep = "adres"


class OrganisatieSerializer(
    NestedGegevensGroepMixin,
    serializers.HyperlinkedModelSerializer,
):
    contactgegevens = ContactgegevensForeignkeySerializer(
        required=True,
        allow_null=False,
        help_text=_("De contact gegevens van de huidige organisatie."),
    )
    adres = OrganisatieAdresSerializer(
        required=False,
        allow_null=True,
        help_text=_("De adres gegevens van een organisatie."),
    )

    class Meta:
        model = Organisatie
        fields = (
            "uuid",
            "url",
            "contactgegevens",
            "handelsnaam",
            "oprichtingsdatum",
            "opheffingsdatum",
            "adres",
            "land",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "contactgegevens:organisatie-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "contactgegevens" in validated_data:
            if contactgegevens := validated_data.pop("contactgegevens", None):
                contactgegevens = Contactgegevens.objects.get(
                    uuid=contactgegevens.get("uuid")
                )

            validated_data["contactgegevens"] = contactgegevens

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        contactgegevens_uuid = validated_data.pop("contactgegevens").get("uuid")
        validated_data["contactgegevens"] = Contactgegevens.objects.get(
            uuid=contactgegevens_uuid
        )

        return super().create(validated_data)


class PersoonAdresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Persoon
        gegevensgroep = "adres"


class PersoonSerializer(
    NestedGegevensGroepMixin,
    serializers.HyperlinkedModelSerializer,
):
    contactgegevens = ContactgegevensForeignkeySerializer(
        required=True,
        allow_null=False,
        help_text=_("De contact gegevens van het huidige persoon."),
        many=False,
    )
    adres = PersoonAdresSerializer(
        required=False,
        allow_null=True,
        help_text=_("De adres gegevens van een organisatie."),
    )

    class Meta:
        model = Persoon
        fields = (
            "uuid",
            "url",
            "contactgegevens",
            "geboortedatum",
            "overlijdensdatum",
            "geslachtsnaam",
            "geslacht",
            "voorvoegsel",
            "voornamen",
            "adres",
            "land",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "contactgegevens:organisatie-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze organisatie binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "contactgegevens" in validated_data:
            if contactgegevens := validated_data.pop("contactgegevens", None):
                contactgegevens = Contactgegevens.objects.get(
                    uuid=contactgegevens.get("uuid")
                )

            validated_data["contactgegevens"] = contactgegevens

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        contactgegevens_uuid = validated_data.pop("contactgegevens").get("uuid")
        validated_data["contactgegevens"] = Contactgegevens.objects.get(
            uuid=contactgegevens_uuid
        )

        return super().create(validated_data)


class ContactgegevensSerializer(serializers.HyperlinkedModelSerializer):
    partij_identificator = FKOrURLField(
        lookup_field="uuid",
        max_length=200,
        min_length=1,
        help_text=_(
            "URL-referentie naar de PartijIdentificator (in de Contactgegevens API)."
        ),
    )
    organisaties = OrganisatieForeignkeySerializer(
        read_only=True,
        many=True,
        source="organisatie_set",
        help_text=_("De gekoppelde organisaties"),
    )

    personen = PersoonForeignkeySerializer(
        read_only=True,
        many=True,
        source="persoon_set",
        help_text=_("De gekoppelde personen"),
    )

    class Meta:
        model = Contactgegevens
        fields = (
            "uuid",
            "url",
            "organisaties",
            "personen",
            "partij_identificator",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "contactgegevens:contactgegevens-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze contactgegevens binnen deze API.",
            },
            "partij_identificator": {
                "max_length": 200,
                "min_length": 1,
                "view_name": "klantinteracties:partijidentificator-detail",
                "lookup_field": "uuid",
            },
        }
