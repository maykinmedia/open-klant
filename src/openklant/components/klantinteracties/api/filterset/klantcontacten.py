import uuid

from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    KlantcontactSerializer,
)
from openklant.components.klantinteracties.models.actoren import ActorKlantcontact
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Klantcontact,
)
from openklant.components.utils.filters import ExpandFilter


class KlantcontactDetailFilterSet(FilterSet):
    expand = ExpandFilter(
        serializer_class=KlantcontactSerializer,
        help_text=_(
            "Sluit de gespecifieerde gerelateerde resources in in het antwoord."
        ),
    )


class KlantcontactFilterSet(FilterSet):
    had_betrokkene__url = filters.CharFilter(
        help_text=_("Zoek klantcontact object op basis van het betrokkene url"),
        method="filter_betrokkene_url",
    )
    had_betrokkene__uuid = filters.UUIDFilter(
        help_text=_("Zoek klantcontact object op basis van het betrokkene uuid"),
        field_name="betrokkene__uuid",
    )
    onderwerpobject__url = filters.CharFilter(
        help_text=_("Zoek klantcontact object op basis van het onderwerpobject url"),
        method="filter_onderwerpobject_url",
    )
    was_onderwerpobject__url = filters.CharFilter(
        help_text=_(
            "Zoek was klantcontact object op basis van het onderwerpobject url"
        ),
        method="filter_was_onderwerpobject_url",
    )
    inhoud = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Zoek klantcontacten met specifieke tekst in inhoud"),
    )
    onderwerp = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Zoek klantcontacten met specifieke tekst in onderwerp"),
    )

    expand = ExpandFilter(
        serializer_class=KlantcontactSerializer,
        help_text=_(
            "Sluit de gespecifieerde gerelateerde resources in in het antwoord."
        ),
    )

    class Meta:
        model = Klantcontact
        fields = (
            "had_betrokkene__url",
            "had_betrokkene__uuid",
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

    def filter_betrokkene_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(betrokkene__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_onderwerpobject_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(onderwerpobject__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_was_onderwerpobject_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(was_onderwerpobject__uuid=url_uuid)
        except ValueError:
            return queryset.none()


class BetrokkeneFilterSet(FilterSet):
    had_klantcontact__nummer = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het klantcontact nummer"),
        method="filter_had_klantcontact_nummer",
    )
    had_klantcontact__url = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het klantcontact url"),
        method="filter_had_klantcontact_url",
    )
    had_klantcontact__uuid = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het klantcontact uuid"),
        method="filter_had_klantcontact_uuid",
    )
    verstrektedigitaal_adres__adres = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het digitaaladres adres"),
        method="filter_digitaaladres_adres",
    )
    verstrektedigitaal_adres__url = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het digitaaladres url"),
        method="filter_digitaaladres_url",
    )
    verstrektedigitaal_adres__uuid = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het digitaaladres uuid"),
        method="filter_digitaaladres_uuid",
    )

    was_partij__nummer = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het partij nummer"),
        method="filter_partij_nummer",
    )
    was_partij__url = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het partij url"),
        method="filter_partij_url",
    )
    was_partij__uuid = filters.CharFilter(
        help_text=_("Zoek betrokkene object op basis van het partij uuid"),
        method="filter_partij_uuid",
    )

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
            "organisatienaam",
        )

    def filter_had_klantcontact_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(klantcontact__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_had_klantcontact_uuid(self, queryset, name, value):
        try:
            klantcontact_uuid = uuid.UUID(value)
            return queryset.filter(klantcontact__uuid=klantcontact_uuid)
        except ValueError:
            return queryset.none()

    def filter_had_klantcontact_nummer(self, queryset, name, value):
        try:
            return queryset.filter(klantcontact__nummer=value)
        except ValueError:
            return queryset.none()

    def filter_digitaaladres_adres(self, queryset, name, value):
        return queryset.filter(digitaaladres__adres=value)

    def filter_digitaaladres_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(digitaaladres__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_digitaaladres_uuid(self, queryset, name, value):
        try:
            digitaaladres_uuid = uuid.UUID(value)
            return queryset.filter(digitaaladres__uuid=digitaaladres_uuid)
        except ValueError:
            return queryset.none()

    def filter_partij_nummer(self, queryset, name, value):
        return queryset.filter(partij__nummer=value)

    def filter_partij_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(partij__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_partij_uuid(self, queryset, name, value):
        try:
            partij_uuid = uuid.UUID(value)
            return queryset.filter(partij__uuid=partij_uuid)
        except ValueError:
            return queryset.none()


class ActorKlantcontactFilterSet(FilterSet):
    actor__url = filters.CharFilter(
        help_text=_("Zoek actor klantcontract object op basis van het actor url"),
        method="filter_actor_url",
    )
    klantcontact__url = filters.CharFilter(
        help_text=_(
            "Zoek actor klantcontract object op basis van het klantcontact url"
        ),
        method="filter_klantcontact_url",
    )

    class Meta:
        model = ActorKlantcontact
        fields = (
            "actor__uuid",
            "actor__url",
            "klantcontact__uuid",
            "klantcontact__url",
        )

    def filter_actor_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(actor__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_klantcontact_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.split("/")[-1])
            return queryset.filter(klantcontact__uuid=url_uuid)
        except ValueError:
            return queryset.none()
