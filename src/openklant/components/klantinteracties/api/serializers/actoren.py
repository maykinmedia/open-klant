from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin
from vng_api_common.polymorphism import Discriminator, PolymorphicSerializer

from openklant.components.klantinteracties.api.validators import actor_exists
from openklant.components.klantinteracties.models.actoren import (
    Actor,
    GeautomatiseerdeActor,
    Medewerker,
    OrganisatorischeEenheid,
)
from openklant.components.klantinteracties.models.constants import SoortActor


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
    PolymorphicSerializer,
):
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
    objectidentificator = ObjectidentificatorSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Gegevens die een onderwerpobject in een extern register uniek identificeren."
        ),
    )
    actor_type = serializers.ChoiceField(
        source="soort_actor",
        choices=SoortActor.choices,
        required=True,
        help_text="Geeft aan van welke specifieke soort actor sprake is.",
    )

    class Meta:
        model = Actor
        fields = (
            "uuid",
            "naam",
            "actor_type",
            "indicatie_actief",
            "objectidentificator",
        )
        extra_kwargs = {"uuid": {"read_only": True}}
