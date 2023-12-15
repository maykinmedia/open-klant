from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.klantinteracties.api.polymorphism import (
    Discriminator,
    PolymorphicSerializer,
)
from openklant.components.klantinteracties.api.validators import actor_exists
from openklant.components.klantinteracties.models.actoren import (
    Actor,
    GeautomatiseerdeActor,
    Medewerker,
    OrganisatorischeEenheid,
)
from openklant.components.klantinteracties.models.constants import SoortActor


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
                "help_text": _("De unieke URL van deze actor binnen deze API."),
            },
        }


class GeautomatiseerdeActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeautomatiseerdeActor
        fields = (
            "functie",
            "omschrijving",
        )


class OrganisatorischeEenheidSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisatorischeEenheid
        fields = (
            "omschrijving",
            "emailadres",
            "faxnummer",
            "telefoonnummer",
        )


class MedewerkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medewerker
        fields = (
            "functie",
            "emailadres",
            "telefoonnummer",
        )


class ObjectidentificatorSerializer(GegevensGroepSerializer):
    class Meta:
        model = Actor
        gegevensgroep = "objectidentificator"


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
            SoortActor.medewerker: MedewerkerSerializer(),
            SoortActor.geautomatiseerde_actor: GeautomatiseerdeActorSerializer(),
            SoortActor.organisatorische_eenheid: OrganisatorischeEenheidSerializer(),
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
                "help_text": _("De unieke URL van deze actor binnen deze API."),
            },
        }

    @transaction.atomic
    def create(self, validated_data):
        actor_identificatie = validated_data.pop("actor_identificatie", None)
        actor = super().create(validated_data)

        if actor_identificatie:
            serializer_class = self.discriminator.mapping[validated_data["soort_actor"]]
            serializer = serializer_class.get_fields()["actor_identificatie"]
            actor_identificatie["actor"] = actor
            serializer.create(actor_identificatie)

        return actor

    @transaction.atomic
    def update(self, instance, validated_data):
        actor_identificatie = validated_data.pop("actor_identificatie", None)
        actor = super().update(instance, validated_data)

        if actor_identificatie:
            serializer_class = self.discriminator.mapping[
                validated_data.get("soort_actor")
            ]
            serializer = serializer_class.get_fields()["actor_identificatie"]

            # remove the previous data
            model = serializer.Meta.model
            model.objects.filter(actor=actor).delete()

            actor_identificatie["actor"] = actor
            serializer.create(actor_identificatie)

        return actor
