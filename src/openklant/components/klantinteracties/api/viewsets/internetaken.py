from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.serializers.internetaken import (
    InterneTaakSerializer,
)
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions


class InterneTaakViewSet(viewsets.ModelViewSet):
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
