from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.utils.filters import URLViewFilter


class InternetaakFilterSet(FilterSet):
    toegewezen_aan_actor__uuid = filters.UUIDFilter(
        help_text=_("Zoek internetaak object op basis van het toegewezen actor uuid."),
        field_name="actoren__uuid",
    )
    toegewezen_aan_actor__url = URLViewFilter(
        help_text=_("Zoek internetaak object op basis van het toegewezen actor url."),
        field_name="actoren__uuid",
    )
    aanleidinggevend_klantcontact__uuid = filters.UUIDFilter(
        help_text=_(
            "Zoek internetaak object op basis van het aanleidingevende klantcontact uuid."
        ),
        field_name="klantcontact__uuid",
    )
    aanleidinggevend_klantcontact__url = URLViewFilter(
        help_text=_(
            "Zoek internetaak object op basis van het aanleidingevende klantcontact url."
        ),
        field_name="klantcontact__uuid",
    )

    class Meta:
        model = InterneTaak
        fields = (
            "nummer",
            "status",
            "toegewezen_op",
            "actoren__naam",
            "klantcontact__uuid",
            "klantcontact__nummer",
            "toegewezen_aan_actor__uuid",
            "toegewezen_aan_actor__url",
            "aanleidinggevend_klantcontact__uuid",
            "aanleidinggevend_klantcontact__url",
        )
