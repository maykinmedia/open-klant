from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import filters
from vng_api_common.filtersets import FilterSet

from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresSerializer,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.utils.filters import ExpandFilter, URLViewFilter


class DigitaalAdresDetailFilterSet(FilterSet):
    expand = ExpandFilter(serializer_class=DigitaalAdresSerializer)


class DigitaalAdresFilterSet(FilterSet):
    verstrekt_door_betrokkene__uuid = filters.UUIDFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van de betrokkene uuid."
        ),
        field_name="betrokkene__uuid",
    )
    verstrekt_door_betrokkene__url = URLViewFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van de betrokkene url."
        ),
        field_name="betrokkene__uuid",
    )
    verstrekt_door_betrokkene__rol = filters.ChoiceFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van de betrokkene rol."
        ),
        field_name="betrokkene__rol",
    )
    verstrekt_door_partij__uuid = filters.UUIDFilter(
        help_text=_("Zoek digitaal adres(sen) object(en) op basis van de partij uuid."),
        field_name="partij__uuid",
    )
    verstrekt_door_partij__url = URLViewFilter(
        help_text=_("Zoek digitaal adres(sen) object(en) op basis van de partij url."),
        field_name="partij__uuid",
    )
    verstrekt_door_partij__soort_partij = filters.ChoiceFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van de partij soort."
        ),
        field_name="partij__soort_partij",
    )
    verstrekt_door_partij__partij_identificator__code_objecttype = filters.CharFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van het partij identificator objecttype."
        ),
        method="filter_partij_identificator_code_objecttype",
    )
    verstrekt_door_partij__partij_identificator__code_soort_object_id = filters.CharFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van het partij identificator soort object ID."
        ),
        method="filter_partij_identificator_code_soort_object_id",
    )
    verstrekt_door_partij__partij_identificator__object_id = filters.CharFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van het partij identificator object ID."
        ),
        method="filter_partij_identificator_object_id",
    )
    verstrekt_door_partij__partij_identificator__code_register = filters.CharFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van het partij identificator register."
        ),
        method="filter_partij_identificator_code_register",
    )
    adres = filters.CharFilter(
        lookup_expr="exact",
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van adres dat exact gelijk moet zijn aan deze waarde."
        ),
    )
    adres__icontains = filters.CharFilter(
        field_name="adres",
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
    is_standaard_adres = filters.BooleanFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis dat het een standaard adres is of niet."
        ),
    )
    omschrijving = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van omschijving die de opgegeven waarden bevat."
        ),
    )
    referentie = filters.CharFilter(
        lookup_expr="exact", help_text="Filter op exacte referentiewaarde."
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
            "verstrekt_door_partij__partij_identificator__code_objecttype",
            "verstrekt_door_partij__partij_identificator__code_soort_object_id",
            "verstrekt_door_partij__partij_identificator__object_id",
            "verstrekt_door_partij__partij_identificator__code_register",
            "adres",
            "adres__icontains",
            "soort_digitaal_adres",
            "is_standaard_adres",
            "omschrijving",
            "referentie",
        )

    def filter_partij_identificator_code_objecttype(self, queryset, name, value):
        try:
            return queryset.filter(
                partij__partijidentificator__partij_identificator_code_objecttype=value
            )
        except ValueError:
            return queryset.none()

    def filter_partij_identificator_code_soort_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                partij__partijidentificator__partij_identificator_code_soort_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_partij_identificator_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                partij__partijidentificator__partij_identificator_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_partij_identificator_code_register(self, queryset, name, value):
        try:
            return queryset.filter(
                partij__partijidentificator__partij_identificator_code_register=value
            )
        except ValueError:
            return queryset.none()
