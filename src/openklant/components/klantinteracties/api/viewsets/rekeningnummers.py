from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from vng_api_common.pagination import DynamicPageSizePagination

from openklant.components.klantinteracties.api.serializers.rekeningnummers import (
    RekeningnummerSerializer,
)
from openklant.components.klantinteracties.models.rekeningnummers import Rekeningnummer
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions

logger = structlog.get_logger(__name__)


@extend_schema(tags=["rekeningnummers"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle rekeningnummers opvragen.",
        description="Alle rekeningnummers opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek rekeningnummer opvragen.",
        description="Een specifiek rekeningnummer opvragen.",
    ),
    create=extend_schema(
        summary="Maak een rekeningnummer aan.",
        description="Maak een rekeningnummer aan.",
    ),
    update=extend_schema(
        summary="Werk een rekeningnummer in zijn geheel bij.",
        description="Werk een rekeningnummer in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een rekeningnummer deels bij.",
        description="Werk een rekeningnummer deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een rekeningnummer.",
        description="Verwijder een rekeningnummer.",
    ),
)
class RekeningnummerViewSet(viewsets.ModelViewSet):
    queryset = Rekeningnummer.objects.order_by("-pk").select_related(
        "partij",
    )
    serializer_class = RekeningnummerSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filterset_fields = [
        "uuid",
        "iban",
        "bic",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        rekening = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "rekeningnummer_created",
            uuid=str(rekening.uuid),
            partij_uuid=str(rekening.partij.uuid) if rekening.partij else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        rekening = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "rekeningnummer_updated",
            uuid=str(rekening.uuid),
            partij_uuid=str(rekening.partij.uuid) if rekening.partij else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        partij_uuid = str(instance.partij.uuid) if instance.partij else None
        super().perform_destroy(instance)
        logger.info(
            "rekeningnummer_deleted",
            uuid=uuid,
            partij_uuid=partij_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )
