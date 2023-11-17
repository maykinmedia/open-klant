from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from openklant.components.contactgegevens.models import (
    Organisatie,
    Persoon,
)


class OrganisatieFilterSet(FilterSet):
    contactgegevens__url = filters.CharFilter(
        help_text=_("Zoek organisatie object op basis van de contactgegevens url."),
        method="filter_url",
    )
    contactgegevens__id = filters.CharFilter(
        help_text=_("Zoek organisatie object op basis van de contactgegevens ID."),
        method="filter_id",
    )

    class Meta:
        model = Organisatie
        fields = ("contactgegevens__url", "contactgegevens__id")

    def filter_id(self, queryset, name, value):
        try:
            return queryset.filter(contactgegevens__id=value)
        except ValueError:
            return queryset.none()

    def filter_url(self, queryset, name, value):
        try:
            id = value.split("/")[-1]
            return queryset.filter(contactgegevens__id=id)
        except ValueError:
            return queryset.none()


class PersoonFilterSet(FilterSet):
    contactgegevens__url = filters.CharFilter(
        help_text=_("Zoek persoon object op basis van de contactgegevens url."),
        method="filter_url",
    )
    contactgegevens__id = filters.CharFilter(
        help_text=_("Zoek persoon object op basis van de contactgegevens ID."),
        method="filter_id",
    )

    class Meta:
        model = Persoon
        fields = ("contactgegevens__url", "contactgegevens__id")

    def filter_id(self, queryset, name, value):
        try:
            return queryset.filter(contactgegevens__id=value)
        except ValueError:
            return queryset.none()

    def filter_url(self, queryset, name, value):
        try:
            id = value.split("/")[-1]
            return queryset.filter(contactgegevens__id=id)
        except ValueError:
            return queryset.none()
