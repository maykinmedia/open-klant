from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from vng_api_common.audittrails.viewsets import AuditTrailViewsetMixin

from openklant.components.klantinteracties.api.serializers.internetaken import (
    InterneTaakSerializer,
)
from openklant.components.klantinteracties.models.internetaken import InterneTaak


class InterneTaakViewSet(
    NotificationViewSetMixin, AuditTrailViewsetMixin, viewsets.ModelViewSet
):
    """
    Iets dat door een actor moet worden gedaan om opvolging te geven aan een klantcontact.

    create:
    Maak een interne taak aan.

    Maak een interne taak aan.

    list:
    Alle interne taken opvragen.

    Alle interne taken opvragen.

    retrieve:
    Een specifiek interne taak opvragen.

    Een specifiek interne taak opvragen.

    update:
    Werk een interne taak in zijn geheel bij.

    Werk een interne taak in zijn geheel bij.

    partial_update:
    Werk een interne taak deels bij.

    Werk een interne taak deels bij.

    destroy:
    Verwijder een interne taak.

    Verwijder een interne taak.
    """

    queryset = InterneTaak.objects.order_by("-pk")
    serializer_class = InterneTaakSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
