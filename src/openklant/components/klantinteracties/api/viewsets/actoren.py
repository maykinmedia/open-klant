from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from vng_api_common.pagination import DynamicPageSizePagination

from openklant.components.klantinteracties.api.filterset.actoren import ActorenFilterSet
from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorSerializer,
)
from openklant.components.klantinteracties.models.actoren import Actor
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions

logger = structlog.get_logger(__name__)


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

    queryset = (
        Actor.objects.order_by("-pk")
        .select_related(
            "geautomatiseerdeactor",
            "medewerker",
            "organisatorischeeenheid",
        )
        .prefetch_related("actorklantcontact_set")
    )
    serializer_class = ActorSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filterset_class = ActorenFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        actor = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "actor_created",
            uuid=str(actor.uuid),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        actor = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "actor_updated",
            uuid=str(actor.uuid),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        uuid = str(instance.uuid)
        token_auth = self.request.auth
        super().perform_destroy(instance)
        logger.info(
            "actor_deleted",
            uuid=uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )
