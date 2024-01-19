import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from vng_api_common.api.views import CreateJWTSecretView as VNGCreateJWTSecretView
from vng_api_common.audittrails.viewsets import (
    AuditTrailViewSet,
    AuditTrailViewsetMixin,
)
from vng_api_common.permissions import AuthScopesRequired

from openklant.components.legacy.klanten.models.klanten import Klant

from .audits import AUDIT_KLANTEN
from .filters import KlantFilter
from .kanalen import KANAAL_KLANTEN
from .scopes import (
    SCOPE_KLANTEN_AANMAKEN,
    SCOPE_KLANTEN_ALLES_LEZEN,
    SCOPE_KLANTEN_ALLES_VERWIJDEREN,
    SCOPE_KLANTEN_BIJWERKEN,
)
from .serializers import KlantSerializer

logger = logging.getLogger(__name__)


@extend_schema(tags=["klanten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle KLANTen opvragen.",
        description="Alle KLANTen opvragen.",
        auth=[{"JWT-Claims": ["klanten.lezen"]}],
    ),
    retrieve=extend_schema(
        summary="Een specifiek KLANT opvragen.",
        description="Een specifiek KLANT opvragen.",
        auth=[{"JWT-Claims": ["klanten.lezen"]}],
    ),
    update=extend_schema(
        summary="Werk een KLANT in zijn geheel bij.",
        description="Werk een KLANT in zijn geheel bij.",
        auth=[{"JWT-Claims": ["klanten.bijwerken"]}],
    ),
    partial_update=extend_schema(
        summary="Werk een KLANT deels bij.",
        description="Werk een KLANT deels bij.",
        auth=[{"JWT-Claims": ["klanten.bijwerken"]}],
    ),
    create=extend_schema(
        summary="Maak een KLANT aan.",
        description="Maak een KLANT aan.",
        auth=[{"JWT-Claims": ["klanten.aanmaken"]}],
    ),
    destroy=extend_schema(
        summary="Verwijder een KLANT.",
        description="Verwijder een KLANT.",
        auth=[{"JWT-Claims": ["klanten.verwijderen"]}],
    ),
)
class KlantViewSet(
    NotificationViewSetMixin, AuditTrailViewsetMixin, viewsets.ModelViewSet
):
    """
    Opvragen en bewerken van KLANTen.

    Een KLANT is een eenvoudige weergave van een NATUURLIJK PERSOON of
    VESTIGING waarbij het gaat om niet geverifieerde gegevens. Om deze reden
    zijn ook alle attributen optioneel.

    Indien de KLANT geverifieerd is mag een relatie gelegd worden met een
    NATUURLIJK PERSOON of VESTIGING  middels het attribuut `subject` of, indien
    er geen API beschikbaar is voor deze objecten, middels
    `subjectIdentificatie`.
    """

    queryset = Klant.objects.order_by("-pk")
    serializer_class = KlantSerializer
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    filterset_class = KlantFilter
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_KLANTEN_ALLES_LEZEN,
        "retrieve": SCOPE_KLANTEN_ALLES_LEZEN,
        "create": SCOPE_KLANTEN_AANMAKEN,
        "update": SCOPE_KLANTEN_BIJWERKEN,
        "partial_update": SCOPE_KLANTEN_BIJWERKEN,
        "destroy": SCOPE_KLANTEN_ALLES_VERWIJDEREN,
    }
    notifications_kanaal = KANAAL_KLANTEN
    audit = AUDIT_KLANTEN


@extend_schema(tags=["klanten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle audit trail regels behorend bij de KLANT.",
        description="Alle audit trail regels behorend bij de KLANT.",
        auth=[{"JWT-Claims": ["audittrails.lezen"]}],
    ),
    retrieve=extend_schema(
        summary="Een specifieke audit trail regel opvragen.",
        description="Een specifieke audit trail regel opvragen.",
        auth=[{"JWT-Claims": ["audittrails.lezen"]}],
    ),
)
class KlantAuditTrailViewSet(AuditTrailViewSet):
    """Opvragen van de audit trail regels."""

    main_resource_lookup_field = "klant_uuid"

    def initialize_request(self, request, *args, **kwargs):
        # workaround for drf-nested-viewset injecting the URL kwarg into request.data
        return super(viewsets.GenericViewSet, self).initialize_request(
            request, *args, **kwargs
        )


@extend_schema(exclude=True)
class CreateJWTSecretView(VNGCreateJWTSecretView):
    pass
