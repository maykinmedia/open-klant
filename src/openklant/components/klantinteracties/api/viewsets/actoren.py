from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.filterset.actoren import ActorenFilterSet
from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorSerializer,
)
from openklant.components.klantinteracties.models.actoren import Actor
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions


@extend_schema(tags=["actoren"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle actoren opvragen.",
        description="Alle actoren opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek actor opvragen.",
        description="Een specifiek actor opvragen.",
    ),
    create=extend_schema(
        summary="Maak een actor aan.",
        description="Maak een actor aan.",
    ),
    update=extend_schema(
        summary="Werk een actor in zijn geheel bij.",
        description="Werk een actor in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een actor deels bij.",
        description="Werk een actor deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een actor.",
        description="Verwijder een actor.",
    ),
)
class ActorViewSet(viewsets.ModelViewSet):
    """Iets dat of iemand die voor de gemeente werkzaamheden uitvoert."""

    queryset = Actor.objects.order_by("-pk").select_related(
        "geautomatiseerdeactor",
        "medewerker",
        "organisatorischeeenheid",
    )
    serializer_class = ActorSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filterset_class = ActorenFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
