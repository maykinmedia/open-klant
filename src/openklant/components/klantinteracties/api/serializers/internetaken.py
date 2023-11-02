from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorForeignKeySerializer,
)
from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    KlantcontactForeignKeySerializer,
)
from openklant.components.klantinteracties.models.internetaken import InterneTaak


class InterneTaakForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InterneTaak
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True},
            "url": {
                "view_name": "internetaak-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze interne taak binnen deze API.",
            },
        }


class InterneTaakSerializer(serializers.HyperlinkedModelSerializer):
    actor = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Actor die een interne taak toegewezen kreeg."),
    )
    klantcontact = KlantcontactForeignKeySerializer(
        required=True,
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
                "view_name": "internetaak-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze interne taak binnen deze API.",
            },
        }
