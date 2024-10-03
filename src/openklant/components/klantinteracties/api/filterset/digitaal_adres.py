import uuid

from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresSerializer,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.utils.filters import ExpandFilter


class DigitaalAdresDetailFilterSet(FilterSet):
    expand = ExpandFilter(serializer_class=DigitaalAdresSerializer)


class DigitaalAdresFilterSet(FilterSet):
    verstrekt_door_betrokkene__uuid = filters.UUIDFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van de betrokkene uuid."
        ),
        field_name="betrokkene__uuid",
    )
    verstrekt_door_betrokkene__url = filters.CharFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van de betrokkene url."
        ),
        method="filter_betrokkene_url",
    )
    verstrekt_door_betrokkene__rol = filters.ChoiceFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van de betrokkene rol."
        ),
        field_name="betrokkene__rol",
    )
    verstrekt_door_partij__uuid = filters.UUIDFilter(
        help_text=_("Zoek digitaal adres(sen) object(en) op basis van de partij uuid."),
        field_name="betrokkene__uuid",
    )
    verstrekt_door_partij__url = filters.CharFilter(
        help_text=_("Zoek digitaal adres(sen) object(en) op basis van de partij url."),
        method="filter_partij_url",
    )
    verstrekt_door_partij__soort_partij = filters.ChoiceFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van de partij soort."
        ),
        field_name="partij__soort_partij",
    )
    adres = filters.CharFilter(
        lookup_expr="exact",
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van adres dat exact gelijk moet zijn aan deze waarde."
        ),
    )
    adres__icontains = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van adres die de opgegeven waarden bevat."
        ),
    )
    soort_digitaal_adres = filters.CharFilter(
        lookup_expr="exact",
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van het soort digitaal adres "
            "dat exact gelijk moet zijn aan deze waarde."
        ),
    )
    omschrijving = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van omschijving die de opgegeven waarden bevat."
        ),
    )

    expand = ExpandFilter(serializer_class=DigitaalAdresSerializer)

    class Meta:
        model = DigitaalAdres
        fields = (
            "verstrekt_door_betrokkene__uuid",
            "verstrekt_door_betrokkene__url",
            "verstrekt_door_betrokkene__rol",
            "verstrekt_door_partij__uuid",
            "verstrekt_door_partij__url",
            "verstrekt_door_partij__soort_partij",
            "adres",
            "adres__icontains",
            "soort_digitaal_adres",
            "omschrijving",
        )

    def filter_betrokkene_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(betrokkene__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_partij_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(partij__uuid=url_uuid)
        except ValueError:
            return queryset.none()