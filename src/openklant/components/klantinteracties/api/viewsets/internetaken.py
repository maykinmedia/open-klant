from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import viewsets
from vng_api_common.pagination import DynamicPageSizePagination

from openklant.components.klantinteracties.api.filterset.internetaken import (
    InternetaakFilterSet,
)
from openklant.components.klantinteracties.api.serializers.internetaken import (
    InterneTaakSerializer,
)
from openklant.components.klantinteracties.kanalen import KANAAL_INTERNETAAK
from openklant.components.klantinteracties.metrics import (
    interne_taken_create_counter,
    interne_taken_delete_counter,
    interne_taken_update_counter,
)
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions
from openklant.components.utils.api import get_related_object_uuid

logger = structlog.get_logger(__name__)


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
class InterneTaakViewSet(NotificationViewSetMixin, viewsets.ModelViewSet):
    """Iets dat door een actor moet worden gedaan om opvolging te geven aan een klantcontact."""

    queryset = (
        InterneTaak.objects.order_by("-pk")
        .prefetch_related("actoren")
        .select_related("klantcontact")
    )
    serializer_class = InterneTaakSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filterset_class = InternetaakFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
    notifications_kanaal = KANAAL_INTERNETAAK

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = serializer.instance
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        klantcontact_uuid = get_related_object_uuid(instance, "klantcontact")

        interne_taken_create_counter.add(
            1,
            attributes={
                "uuid": uuid,
                "klantcontact_uuid": klantcontact_uuid,
            },
        )
        logger.info(
            "interne_taak_created",
            uuid=uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = serializer.instance
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        klantcontact_uuid = get_related_object_uuid(instance, "klantcontact")

        interne_taken_update_counter.add(
            1,
            attributes={
                "uuid": uuid,
                "klantcontact_uuid": klantcontact_uuid,
            },
        )
        logger.info(
            "interne_taak_updated",
            uuid=uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        uuid = str(instance.uuid)
        token_auth = self.request.auth
        klantcontact_uuid = get_related_object_uuid(instance, "klantcontact")
        super().perform_destroy(instance)

        interne_taken_delete_counter.add(
            1,
            attributes={
                "uuid": uuid,
                "klantcontact_uuid": klantcontact_uuid,
            },
        )
        logger.info(
            "interne_taak_deleted",
            uuid=uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )
