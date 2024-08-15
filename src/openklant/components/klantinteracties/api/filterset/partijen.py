import uuid

from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from openklant.components.klantinteracties.api.serializers.partijen import (
    PartijSerializer,
)
from openklant.components.klantinteracties.models.partijen import (
    CategorieRelatie,
    Partij,
    Vertegenwoordigden,
)
from openklant.components.utils.filters import ExpandFilter


class PartijDetailFilterSet(FilterSet):
    expand = ExpandFilter(serializer_class=PartijSerializer)


class PartijFilterSet(FilterSet):
    vertegenwoordigde_partij__uuid = filters.UUIDFilter(
        help_text=_(
            "Zoek partij object op basis van het vertegenwoordigde partij uuid."
        ),
        field_name="vertegenwoordigde__vertegenwoordigende_partij__uuid",
    )
    vertegenwoordigde_partij__url = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het vertegenwoordigde partij url."
        ),
        method="filter_vertegenwoordigde_partij_url",
    )
    partij_identificator__code_objecttype = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het partij identificator objecttype."
        ),
        method="filter_identificator_code_objecttype",
    )
    partij_identificator__code_soort_object_id = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het partij identificator soort object ID."
        ),
        method="filter_identificator_code_soort_object_id",
    )
    partij_identificator__object_id = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het partij identificator object ID."
        ),
        method="filter_identificator_object_id",
    )
    partij_identificator__code_register = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het partij identificator register."
        ),
        method="filter_identificator_code_register",
    )

    categorierelatie__categorie__naam = filters.CharFilter(
        help_text=_("Zoek partij object op basis van categorie namen."),
        method="filter_categorierelatie_categorie_naam",
    )

    expand = ExpandFilter(serializer_class=PartijSerializer)

    class Meta:
        model = Partij
        fields = (
            "vertegenwoordigde_partij__uuid",
            "vertegenwoordigde_partij__url",
            "partij_identificator__code_objecttype",
            "partij_identificator__code_soort_object_id",
            "partij_identificator__object_id",
            "partij_identificator__code_register",
            "categorierelatie__categorie__naam",
            "nummer",
            "indicatie_geheimhouding",
            "indicatie_actief",
            "soort_partij",
            "bezoekadres_nummeraanduiding_id",
            "bezoekadres_adresregel1",
            "bezoekadres_adresregel2",
            "bezoekadres_adresregel3",
            "bezoekadres_land",
            "correspondentieadres_nummeraanduiding_id",
            "correspondentieadres_adresregel1",
            "correspondentieadres_adresregel2",
            "correspondentieadres_adresregel3",
            "correspondentieadres_land",
        )

    def filter_vertegenwoordigde_partij_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(
                vertegenwoordigde__vertegenwoordigende_partij__uuid=url_uuid
            )
        except ValueError:
            return queryset.none()

    def filter_identificator_code_objecttype(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_code_objecttype=value
            )
        except ValueError:
            return queryset.none()

    def filter_identificator_code_soort_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_code_soort_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_identificator_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_identificator_code_register(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_code_register=value
            )
        except ValueError:
            return queryset.none()

    def filter_categorierelatie_categorie_naam(self, queryset, name, value):
        categorie_namen = value.split(",")
        try:
            return queryset.filter(
                categorierelatie__categorie__naam__in=categorie_namen
            )
        except ValueError:
            return queryset.none()


class VertegenwoordigdenFilterSet(FilterSet):
    vertegenwoordigende_partij__url = filters.CharFilter(
        help_text=_(
            "Zoek Vertegenwoordigden object op basis van het vertegenwoordigende partij url."
        ),
        method="filter_vertegenwoordigende_partij_url",
    )
    vertegenwoordigde_partij__url = filters.CharFilter(
        help_text=_(
            "Zoek Vertegenwoordigden object op basis van het vertegenwoordigde partij url."
        ),
        method="filter_vertegenwoordigde_partij_url",
    )

    class Meta:
        model = Vertegenwoordigden
        fields = (
            "vertegenwoordigende_partij__uuid",
            "vertegenwoordigende_partij__url",
            "vertegenwoordigde_partij__uuid",
            "vertegenwoordigde_partij__url",
        )

    def filter_vertegenwoordigende_partij_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(vertegenwoordigende_partij__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_vertegenwoordigde_partij_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(vertegenwoordigde_partij__uuid=url_uuid)
        except ValueError:
            return queryset.none()


class CategorieRelatieFilterSet(FilterSet):
    partij__url = filters.CharFilter(
        help_text=_("Zoek categorie relatie object op basis van de partij url."),
        method="filter_partij_url",
    )
    partij__uuid = filters.CharFilter(
        help_text=_("Zoek categorie relatie object op basis van de partij uuid."),
        method="filter_partij_uuid",
    )
    partij__nummer = filters.CharFilter(
        help_text=_("Zoek categorie relatie object op basis van het partij nummer."),
        method="filter_partij_nummer",
    )
    categorie__naam = filters.CharFilter(
        help_text=_("Zoek categorie relatie object op basis van de categorie naam."),
        method="filter_categorie_naam",
    )
    categorie__uuid = filters.CharFilter(
        help_text=_("Zoek categorie relatie object op basis van de categorie uuid."),
        method="filter_categorie_uuid",
    )
    categorie__url = filters.CharFilter(
        help_text=_("Zoek categorie relatie object op basis van de categorie url."),
        method="filter_categorie_url",
    )

    class Meta:
        model = CategorieRelatie
        fields = (
            "partij__url",
            "partij__uuid",
            "partij__nummer",
            "categorie__url",
            "categorie__uuid",
            "categorie__naam",
            "begin_datum",
            "eind_datum",
        )

    def filter_partij_uuid(self, queryset, name, value):
        try:
            partij_uuid = uuid.UUID(value)
            return queryset.filter(partij__uuid=partij_uuid)
        except ValueError:
            return queryset.none()

    def filter_partij_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(partij__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_partij_nummer(self, queryset, name, value):
        try:
            return queryset.filter(partij__nummer=value)
        except ValueError:
            return queryset.none()

    def filter_categorie_uuid(self, queryset, name, value):
        try:
            categorie_uuid = uuid.UUID(value)
            return queryset.filter(categorie__uuid=categorie_uuid)
        except ValueError:
            return queryset.none()

    def filter_categorie_url(self, queryset, name, value):
        try:
            url_uuid = uuid.UUID(value.rstrip("/").split("/")[-1])
            return queryset.filter(categorie__uuid=url_uuid)
        except ValueError:
            return queryset.none()

    def filter_categorie_naam(self, queryset, name, value):
        try:
            return queryset.filter(categorie__naam=value)
        except ValueError:
            return queryset.none()
