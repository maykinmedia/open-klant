import uuid

from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from openklant.components.klantinteracties.api.serializers.partijen import (
    PartijSerializer,
)
from openklant.components.klantinteracties.models.partijen import Partij
from openklant.components.utils.filters import ExpandFilter


class PartijFilterSet(FilterSet):
    werkt_voor_partij__url = filters.CharFilter(
        help_text=_("Zoek partij object op basis van het vertegenwoordigde partij url"),
        method="filter_werkt_voor_partij_url",
    )
    werkt_voor_partij__uuid = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het vertegenwoordigde partij uuid"
        ),
        method="filter_werkt_voor_partij_uuid",
    )
    werkt_voor_partij__nummer = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het vertegenwoordigde partij nummer"
        ),
        method="filter_werkt_voor_partij_nummer",
    )

    partij_identificator__objecttype = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het partij identificator objecttype"
        ),
        method="filter_identificator_objecttype",
    )
    partij_identificator__soort_object_id = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het partij identificator soort object ID"
        ),
        method="filter_identificator_soort_object_id",
    )
    partij_identificator__object_id = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het partij identificator object ID"
        ),
        method="filter_identificator_object_id",
    )
    partij_identificator__register = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het partij identificator register"
        ),
        method="filter_identificator_register",
    )

    expand = ExpandFilter(
        serializer_class=PartijSerializer,
        help_text=_(
            "Sluit de gespecifieerde gerelateerde resources in in het antwoord."
        ),
    )

    class Meta:
        model = Partij
        fields = (
            "werkt_voor_partij__url",
            "werkt_voor_partij__uuid",
            "werkt_voor_partij__nummer",
            "partij_identificator__objecttype",
            "partij_identificator__soort_object_id",
            "partij_identificator__object_id",
            "partij_identificator__register",
            "nummer",
            "indicatie_geheimhouding",
            "indicatie_actief",
            "soort_partij",
            "bezoekadres_nummeraanduiding_id",
            "bezoekadres_adresregel1",
            "bezoekadres_adresregel2",
            "bezoekadres_adresregel3",
            "bezoekadres_land",
            "correspondentieadres_nummeraanduiding_id",
            "correspondentieadres_adresregel1",
            "correspondentieadres_adresregel2",
            "correspondentieadres_adresregel3",
            "correspondentieadres_land",
        )

    def filter_werkt_voor_partij_uuid(self, queryset, name, value):
        try:
            partij_uuid = uuid.UUID(value)
            return queryset.filter(vertegenwoordigde__uuid=partij_uuid)
        except ValueError:
            return queryset.none()

    def filter_werkt_voor_partij_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(vertegenwoordigde__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_werkt_voor_partij_nummer(self, queryset, name, value):
        try:
            return queryset.filter(vertegenwoordigde__nummer=value)
        except ValueError:
            return queryset.none()

    def filter_identificator_objecttype(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_objecttype=value
            )
        except ValueError:
            return queryset.none()

    def filter_identificator_soort_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_soort_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_identificator_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_identificator_register(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_register=value
            )
        except ValueError:
            return queryset.none()
