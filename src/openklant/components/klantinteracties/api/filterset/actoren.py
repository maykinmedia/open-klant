from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from openklant.components.klantinteracties.models.actoren import Actor


class ActorenFilterSet(FilterSet):
    naam = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Zoek klantcontacten met specifieke tekst in inhoud"),
    )

    class Meta:
        model = Actor
        fields = (
            "naam",
            "soort_actor",
            "indicatie_actief",
            "objectidentificator_objecttype",
            "objectidentificator_soort_object_id",
            "objectidentificator_object_id",
        )
