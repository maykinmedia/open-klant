from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.filterset.partijen import (
    CategorieRelatieFilterSet,
    PartijFilterSet,
)
from openklant.components.klantinteracties.api.serializers.partijen import (
    CategorieRelatieSerializer,
    CategorieSerializer,
    PartijIdentificatorSerializer,
    PartijSerializer,
)
from openklant.components.klantinteracties.models.partijen import (
    Categorie,
    CategorieRelatie,
    Partij,
    PartijIdentificator,
)
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions
from openklant.components.utils.mixins import ExpandMixin


@extend_schema(tags=["partijen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle partijen opvragen.",
        description="Alle partijen opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek partij opvragen.",
        description="Een specifiek partij opvragen.",
    ),
    create=extend_schema(
        summary="Maak een partij aan.",
        description="Maak een partij aan.",
    ),
    update=extend_schema(
        summary="Werk een partij in zijn geheel bij.",
        description="Werk een partij in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een partij deels bij.",
        description="Werk een partij deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een partij.",
        description="Verwijder een partij.",
    ),
)
class PartijViewSet(ExpandMixin, viewsets.ModelViewSet):
    """Persoon of organisatie waarmee de gemeente een relatie heeft."""

    queryset = (
        Partij.objects.order_by("-pk")
        .select_related(
            "organisatie",
            "persoon",
            "contactpersoon",
        )
        .prefetch_related(
            "betrokkene_set",
            "digitaaladres_set",
        )
    )
    serializer_class = PartijSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filterset_class = PartijFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


@extend_schema(tags=["categorie relaties"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle categorie relaties opvragen.",
        description="Alle categorie relaties opvragen, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek categorie relatie opvragen..",
        description="Een specifiek categorie relatie opvragen, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    create=extend_schema(
        summary="Maak een categorie relatie aan.",
        description="Maak een categorie relatie aan, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    update=extend_schema(
        summary="Werk een categorie relatie in zijn geheel bij.",
        description="Werk een categorie relatie deels bij, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    partial_update=extend_schema(
        summary="Werk een categorie relatie deels bij.",
        description="Werk een categorie relatie deels bij, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    destroy=extend_schema(
        summary="Verwijder een categorie relatie.",
        description="Verwijder een categorie relatie, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
)
class CategorieRelatieViewSet(viewsets.ModelViewSet):
    """De categorie relatie van een partij, Let op: Dit endpoint is EXPERIMENTEEL."""

    queryset = CategorieRelatie.objects.order_by("-pk").select_related(
        "partij",
        "categorie",
    )
    serializer_class = CategorieRelatieSerializer
    lookup_field = "uuid"
    filterset_class = CategorieRelatieFilterSet
    pagination_class = PageNumberPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


@extend_schema(tags=["categorieën"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle categorieën opvragen.",
        description="Alle categorieën opvragen, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek categorie opvragen..",
        description="Een specifiek categorie opvragen, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    create=extend_schema(
        summary="Maak een categorie aan.",
        description="Maak een categorie aan, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    update=extend_schema(
        summary="Werk een categorie in zijn geheel bij.",
        description="Werk een categorie deels bij, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    partial_update=extend_schema(
        summary="Werk een categorie deels bij.",
        description="Werk een categorie deels bij, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    destroy=extend_schema(
        summary="Verwijder een categorie.",
        description="Verwijder een categorie, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
)
class CategorieViewSet(viewsets.ModelViewSet):
    """De categorie van een partij, Let op: Dit endpoint is EXPERIMENTEEL."""

    queryset = Categorie.objects.order_by("-pk")
    serializer_class = CategorieSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


@extend_schema(tags=["partij-identificatoren"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle partij-identificatoren opvragen.",
        description="Alle partij-identificatoren opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek partij-identificator opvragen.",
        description="Een specifiek partij-identificator opvragen.",
    ),
    create=extend_schema(
        summary="Maak een partij-identificator aan.",
        description="Maak een partij-identificator aan.",
    ),
    update=extend_schema(
        summary="Werk een partij-identificator in zijn geheel bij.",
        description="Werk een partij-identificator in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een partij-identificator deels bij.",
        description="Werk een partij-identificator deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een partij-identificator.",
        description="Verwijder een partij-identificator.",
    ),
)
class PartijIdentificatorViewSet(viewsets.ModelViewSet):
    """Gegevens die een partij in een basisregistratie of ander extern register uniek identificeren."""

    queryset = PartijIdentificator.objects.order_by("-pk").select_related("partij")
    serializer_class = PartijIdentificatorSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
