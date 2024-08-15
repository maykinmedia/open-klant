import uuid

from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from openklant.components.klantinteracties.models.internetaken import InterneTaak


class InternetaakFilterSet(FilterSet):
    toegewezen_aan_actor__uuid = filters.UUIDFilter(
        help_text=_("Zoek internetaak object op basis van het toegewezen actor uuid."),
        field_name="actor__uuid",
    )
    toegewezen_aan_actor__url = filters.CharFilter(
        help_text=_("Zoek internetaak object op basis van het toegewezen actor url."),
        method="filter_toegewezen_aan_actor_url",
    )
    aanleidinggevend_klantcontact__uuid = filters.UUIDFilter(
        help_text=_(
            "Zoek internetaak object op basis van het aanleidingevende klantcontact uuid."
        ),
        field_name="klantcontact__uuid",
    )
    aanleidinggevend_klantcontact__url = filters.CharFilter(
        help_text=_(
            "Zoek internetaak object op basis van het aanleidingevende klantcontact url."
        ),
        method="filter_aanleidinggevend_klantcontact_url",
    )

    class Meta:
        model = InterneTaak
        fields = (
            "nummer",
            "status",
            "toegewezen_op",
            "actor__naam",
            "klantcontact__uuid",
            "klantcontact__nummer",
            "toegewezen_aan_actor__uuid",
            "toegewezen_aan_actor__url",
            "aanleidinggevend_klantcontact__uuid",
            "aanleidinggevend_klantcontact__url",
        )

    def filter_toegewezen_aan_actor_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(actor__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_aanleidinggevend_klantcontact_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(klantcontact__uuid=url_uuid)
        except ValueError:
            return queryset.none()
