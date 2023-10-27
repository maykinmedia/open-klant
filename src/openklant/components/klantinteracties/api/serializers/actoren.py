from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer

from openklant.components.klantinteracties.models.actoren import (
    Actor,
    GeautomatiseerdeActor,
    Medewerker,
    OrganisatorischeEenheid,
)


class ObjectidentificatorSerializer(GegevensGroepSerializer):
    class Meta:
        model = Actor
        gegevensgroep = "objectidentificator"


class ActorForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields = (
            "uuid",
            "url",
            "naam",
        )
        extra_kwargs = {
            "url": {
                "view_name": "actor-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
            "naam": {"read_only": True},
        }


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    objectidentificator = ObjectidentificatorSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Gegevens die een onderwerpobject in een extern register uniek identificeren."
        ),
    )

    class Meta:
        model = Actor
        fields = (
            "uuid",
            "url",
            "naam",
            "soort_actor",
            "indicatie_actief",
            "objectidentificator",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "actor-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
        }


class GeautomatiseerdeActorSerializer(serializers.HyperlinkedModelSerializer):
    actor = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Iets dat of iemand die voor de gemeente werkzaamheden uitvoert."),
    )

    class Meta:
        model = GeautomatiseerdeActor
        fields = (
            "id",
            "url",
            "actor",
            "functie",
            "omschrijving",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "geautomatiseerdeactor-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van deze geautomatiseerde actor binnen deze API.",
            },
        }


class MedewerkerSerializer(serializers.HyperlinkedModelSerializer):
    actor = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Iets dat of iemand die voor de gemeente werkzaamheden uitvoert."),
    )

    class Meta:
        model = Medewerker
        fields = (
            "id",
            "url",
            "actor",
            "functie",
            "emailadres",
            "telefoonnummer",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "medewerker-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van deze medewerker binnen deze API.",
            },
        }


class OrganisatorischeEenheidSerializer(serializers.HyperlinkedModelSerializer):
    actor = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Iets dat of iemand die voor de gemeente werkzaamheden uitvoert."),
    )

    class Meta:
        model = OrganisatorischeEenheid
        fields = (
            "id",
            "url",
            "actor",
            "omschrijving",
            "emailadres",
            "faxnummer",
            "telefoonnummer",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "organisatorischeeenheid-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van deze organisatorische eenheid binnen deze API.",
            },
        }
