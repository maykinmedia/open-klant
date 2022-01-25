from django.utils.translation import gettext_lazy as _

from django_filters import filters
from vng_api_common.filters import URLModelChoiceFilter
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_help_text

from openklant.components.contactmomenten.datamodel.models import (
    ContactMoment,
    KlantContactMoment,
    ObjectContactMoment,
)
from openklant.utils.api_spec import mark_oas_difference
from openklant.utils.filters import ExpandFilter

from .serializers import ContactMomentSerializer


class ObjectContactMomentFilter(FilterSet):
    class Meta:
        model = ObjectContactMoment
        fields = (
            "object",
            "contactmoment",
            "object_type",
        )


class ContactMomentFilter(FilterSet):
    object = filters.BaseCSVFilter(
        "objectcontactmoment__object",
        lookup_expr="in",
        help_text=_(
            mark_oas_difference(
                "De URL van het gerelateerde object "
                "(zoals vastgelegd in de OBJECTCONTACTMOMENT resource). "
                "Meerdere waardes kunnen met komma's gescheiden worden."
            )
        ),
    )
    klant = filters.BaseCSVFilter(
        "klantcontactmoment__klant",
        lookup_expr="in",
        help_text=_(
            mark_oas_difference(
                "De URL van de gerelateerde KLANT "
                "(zoals vastgelegd in de KLANTCONTACTMOMENT resource). "
                "Meerdere waardes kunnen met komma's gescheiden worden."
            )
        ),
    )
    medewerker_identificatie__identificatie = filters.CharFilter(
        field_name="medewerker_identificatie__identificatie",
        help_text=mark_oas_difference(
            get_help_text("contactmomenten.Medewerker", "identificatie")
        ),
    )
    medewerker_identificatie__achternaam = filters.CharFilter(
        field_name="medewerker_identificatie__achternaam",
        help_text=mark_oas_difference(
            get_help_text("contactmomenten.Medewerker", "achternaam")
        ),
    )
    medewerker_identificatie__voorletters = filters.CharFilter(
        field_name="medewerker_identificatie__voorletters",
        help_text=mark_oas_difference(
            get_help_text("contactmomenten.Medewerker", "voorletters")
        ),
    )
    medewerker_identificatie__voorvoegsel_achternaam = filters.CharFilter(
        field_name="medewerker_identificatie__voorvoegsel_achternaam",
        help_text=mark_oas_difference(
            get_help_text("contactmomenten.Medewerker", "voorvoegsel_achternaam")
        ),
    )
    expand = ExpandFilter(
        serializer_class=ContactMomentSerializer,
        help_text=_(
            mark_oas_difference("Haal details van inline resources direct op.")
        ),
    )
    ordering = filters.OrderingFilter(
        fields=(
            "url",
            "bronorganisatie",
            "klant",
            "registratiedatum",
            "kanaal",
            "voorkeurskanaal",
            "tekst",
            "onderwerp_links",
            "initiatiefnemer",
            "medewerker",
            "medewerker_identificatie",
        ),
        help_text=_("Het veld waarop de resultaten geordend worden."),
    )

    class Meta:
        model = ContactMoment
        fields = {
            "vorig_contactmoment": ["exact"],
            "volgend_contactmoment": ["exact"],
            "bronorganisatie": ["exact"],
            "registratiedatum": ["exact", "gt", "gte", "lt", "lte"],
            "kanaal": ["exact"],
            "voorkeurskanaal": ["exact"],
            "voorkeurstaal": ["exact"],
            "initiatiefnemer": ["exact"],
            "medewerker": ["exact"],
            "medewerker_identificatie__identificatie": ["exact"],
            "medewerker_identificatie__achternaam": ["exact"],
            "medewerker_identificatie__voorletters": ["exact"],
            "medewerker_identificatie__voorvoegsel_achternaam": ["exact"],
        }

    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        # Needed because `volgend_contactmoment` is a reverse OneToOne rel
        if f.name == "volgend_contactmoment":
            filter = URLModelChoiceFilter()
            filter.field_name = "volgend_contactmoment"
            filter.extra["help_text"] = _(
                "URL-referentie naar het volgende CONTACTMOMENT."
            )
            filter.queryset = ContactMoment.objects.all()
        else:
            filter = super().filter_for_field(f, name, lookup_expr)
        return filter


class KlantContactMomentFilter(FilterSet):
    class Meta:
        model = KlantContactMoment
        fields = ("contactmoment", "klant", "rol")
