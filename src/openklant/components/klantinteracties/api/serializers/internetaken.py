from django.db import transaction
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema_serializer
from glom import PathAccessError, glom
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
from openklant.components.klantinteracties.models.internetaken import (
    InterneActorenThoughModel,
    InterneTaak,
)
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


@extend_schema_serializer(deprecate_fields=["toegewezen_aan_actor"])
class InterneTaakSerializer(serializers.HyperlinkedModelSerializer):
    toegewezen_aan_actor = ActorForeignKeySerializer(
        required=False,
        allow_null=False,
        help_text=_("Eerste actor die een interne taak toegewezen kreeg."),
        source="actoren.first",
        many=False,
    )
    toegewezen_aan_actoren = ActorForeignKeySerializer(
        required=False,
        allow_null=False,
        help_text=_("Actoren die een interne taak toegewezen kreeg."),
        source="actoren",
        many=True,
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
            "toegewezen_aan_actoren",
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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["toegewezen_aan_actor"] = ActorForeignKeySerializer(
            instance.actoren.order_by("interneactorenthoughmodel__order").first(),
            context={**self.context},
        ).data

        response["toegewezen_aan_actoren"] = ActorForeignKeySerializer(
            instance.actoren.all().order_by("interneactorenthoughmodel__order"),
            context={**self.context},
            many=True,
        ).data
        return response

    # TODO: remove when depricated actoren field gets removed
    def _validate_actoren(self):
        toegewezen_aan_actor = "toegewezen_aan_actor" in self.initial_data
        toegewezen_aan_actoren = "toegewezen_aan_actoren" in self.initial_data

        if toegewezen_aan_actor == toegewezen_aan_actoren:
            if toegewezen_aan_actor:
                message = _(
                    "`toegewezen_aan_actor` en `toegewezen_aan_actoren` mag niet beiden gebruikt worden."
                )
            else:
                message = _(
                    "`toegewezen_aan_actor` of `toegewezen_aan_actoren` is required (mag niet beiden gebruiken)."
                )

                # If patch don't raise required error
                if self.context.get("request").method == "PATCH":
                    return

            raise serializers.ValidationError(message)

    # TODO: remove when depricated actoren field gets removed
    def _get_actoren(self, actoren):
        if isinstance(actoren, list):
            actor_uuids = [str(actor.get("uuid")) for actor in actoren]
        else:
            actor_uuids = [glom(actoren, "first.uuid", skip_exc=PathAccessError)]

        return [Actor.objects.get(uuid=uuid) for uuid in actor_uuids]

    def validate(self, attrs):
        self._validate_actoren()
        status = attrs.get("status", None)
        if status is None and self.instance is not None:
            status = self.instance.status

        if attrs.get("afgehandeld_op") and status != Taakstatus.verwerkt:
            raise serializers.ValidationError(
                {
                    "afgehandeld_op": _(
                        "De Internetaak kan geen afgehandeld op datum bevatten "
                        "als de status niet op '{verwerkt}' staat."
                    ).format(verwerkt=Taakstatus.verwerkt)
                }
            )

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        actoren = validated_data.pop("actoren", None)
        klantcontact_uuid = str(validated_data.pop("klantcontact").get("uuid"))

        validated_data["klantcontact"] = Klantcontact.objects.get(
            uuid=klantcontact_uuid
        )

        internetaak = super().create(validated_data)
        if actoren:
            bulk_create_instances = [
                InterneActorenThoughModel(internetaak=internetaak, actor=actor)
                for actor in self._get_actoren(actoren)
            ]
            InterneActorenThoughModel.objects.bulk_create(bulk_create_instances)

        return internetaak

    @transaction.atomic
    def update(self, instance, validated_data):
        if "actoren" in validated_data:
            actoren = validated_data.pop("actoren")
            instance.actoren.clear()
            bulk_create_instances = [
                InterneActorenThoughModel(internetaak=instance, actor=actor)
                for actor in self._get_actoren(actoren)
            ]
            InterneActorenThoughModel.objects.bulk_create(bulk_create_instances)

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
                "help_text": _("De unieke URL van deze interne taak binnen deze API."),
            },
        }
