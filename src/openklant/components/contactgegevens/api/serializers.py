from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.contactgegevens.models import Organisatie


class OrganisatieAdresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Organisatie
        gegevensgroep = "adres"


class OrganisatieLandSerializer(GegevensGroepSerializer):
    class Meta:
        model = Organisatie
        gegevensgroep = "land"


class OrganisatieSerializer(
    NestedGegevensGroepMixin,
    serializers.HyperlinkedModelSerializer,
):
    adres = OrganisatieAdresSerializer(
        required=False,
        allow_null=True,
        help_text=_("De adres gegevens van een organisatie"),
    )
    land = OrganisatieLandSerializer(
        required=False,
        allow_null=True,
        help_text=_("De land gegevens van een organisatie"),
    )

    class Meta:
        model = Organisatie
        fields = (
            "id",
            "url",
            "contactgegevens",
            "handelsnaam",
            "oprichtingsdatum",
            "opheffingsdatum",
            "adres",
            "land",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "contactgegevens:organisatie-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
        }
