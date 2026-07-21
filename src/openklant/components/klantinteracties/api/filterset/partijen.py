from django.db.models import Exists, OuterRef
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import filters
from vng_api_common.filtersets import FilterSet

from openklant.components.klantinteracties.api.serializers.partijen import (
    PartijSerializer,
)
from openklant.components.klantinteracties.models.partijen import (
    CategorieRelatie,
    Partij,
    PartijIdentificator,
    Vertegenwoordigden,
)
from openklant.components.utils.filters import ExpandFilter, URLViewFilter


class PartijDetailFilterSet(FilterSet):
    expand = ExpandFilter(serializer_class=PartijSerializer)


class PartijFilterSet(FilterSet):
    vertegenwoordigde_partij__uuid = filters.UUIDFilter(
        help_text=_(
            "Zoek partij object op basis van het vertegenwoordigde partij uuid."
        ),
        field_name="vertegenwoordigde__vertegenwoordigende_partij__uuid",
    )
    vertegenwoordigde_partij__url = URLViewFilter(
        help_text=_(
            "Zoek partij object op basis van het vertegenwoordigde partij url."
        ),
        field_name="vertegenwoordigde__vertegenwoordigende_partij__uuid",
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
    sub_identificator_van__object_id = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het ``subIdentificatorVan`` object ID. "
            "Deze parameter kan gecombineerd worden met de ``partijIdentificator__`` "
            "parameters om een specifieke vestiging te vinden, door bij ``partijIdentificator__`` "
            "de vestigingspecifieke informatie mee te geven en bij ``subIdentificatorVan__`` "
            "de informatie van de rechtspersoon waaraan deze vestiging gekoppeld is."
        ),
        method="filter_sub_identificator_object_id",
    )
    sub_identificator_van__code_objecttype = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het ``subIdentificatorVan`` objecttype. "
            "Deze parameter kan gecombineerd worden met de ``partijIdentificator__`` "
            "parameters om een specifieke vestiging te vinden, door bij ``partijIdentificator__`` "
            "de vestigingspecifieke informatie mee te geven en bij ``subIdentificatorVan__`` "
            "de informatie van de rechtspersoon waaraan deze vestiging gekoppeld is."
        ),
        method="filter_sub_identificator_code_objecttype",
    )
    sub_identificator_van__code_soort_object_id = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het ``subIdentificatorVan`` soort object ID. "
            "Deze parameter kan gecombineerd worden met de ``partijIdentificator__`` "
            "parameters om een specifieke vestiging te vinden, door bij ``partijIdentificator__`` "
            "de vestigingspecifieke informatie mee te geven en bij ``subIdentificatorVan__`` "
            "de informatie van de rechtspersoon waaraan deze vestiging gekoppeld is."
        ),
        method="filter_sub_identificator_code_soort_object_id",
    )
    sub_identificator_van__code_register = filters.CharFilter(
        help_text=_(
            "Zoek partij object op basis van het ``subIdentificatorVan`` register. "
            "Deze parameter kan gecombineerd worden met de ``partijIdentificator__`` "
            "parameters om een specifieke vestiging te vinden, door bij ``partijIdentificator__`` "
            "de vestigingspecifieke informatie mee te geven en bij ``subIdentificatorVan__`` "
            "de informatie van de rechtspersoon waaraan deze vestiging gekoppeld is."
        ),
        method="filter_sub_identificator_code_register",
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
            "sub_identificator_van__code_objecttype",
            "sub_identificator_van__code_soort_object_id",
            "sub_identificator_van__object_id",
            "sub_identificator_van__code_register",
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

    def filter_identificator_code_objecttype(self, queryset, name, value):
        subquery = PartijIdentificator.objects.filter(
            partij_id=OuterRef("pk"),
            partij_identificator_code_objecttype=value,
        )
        return queryset.filter(Exists(subquery))

    def filter_identificator_code_soort_object_id(self, queryset, name, value):
        # No Exists() needed: (partij, code_soort_object_id) is unique per partij
        try:
            return queryset.filter(
                partijidentificator__partij_identificator_code_soort_object_id=value
            )
        except ValueError:
            return queryset.none()

    def filter_identificator_object_id(self, queryset, name, value):
        subquery = PartijIdentificator.objects.filter(
            partij_id=OuterRef("pk"),
            partij_identificator_object_id=value,
        )
        return queryset.filter(Exists(subquery))

    def filter_identificator_code_register(self, queryset, name, value):
        subquery = PartijIdentificator.objects.filter(
            partij_id=OuterRef("pk"),
            partij_identificator_code_register=value,
        )
        return queryset.filter(Exists(subquery))

    def filter_categorierelatie_categorie_naam(self, queryset, name, value):
        categorie_namen = value.split(",")
        subquery = CategorieRelatie.objects.filter(
            partij_id=OuterRef("pk"),
            categorie__naam__in=categorie_namen,
        )
        return queryset.filter(Exists(subquery))

    def filter_sub_identificator_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__sub_identificator_van__partij_identificator_object_id=value
            ).distinct()
        except ValueError:
            return queryset.none()

    def filter_sub_identificator_code_objecttype(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__sub_identificator_van__partij_identificator_code_objecttype=value
            ).distinct()
        except ValueError:
            return queryset.none()

    def filter_sub_identificator_code_soort_object_id(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__sub_identificator_van__partij_identificator_code_soort_object_id=value
            ).distinct()
        except ValueError:
            return queryset.none()

    def filter_sub_identificator_code_register(self, queryset, name, value):
        try:
            return queryset.filter(
                partijidentificator__sub_identificator_van__partij_identificator_code_register=value
            ).distinct()
        except ValueError:
            return queryset.none()


class VertegenwoordigdenFilterSet(FilterSet):
    vertegenwoordigende_partij__url = URLViewFilter(
        help_text=_(
            "Zoek Vertegenwoordigden object op basis van het vertegenwoordigende partij url."
        ),
        field_name="vertegenwoordigende_partij__uuid",
    )
    vertegenwoordigde_partij__url = URLViewFilter(
        help_text=_(
            "Zoek Vertegenwoordigden object op basis van het vertegenwoordigde partij url."
        ),
        field_name="vertegenwoordigde_partij__uuid",
    )

    class Meta:
        model = Vertegenwoordigden
        fields = (
            "vertegenwoordigende_partij__uuid",
            "vertegenwoordigende_partij__url",
            "vertegenwoordigde_partij__uuid",
            "vertegenwoordigde_partij__url",
        )


class CategorieRelatieFilterSet(FilterSet):
    partij__url = URLViewFilter(
        help_text=_("Zoek categorie relatie object op basis van de partij url."),
        field_name="partij__uuid",
    )
    partij__uuid = filters.UUIDFilter(
        help_text=_("Zoek categorie relatie object op basis van de partij uuid."),
    )
    partij__nummer = filters.CharFilter(
        help_text=_("Zoek categorie relatie object op basis van het partij nummer."),
        method="filter_partij_nummer",
    )
    categorie__naam = filters.CharFilter(
        help_text=_("Zoek categorie relatie object op basis van de categorie naam."),
        method="filter_categorie_naam",
    )
    categorie__uuid = filters.UUIDFilter(
        help_text=_("Zoek categorie relatie object op basis van de categorie uuid."),
    )
    categorie__url = URLViewFilter(
        help_text=_("Zoek categorie relatie object op basis van de categorie url."),
        field_name="categorie__uuid",
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

    def filter_partij_nummer(self, queryset, name, value):
        try:
            return queryset.filter(partij__nummer=value)
        except ValueError:
            return queryset.none()

    def filter_categorie_naam(self, queryset, name, value):
        try:
            return queryset.filter(categorie__naam=value)
        except ValueError:
            return queryset.none()
