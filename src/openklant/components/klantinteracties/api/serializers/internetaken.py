from django.db import transaction
from django.utils import timezone
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
from openklant.components.klantinteracties.models.constants import Taakstatus
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
                "help_text": _("De unieke URL van deze interne taak binnen deze API."),
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
            "afgehandeld_op",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:internetaak-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze interne taak binnen deze API."),
            },
        }

    def validate(self, attrs):
        status = attrs.get("status", None)
        if not status and self.instance:
            status = self.instance.status

        if attrs.get("afgehandeld_op") and status == Taakstatus.te_verwerken.value:
            raise serializers.ValidationError(
                {
                    "afgehandeld_op": _(
                        "De Internetaak kan geen afgehandeld op datum bevatten "
                        "als de status nog in '{te_verwerken}' staat."
                    ).format(te_verwerken=Taakstatus.te_verwerken.value)
                }
            )

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        actor_uuid = str(validated_data.pop("actor").get("uuid"))
        klantcontact_uuid = str(validated_data.pop("klantcontact").get("uuid"))
        afgehandeld_op = validated_data.pop("afgehandeld_op", timezone.now())

        validated_data["actor"] = Actor.objects.get(uuid=actor_uuid)
        validated_data["klantcontact"] = Klantcontact.objects.get(
            uuid=klantcontact_uuid
        )

        if validated_data.get("status") == Taakstatus.verwerkt:
            validated_data["afgehandeld_op"] = afgehandeld_op

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        afgehandeld_op = validated_data.pop("afgehandeld_op", timezone.now())

        if "actor" in validated_data:
            if actor := validated_data.pop("actor", None):
                validated_data["actor"] = Actor.objects.get(uuid=str(actor.get("uuid")))

        if "klantcontact" in validated_data:
            if klantcontact := validated_data.pop("klantcontact", None):
                validated_data["klantcontact"] = Klantcontact.objects.get(
                    uuid=str(klantcontact.get("uuid"))
                )

        if (
            not self.instance.afgehandeld_op
            and validated_data.get("status") == Taakstatus.verwerkt
        ):
            validated_data["afgehandeld_op"] = afgehandeld_op

        if (
            self.instance.afgehandeld_op
            and validated_data.get("status") == Taakstatus.te_verwerken
        ):
            validated_data["afgehandeld_op"] = None

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
                "help_text": _("De unieke URL van deze interne taak binnen deze API."),
            },
        }
