from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from vng_api_common.pagination import DynamicPageSizePagination

from openklant.components.klantinteracties.api.filterset.digitaal_adres import (
    DigitaalAdresDetailFilterSet,
    DigitaalAdresFilterSet,
)
from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresSerializer,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions
from openklant.components.utils.mixins import ExpandMixin

logger = structlog.get_logger(__name__)


@extend_schema(tags=["digitale adressen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle digitale adressen opvragen.",
        description="Alle digitale adressen opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek digitaal adres opvragen.",
        description="Een specifiek digitaal adres opvragen.",
    ),
    create=extend_schema(
        summary="Maak een digitaal adres aan.",
        description="Maak een digitaal adres aan.",
    ),
    update=extend_schema(
        summary="Werk een digitaal adres in zijn geheel bij.",
        description="Werk een digitaal adres in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een digitaal adres deels bij.",
        description="Werk een digitaal adres deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een digitaal adres.",
        description="Verwijder een digitaal adres.",
    ),
)
class DigitaalAdresViewSet(ExpandMixin, viewsets.ModelViewSet):
    """
    Digitaal adres dat een betrokkene bij klantcontact verstrekte
    voor gebruik bij opvolging van een klantcontact.
    """

    queryset = DigitaalAdres.objects.order_by("-pk").select_related(
        "partij",
        "betrokkene",
    )
    serializer_class = DigitaalAdresSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @property
    def filterset_class(self):
        """
        support expand in the detail endpoint
        """
        if self.detail:
            return DigitaalAdresDetailFilterSet
        return DigitaalAdresFilterSet

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        adres = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "digitaal_adres_created",
            uuid=str(adres.uuid),
            partij_uuid=str(adres.partij.uuid) if adres.partij else None,
            betrokkene_uuid=str(adres.betrokkene.uuid) if adres.betrokkene else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        adres = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "digitaal_adres_updated",
            uuid=str(adres.uuid),
            partij_uuid=str(adres.partij.uuid) if adres.partij else None,
            betrokkene_uuid=str(adres.betrokkene.uuid) if adres.betrokkene else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        partij_uuid = str(instance.partij.uuid) if instance.partij else None
        betrokkene_uuid = str(instance.betrokkene.uuid) if instance.betrokkene else None
        super().perform_destroy(instance)
        logger.info(
            "digitaal_adres_deleted",
            uuid=uuid,
            partij_uuid=partij_uuid,
            betrokkene_uuid=betrokkene_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )
