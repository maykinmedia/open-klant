from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.polymorphism import PolymorphicSerializer
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.klantinteracties.api.polymorphism import Discriminator
from openklant.components.klantinteracties.api.validators import (
    actor_exists,
    actor_is_valid_instance,
)
from openklant.components.klantinteracties.models.actoren import (
    Actor,
    GeautomatiseerdeActor,
    Medewerker,
    OrganisatorischeEenheid,
)
from openklant.components.klantinteracties.models.constants import SoortActor


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
                "view_name": "klantinteracties:actor-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
        }


class GeautomatiseerdeActorBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeautomatiseerdeActor
        fields = (
            "functie",
            "omschrijving",
        )


class GeautomatiseerdeActorSerializer(GeautomatiseerdeActorBaseSerializer):
    class Meta(GeautomatiseerdeActorBaseSerializer.Meta):
        fields = GeautomatiseerdeActorBaseSerializer.Meta.fields + ("actor",)
        extra_kwargs = {
            "actor": {"required": True, "validators": [actor_is_valid_instance]},
        }


class OrganisatorischeEenheidBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisatorischeEenheid
        fields = (
            "omschrijving",
            "emailadres",
            "faxnummer",
            "telefoonnummer",
        )


class OrganisatorischeEenheidSerializer(OrganisatorischeEenheidBaseSerializer):
    class Meta(OrganisatorischeEenheidBaseSerializer.Meta):
        fields = OrganisatorischeEenheidBaseSerializer.Meta.fields + ("actor",)
        extra_kwargs = {
            "actor": {"required": True, "validators": [actor_is_valid_instance]},
        }


class MedewerkerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medewerker
        fields = (
            "functie",
            "emailadres",
            "telefoonnummer",
        )


class MedewerkerSerializer(MedewerkerBaseSerializer):
    class Meta(MedewerkerBaseSerializer.Meta):
        fields = MedewerkerBaseSerializer.Meta.fields + ("actor",)
        extra_kwargs = {
            "actor": {"required": True, "validators": [actor_is_valid_instance]},
        }


class ActorSerializer(
    NestedGegevensGroepMixin,
    PolymorphicSerializer,
):
    objectidentificator = ObjectidentificatorSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Gegevens die een onderwerpobject in een extern register uniek identificeren."
        ),
    )
    discriminator = Discriminator(
        discriminator_field="soort_actor",
        mapping={
            SoortActor.medewerker: MedewerkerBaseSerializer(),
            SoortActor.geautomatiseerde_actor: GeautomatiseerdeActorBaseSerializer(),
            SoortActor.organisatorische_eenheid: OrganisatorischeEenheidBaseSerializer(),
        },
        same_model=False,
        group_field="actor_identificatie",
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
                "view_name": "klantinteracties:actor-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
        }

    create_and_update_mapping = {
        SoortActor.medewerker: MedewerkerSerializer,
        SoortActor.geautomatiseerde_actor: GeautomatiseerdeActorSerializer,
        SoortActor.organisatorische_eenheid: OrganisatorischeEenheidSerializer,
    }

    @transaction.atomic
    def create(self, validated_data):
        actor_identificatie = validated_data.pop("actor_identificatie")
        actor = super().create(validated_data)

        serializer_class = self.create_and_update_mapping[
            validated_data.get("soort_actor")
        ]
        actor_identificatie["actor"] = actor.pk

        serializer = serializer_class(
            data=actor_identificatie, context=self.context, many=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return actor

    @transaction.atomic
    def update(self, instance, validated_data):
        if "actor_identificatie" in validated_data:
            actor_identificatie = validated_data.pop("actor_identificatie")
            serializer_class = self.create_and_update_mapping[
                validated_data.get("soort_actor")
            ]
            actor_identificatie["actor"] = instance.pk

            try:
                polymoprhic_instance = serializer_class.Meta.model.objects.get(
                    actor=instance
                )
                serializer = serializer_class(
                    data=actor_identificatie,
                    context=self.context,
                    instance=polymoprhic_instance,
                    many=False,
                )
            except serializer_class.Meta.model.DoesNotExist:
                self.context["request"].method = "POST"
                serializer = serializer_class(
                    data=actor_identificatie,
                    context=self.context,
                    many=False,
                )

            serializer.is_valid(raise_exception=True)
            serializer.save()

        return super().update(instance, validated_data)
