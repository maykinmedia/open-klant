from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.klantinteracties.api.validators import actor_exists
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
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [actor_exists]},
            "url": {
                "view_name": "actor-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
        }


class ActorSerializer(
    NestedGegevensGroepMixin,
    serializers.HyperlinkedModelSerializer,
):
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

    @transaction.atomic
    def update(self, instance, validated_data):
        if actor := validated_data.pop("actor", None):
            validated_data["actor"] = Actor.objects.get(uuid=str(actor.get("uuid")))

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        actor_uuid = str(validated_data.pop("actor").get("uuid"))
        validated_data["actor"] = Actor.objects.get(uuid=actor_uuid)

        return super().create(validated_data)


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

    @transaction.atomic
    def update(self, instance, validated_data):
        if actor := validated_data.pop("actor", None):
            validated_data["actor"] = Actor.objects.get(uuid=str(actor.get("uuid")))

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        actor_uuid = str(validated_data.pop("actor").get("uuid"))
        validated_data["actor"] = Actor.objects.get(uuid=actor_uuid)

        return super().create(validated_data)


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

    @transaction.atomic
    def update(self, instance, validated_data):
        if actor := validated_data.pop("actor", None):
            actor_uuid = str(actor.get("uuid"))
            if actor_uuid != str(instance.actor.uuid):
                actoren = OrganisatorischeEenheid.objects.filter(actor__uuid=actor_uuid)
                if len(actoren) != 0:
                    raise serializers.ValidationError(
                        {"actor.uuid": _("Er bestaat al een actor met eenzelfde uuid.")}
                    )

            validated_data["actor"] = Actor.objects.get(uuid=actor_uuid)

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        actor_uuid = str(validated_data.pop("actor").get("uuid"))
        actoren = OrganisatorischeEenheid.objects.filter(actor__uuid=actor_uuid)

        if len(actoren) != 0:
            raise serializers.ValidationError(
                {"actor.uuid": _("Er bestaat al een actor met eenzelfde uuid.")}
            )

        validated_data["actor"] = Actor.objects.get(uuid=actor_uuid)

        return super().create(validated_data)
