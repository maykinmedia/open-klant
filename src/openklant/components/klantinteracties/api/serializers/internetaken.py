from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorForeignKeySerializer,
)
from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    KlantcontactForeignKeySerializer,
)
from openklant.components.klantinteracties.api.validators import internetaak_exists
from openklant.components.klantinteracties.models.actoren import Actor
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.klantcontacten import Klantcontact


class InterneTaakForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InterneTaak
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [internetaak_exists]},
            "url": {
                "view_name": "klantinteracties:internetaak-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze interne taak binnen deze API.",
            },
        }


class InterneTaakSerializer(serializers.HyperlinkedModelSerializer):
    toegewezen_aan_actor = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Actor die een interne taak toegewezen kreeg."),
        source="actor",
    )
    aanleidinggevend_klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Klantcontact dat leidde tot een interne taak."),
        source="klantcontact",
    )

    class Meta:
        model = InterneTaak
        fields = (
            "uuid",
            "url",
            "nummer",
            "gevraagde_handeling",
            "aanleidinggevend_klantcontact",
            "toegewezen_aan_actor",
            "toelichting",
            "status",
            "toegewezen_op",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:internetaak-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze interne taak binnen deze API.",
            },
        }

    @transaction.atomic
    def create(self, validated_data):
        actor_uuid = str(validated_data.pop("actor").get("uuid"))
        klantcontact_uuid = str(validated_data.pop("klantcontact").get("uuid"))

        validated_data["actor"] = Actor.objects.get(uuid=actor_uuid)
        validated_data["klantcontact"] = Klantcontact.objects.get(
            uuid=klantcontact_uuid
        )

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        if "actor" in validated_data:
            if actor := validated_data.pop("actor", None):
                validated_data["actor"] = Actor.objects.get(uuid=str(actor.get("uuid")))

        if "klantcontact" in validated_data:
            if klantcontact := validated_data.pop("klantcontact", None):
                validated_data["klantcontact"] = Klantcontact.objects.get(
                    uuid=str(klantcontact.get("uuid"))
                )

        return super().update(instance, validated_data)


class KlantcontactInterneTaakSerializer(serializers.HyperlinkedModelSerializer):
    actor = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Actor die een interne taak toegewezen kreeg."),
    )
    klantcontact = KlantcontactForeignKeySerializer(
        read_only=True,
        allow_null=False,
        help_text=_("Klantcontact dat leidde tot een interne taak."),
    )

    class Meta:
        model = InterneTaak
        fields = (
            "uuid",
            "url",
            "nummer",
            "gevraagde_handeling",
            "actor",
            "klantcontact",
            "toelichting",
            "status",
            "toegewezen_op",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:internetaak-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze interne taak binnen deze API.",
            },
        }
