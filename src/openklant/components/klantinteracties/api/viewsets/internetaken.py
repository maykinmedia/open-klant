from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.serializers.internetaken import (
    InterneTaakSerializer,
)
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions


@extend_schema(tags=["interne taken"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle interne taken opvragen.",
        description="Alle interne taken opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek interne taak opvragen.",
        description="Een specifiek interne taak opvragen.",
    ),
    create=extend_schema(
        summary="Maak een interne taak aan.",
        description="Maak een interne taak aan.",
    ),
    update=extend_schema(
        summary="Werk een interne taak in zijn geheel bij.",
        description="Werk een interne taak in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een interne taak deels bij.",
        description="Werk een interne taak deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een interne taak.",
        description="Verwijder een interne taak.",
    ),
)
class InterneTaakViewSet(viewsets.ModelViewSet):
    """Iets dat door een actor moet worden gedaan om opvolging te geven aan een klantcontact."""

    queryset = InterneTaak.objects.order_by("-pk").select_related(
        "actor",
        "klantcontact",
    )
    serializer_class = InterneTaakSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "nummer",
        "status",
        "actor__naam",
        "klantcontact__uuid",
        "klantcontact__nummer",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
