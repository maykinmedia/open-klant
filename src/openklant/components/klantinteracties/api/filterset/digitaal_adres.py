from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import filters
from vng_api_common.filtersets import FilterSet

from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresSerializer,
)
from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models import Klantcontrol, SoortPartij
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
        choices=Klantcontrol.choices,
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
        choices=SoortPartij.choices,
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
    soort_digitaal_adres = filters.ChoiceFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis van het soort digitaal adres "
            "dat exact gelijk moet zijn aan deze waarde."
        ),
        choices=SoortDigitaalAdres.choices,
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
    is_geverifieerd = filters.BooleanFilter(
        help_text=_(
            "Zoek digitaal adres(sen) object(en) op basis dat het een geverifieerd adres is of niet."
        ),
        method="filter_is_geverifieerd",
    )

    expand = ExpandFilter(serializer_class=DigitaalAdresSerializer)

    class Meta:
        model = DigitaalAdres
        fields = {
            "adres": ["exact", "icontains"],
            "soort_digitaal_adres": ["exact"],
            "is_standaard_adres": ["exact"],
            "omschrijving": ["exact"],
            "referentie": ["exact"],
            "verificatie_datum": ["exact", "gt", "gte", "lt", "lte"],
        }

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

    def filter_is_geverifieerd(self, queryset, name, value):
        if value:
            return queryset.filter(verificatie_datum__isnull=False)
        else:
            return queryset.filter(verificatie_datum__isnull=True)
