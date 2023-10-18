import logging

from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
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

    create:
    Maak een KLANT aan.

    Maak een KLANT aan.

    list:
    Alle KLANTen opvragen.

    Alle KLANTen opvragen.

    retrieve:
    Een specifiek KLANT opvragen.

    Een specifiek KLANT opvragen.

    update:
    Werk een KLANT in zijn geheel bij.

    Werk een KLANT in zijn geheel bij.

    partial_update:
    Werk een KLANT deels bij.

    Werk een KLANT deels bij.

    destroy:
    Verwijder een KLANT.

    Verwijder een KLANT.
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


class KlantAuditTrailViewSet(AuditTrailViewSet):
    """
    Opvragen van de audit trail regels.

    list:
    Alle audit trail regels behorend bij de KLANT.

    Alle audit trail regels behorend bij de KLANT.

    retrieve:
    Een specifieke audit trail regel opvragen.

    Een specifieke audit trail regel opvragen.
    """

    main_resource_lookup_field = "klant_uuid"
