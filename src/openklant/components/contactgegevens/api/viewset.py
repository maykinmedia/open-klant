from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from vng_api_common.pagination import DynamicPageSizePagination

from openklant.components.contactgegevens.api.serializers import (
    OrganisatieSerializer,
    PersoonSerializer,
)
from openklant.components.contactgegevens.models import Organisatie, Persoon
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions


@extend_schema(tags=["organisaties"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle organisaties opvragen.",
        description="Alle organisaties opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek organisatie opvragen.",
        description="Een specifiek organisatie opvragen.",
    ),
    create=extend_schema(
        summary="Maak een organisatie aan.",
        description="Maak een organisatie aan.",
    ),
    update=extend_schema(
        summary="Werk een organisatie in zijn geheel bij.",
        description="Werk een organisatie in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een organisatie deels bij.",
        description="Werk een organisatie deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een organisatie.",
        description="Verwijder een organisatie.",
    ),
)
class OrganisatieViewSet(viewsets.ModelViewSet):
    """De contact gegevens van een specifieke organisatie"""

    queryset = Organisatie.objects.order_by("-pk")
    serializer_class = OrganisatieSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


@extend_schema(tags=["personen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle personen opvragen.",
        description="Alle personen opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek persoon opvragen.",
        description="Een specifiek persoon opvragen.",
    ),
    create=extend_schema(
        summary="Maak een persoon aan.",
        description="Maak een persoon aan.",
    ),
    update=extend_schema(
        summary="Werk een persoon in zijn geheel bij.",
        description="Werk een persoon in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een persoon deels bij.",
        description="Werk een persoon deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een persoon.",
        description="Verwijder een persoon.",
    ),
)
class PersoonViewSet(viewsets.ModelViewSet):
    """De contact gegevens van een specifieke persoon"""

    queryset = Persoon.objects.order_by("-pk")
    serializer_class = PersoonSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
