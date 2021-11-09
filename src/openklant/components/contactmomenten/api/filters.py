from django.utils.translation import ugettext_lazy as _

from django_filters import filters
from vng_api_common.filters import URLModelChoiceFilter
from vng_api_common.filtersets import FilterSet

from openklant.components.contactmomenten.datamodel.constants import Rol
from openklant.components.contactmomenten.datamodel.models import (
    ContactMoment,
    KlantContactMoment,
    ObjectContactMoment,
)


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
            "De URL van het gerelateerde object "
            "(zoals vastgelegd in de OBJECTCONTACTMOMENT resource). "
            "Meerdere waardes kunnen met komma's gescheiden worden."
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
            "ordering": ["exact"],
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
