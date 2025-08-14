from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import filters
from vng_api_common.filtersets import FilterSet

from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    BetrokkeneSerializer,
    KlantcontactSerializer,
)
from openklant.components.klantinteracties.models.actoren import ActorKlantcontact
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.utils.filters import ExpandFilter, URLViewFilter


class KlantcontactDetailFilterSet(FilterSet):
    expand = ExpandFilter(serializer_class=KlantcontactSerializer)


class KlantcontactFilterSet(FilterSet):
    had_betrokkene__url = URLViewFilter(
        help_text=_("Zoek klantcontact object op basis van het betrokkene url."),
        field_name="betrokkene__uuid",
    )
    had_betrokkene__uuid = filters.UUIDFilter(
        help_text=_("Zoek klantcontact object op basis van het betrokkene uuid."),
        field_name="betrokkene__uuid",
    )
    had_betrokkene__was_partij__url = URLViewFilter(
        help_text=_("Zoek klantcontact object op basis van de partij url."),
        field_name="betrokkene__partij__uuid",
    )
    had_betrokkene__was_partij__uuid = filters.UUIDFilter(
        help_text=_("Zoek klantcontact object op basis van de partij uuid."),
        field_name="betrokkene__partij__uuid",
    )
    had_betrokkene__was_partij__partij_identificator__code_objecttype = filters.CharFilter(
        help_text=_(
            "Zoek klantcontact object op basis van het partij identificator objecttype."
        ),
        method="filter_betrokkene_partij_identificator_code_objecttype",
    )
    had_betrokkene__was_partij__partij_identificator__code_soort_object_id = filters.CharFilter(
        help_text=_(
            "Zoek klantcontact object op basis van het partij identificator soort object ID."
        ),
        method="filter_betrokkene_partij_identificator_code_soort_object_id",
    )
    had_betrokkene__was_partij__partij_identificator__object_id = filters.CharFilter(
        help_text=_(
            "Zoek klantcontact object op basis van het partij identificator object ID."
        ),
        method="filter_betrokkene_partij_identificator_object_id",
    )
    had_betrokkene__was_partij__partij_identificator__code_register = filters.CharFilter(
        help_text=_(
            "Zoek klantcontact object op basis van het partij identificator register."
        ),
        method="filter_betrokkene_partij_identificator_code_register",
    )
    onderwerpobject__url = URLViewFilter(
        help_text=_("Zoek klantcontact object op basis van het onderwerpobject url."),
        field_name="onderwerpobject__uuid",
    )
    was_onderwerpobject__url = URLViewFilter(
        help_text=_(
            "Zoek was klantcontact object op basis van het onderwerpobject url."
        ),
        field_name="was_onderwerpobject__uuid",
    )
    inhoud = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Zoek klantcontacten met specifieke tekst in inhoud."),
    )
    onderwerp = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Zoek klantcontacten met specifieke tekst in onderwerp."),
    )

    expand = ExpandFilter(serializer_class=KlantcontactSerializer)

    class Meta:
        model = Klantcontact
        fields = (
            "had_betrokkene__url",
            "had_betrokkene__uuid",
            "had_betrokkene__was_partij__url",
            "had_betrokkene__was_partij__uuid",
            "had_betrokkene__was_partij__partij_identificator__code_objecttype",
            "had_betrokkene__was_partij__partij_identificator__code_soort_object_id",
            "had_betrokkene__was_partij__partij_identificator__object_id",
            "had_betrokkene__was_partij__partij_identificator__code_register",
            "onderwerpobject__uuid",
            "onderwerpobject__url",
            "onderwerpobject__onderwerpobjectidentificator_code_objecttype",
            "onderwerpobject__onderwerpobjectidentificator_code_soort_object_id",
            "onderwerpobject__onderwerpobjectidentificator_object_id",
            "onderwerpobject__onderwerpobjectidentificator_code_register",
            "was_onderwerpobject__uuid",
            "was_onderwerpobject__url",
            "was_onderwerpobject__onderwerpobjectidentificator_code_objecttype",
            "was_onderwerpobject__onderwerpobjectidentificator_code_soort_object_id",
            "was_onderwerpobject__onderwerpobjectidentificator_object_id",
            "was_onderwerpobject__onderwerpobjectidentificator_code_register",
            "nummer",
            "kanaal",
            "onderwerp",
            "inhoud",
            "indicatie_contact_gelukt",
            "vertrouwelijk",
            "plaatsgevonden_op",
        )

    def filter_betrokkene_partij_identificator_code_objecttype(
        self, queryset, name, value
    ):
        try:
            return queryset.filter(
                betrokkene__partij__partijidentificator__partij_identificator_code_objecttype=value
            )
        except ValueError:
            return queryset.none()

    def filter_betrokkene_partij_identificator_code_soort_object_id(
        self, queryset, name, value
    ):
        try:
            return queryset.filter(
                betrokkene__partij__partijidentificator__partij_identificator_code_soort_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_betrokkene_partij_identificator_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                betrokkene__partij__partijidentificator__partij_identificator_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_betrokkene_partij_identificator_code_register(
        self, queryset, name, value
    ):
        try:
            return queryset.filter(
                betrokkene__partij__partijidentificator__partij_identificator_code_register=value
            )
        except ValueError:
            return queryset.none()


class BetrokkeneDetailFilterSet(FilterSet):
    expand = ExpandFilter(serializer_class=BetrokkeneSerializer)


class BetrokkeneFilterSet(FilterSet):
    had_klantcontact__nummer = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het klantcontact nummer"),
        method="filter_had_klantcontact_nummer",
    )
    had_klantcontact__url = URLViewFilter(
        help_text=_("Zoek betrokkene object op basis van het klantcontact url"),
        field_name="klantcontact__uuid",
    )
    had_klantcontact__uuid = filters.UUIDFilter(
        help_text=_("Zoek betrokkene object op basis van het klantcontact uuid"),
        field_name="klantcontact__uuid",
    )
    verstrektedigitaal_adres__adres = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het digitaaladres adres"),
        method="filter_digitaaladres_adres",
    )
    verstrektedigitaal_adres__url = URLViewFilter(
        help_text=_("Zoek betrokkene object op basis van het digitaaladres url"),
        field_name="digitaaladres__uuid",
    )
    verstrektedigitaal_adres__uuid = filters.UUIDFilter(
        help_text=_("Zoek betrokkene object op basis van het digitaaladres uuid"),
        field_name="digitaaladres__uuid",
    )

    was_partij__nummer = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het partij nummer"),
        method="filter_partij_nummer",
    )
    was_partij__url = URLViewFilter(
        help_text=_("Zoek betrokkene object op basis van het partij url"),
        field_name="partij__uuid",
    )
    was_partij__uuid = filters.UUIDFilter(
        help_text=_("Zoek betrokkene object op basis van het partij uuid"),
        field_name="partij__uuid",
    )
    was_partij__partij_identificator__code_objecttype = filters.CharFilter(
        help_text=_(
            "Zoek betrokkene object op basis van het partij identificator objecttype."
        ),
        method="filter_partij_identificator_code_objecttype",
    )
    was_partij__partij_identificator__code_soort_object_id = filters.CharFilter(
        help_text=_(
            "Zoek betrokkene object op basis van het partij identificator soort object ID."
        ),
        method="filter_partij_identificator_code_soort_object_id",
    )
    was_partij__partij_identificator__object_id = filters.CharFilter(
        help_text=_(
            "Zoek betrokkene object op basis van het partij identificator object ID."
        ),
        method="filter_partij_identificator_object_id",
    )
    was_partij__partij_identificator__code_register = filters.CharFilter(
        help_text=_(
            "Zoek betrokkene object op basis van het partij identificator register."
        ),
        method="filter_partij_identificator_code_register",
    )
    expand = ExpandFilter(serializer_class=BetrokkeneSerializer)

    class Meta:
        model = Betrokkene
        fields = (
            "contactnaam_voorletters",
            "contactnaam_voornaam",
            "contactnaam_voorvoegsel_achternaam",
            "contactnaam_achternaam",
            "had_klantcontact__nummer",
            "had_klantcontact__uuid",
            "had_klantcontact__url",
            "verstrektedigitaal_adres__adres",
            "verstrektedigitaal_adres__uuid",
            "verstrektedigitaal_adres__url",
            "was_partij__nummer",
            "was_partij__url",
            "was_partij__uuid",
            "was_partij__partij_identificator__code_objecttype",
            "was_partij__partij_identificator__code_soort_object_id",
            "was_partij__partij_identificator__object_id",
            "was_partij__partij_identificator__code_register",
            "organisatienaam",
        )

    def filter_had_klantcontact_nummer(self, queryset, name, value):
        try:
            return queryset.filter(klantcontact__nummer=value)
        except ValueError:
            return queryset.none()

    def filter_digitaaladres_adres(self, queryset, name, value):
        return queryset.filter(digitaaladres__adres=value)

    def filter_partij_nummer(self, queryset, name, value):
        return queryset.filter(partij__nummer=value)

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


class ActorKlantcontactFilterSet(FilterSet):
    actor__url = URLViewFilter(
        help_text=_("Zoek actor klantcontact object op basis van het actor url"),
        field_name="actor__uuid",
    )
    klantcontact__url = URLViewFilter(
        help_text=_("Zoek actor klantcontact object op basis van het klantcontact url"),
        field_name="klantcontact__uuid",
    )

    class Meta:
        model = ActorKlantcontact
        fields = (
            "actor__uuid",
            "actor__url",
            "klantcontact__uuid",
            "klantcontact__url",
        )


class OnderwerpObjectFilterSet(FilterSet):
    was_klantcontact__url = URLViewFilter(
        help_text=_("Zoek klantcontact object op basis van het klantcontact url"),
        field_name="was_klantcontact__uuid",
    )

    class Meta:
        model = Onderwerpobject
        fields = (
            "onderwerpobjectidentificator_code_objecttype",
            "onderwerpobjectidentificator_code_register",
            "onderwerpobjectidentificator_code_soort_object_id",
            "onderwerpobjectidentificator_object_id",
            "was_klantcontact__uuid",
            "was_klantcontact__url",
        )
