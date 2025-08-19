from django.db import transaction

import structlog
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from vng_api_common.pagination import DynamicPageSizePagination

from openklant.components.klantinteracties.api.filterset.klantcontacten import (
    ActorKlantcontactFilterSet,
    BetrokkeneDetailFilterSet,
    BetrokkeneFilterSet,
    KlantcontactDetailFilterSet,
    KlantcontactFilterSet,
    OnderwerpObjectFilterSet,
)
from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    ActorKlantcontactSerializer,
    BetrokkeneSerializer,
    BijlageSerializer,
    KlantcontactSerializer,
    MaakKlantcontactSerializer,
    OnderwerpobjectSerializer,
)
from openklant.components.klantinteracties.models.actoren import ActorKlantcontact
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Bijlage,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.models import TokenAuth
from openklant.components.token.permission import TokenPermissions
from openklant.components.utils.mixins import ExpandMixin

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["klanten contacten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle klanten contacten opvragen.",
        description="Alle klanten contacten opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek klant contact opvragen.",
        description="Een specifiek klant contact opvragen.",
    ),
    create=extend_schema(
        summary="Maak een klant contact aan.",
        description="Maak een klant contact aan.",
    ),
    update=extend_schema(
        summary="Werk een klant contact in zijn geheel bij.",
        description="Werk een klant contact in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een klant contact deels bij.",
        description="Werk een klant contact deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een klant contact.",
        description="Verwijder een klant contact.",
    ),
)
class KlantcontactViewSet(ExpandMixin, viewsets.ModelViewSet):
    """
    Contact tussen een klant of een vertegenwoordiger van een
    klant en de gemeente over een onderwerp.
    """

    queryset = Klantcontact.objects.order_by("-pk").prefetch_related(
        "bijlage_set",
        "betrokkene_set",
        "internetaak_set",
        "actorklantcontact_set",
        "onderwerpobject_set",
    )
    serializer_class = KlantcontactSerializer
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
            return KlantcontactDetailFilterSet
        return KlantcontactFilterSet

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        klantcontact = serializer.instance
        token_auth: TokenAuth = self.request.auth
        logger.info(
            "klantcontact_created",
            uuid=str(klantcontact.uuid),
            nummer=klantcontact.nummer,
            onderwerp=klantcontact.onderwerp,
            plaatsgevonden_op=klantcontact.plaatsgevonden_op.isoformat()
            if klantcontact.plaatsgevonden_op
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        klantcontact = serializer.instance
        token_auth: TokenAuth = self.request.auth
        logger.info(
            "klantcontact_updated",
            uuid=str(klantcontact.uuid),
            nummer=klantcontact.nummer,
            onderwerp=klantcontact.onderwerp,
            plaatsgevonden_op=klantcontact.plaatsgevonden_op.isoformat()
            if klantcontact.plaatsgevonden_op
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth: TokenAuth = self.request.auth
        instance.delete()
        logger.info(
            "klantcontact_deleted",
            uuid=str(instance.uuid),
            nummer=instance.nummer,
            onderwerp=instance.onderwerp,
            plaatsgevonden_op=instance.plaatsgevonden_op.isoformat()
            if instance.plaatsgevonden_op
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema(tags=["betrokkenen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle betrokkenen opvragen.",
        description="Alle betrokkenen opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek betrokkene opvragen.",
        description="Een specifiek betrokkene opvragen.",
    ),
    create=extend_schema(
        summary="Maak een betrokkene aan.",
        description="Maak een betrokkene aan.",
    ),
    update=extend_schema(
        summary="Werk een betrokkene in zijn geheel bij.",
        description="Werk een betrokkene in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een betrokkene deels bij.",
        description="Werk een betrokkene deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een betrokkene.",
        description="Verwijder een betrokkene.",
    ),
)
class BetrokkeneViewSet(ExpandMixin, viewsets.ModelViewSet):
    """
    Ofwel betrokkenheid van een partij bij een klantcontact, eventueel aangevuld met
    specifiek voor opvolging van dat klantcontact te gebruiken contactgegevens, ofwel
    voor opvolging van een klantcontact te gebruiken contactgegevens van een tijdens
    dat klantcontact niet als partij gekende persoon.
    """

    queryset = (
        Betrokkene.objects.order_by("-pk")
        .select_related(
            "partij",
            "klantcontact",
        )
        .prefetch_related("digitaaladres_set")
    )
    serializer_class = BetrokkeneSerializer
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
            return BetrokkeneDetailFilterSet
        return BetrokkeneFilterSet

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        betrokkene = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "betrokkene_created",
            uuid=str(betrokkene.uuid),
            partij_uuid=str(betrokkene.partij.uuid) if betrokkene.partij else None,
            klantcontact_uuid=str(betrokkene.klantcontact.uuid)
            if betrokkene.klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        betrokkene = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "betrokkene_updated",
            uuid=str(betrokkene.uuid),
            partij_uuid=str(betrokkene.partij.uuid) if betrokkene.partij else None,
            klantcontact_uuid=str(betrokkene.klantcontact.uuid)
            if betrokkene.klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        uuid = str(instance.uuid)
        partij_uuid = str(instance.partij.uuid) if instance.partij else None
        klantcontact_uuid = (
            str(instance.klantcontact.uuid) if instance.klantcontact else None
        )
        token_auth = self.request.auth

        super().perform_destroy(instance)

        logger.info(
            "betrokkene_deleted",
            uuid=uuid,
            partij_uuid=partij_uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema(tags=["onderwerpobjecten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle onderwerpobject opvragen.",
        description="Alle onderwerpobject opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek onderwerpobject opvragen.",
        description="Een specifiek onderwerpobject opvragen.",
    ),
    create=extend_schema(
        summary="Maak een onderwerpobject aan.",
        description="Maak een onderwerpobject aan.",
    ),
    update=extend_schema(
        summary="Werk een onderwerpobject in zijn geheel bij.",
        description="Werk een onderwerpobject in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een onderwerpobject deels bij.",
        description="Werk een onderwerpobject deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een onderwerpobject.",
        description="Verwijder een onderwerpobject.",
    ),
)
class OnderwerpobjectViewSet(viewsets.ModelViewSet):
    queryset = Onderwerpobject.objects.order_by("-pk").select_related(
        "klantcontact",
        "was_klantcontact",
    )
    serializer_class = OnderwerpobjectSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filterset_class = OnderwerpObjectFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "onderwerpobject_created",
            uuid=str(instance.uuid),
            klantcontact_uuid=str(instance.klantcontact.uuid)
            if instance.klantcontact
            else None,
            was_klantcontact_uuid=str(instance.was_klantcontact.uuid)
            if instance.was_klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "onderwerpobject_updated",
            uuid=str(instance.uuid),
            klantcontact_uuid=str(instance.klantcontact.uuid)
            if instance.klantcontact
            else None,
            was_klantcontact_uuid=str(instance.was_klantcontact.uuid)
            if instance.was_klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        token_auth = self.request.auth
        logger.info(
            "onderwerpobject_deleted",
            uuid=str(instance.uuid),
            klantcontact_uuid=str(instance.klantcontact.uuid)
            if instance.klantcontact
            else None,
            was_klantcontact_uuid=str(instance.was_klantcontact.uuid)
            if instance.was_klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema(tags=["bijlagen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle bijlagen opvragen.",
        description="Alle bijlagen opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek bijlage opvragen.",
        description="Een specifiek bijlage opvragen.",
    ),
    create=extend_schema(
        summary="Maak een bijlage aan.",
        description="Maak een bijlage aan.",
    ),
    update=extend_schema(
        summary="Werk een bijlage in zijn geheel bij.",
        description="Werk een bijlage in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een bijlage deels bij.",
        description="Werk een bijlage deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een bijlage.",
        description="Verwijder een bijlage.",
    ),
)
class BijlageViewSet(viewsets.ModelViewSet):
    queryset = Bijlage.objects.order_by("-pk").select_related("klantcontact")
    serializer_class = BijlageSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filterset_fields = [
        "bijlageidentificator_object_id",
        "bijlageidentificator_code_objecttype",
        "bijlageidentificator_code_register",
        "bijlageidentificator_code_soort_object_id",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        bijlage = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "bijlage_created",
            uuid=str(bijlage.uuid),
            klantcontact_uuid=str(bijlage.klantcontact.uuid)
            if bijlage.klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        bijlage = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "bijlage_updated",
            uuid=str(bijlage.uuid),
            klantcontact_uuid=str(bijlage.klantcontact.uuid)
            if bijlage.klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        klantcontact_uuid = (
            str(instance.klantcontact.uuid) if instance.klantcontact else None
        )
        super().perform_destroy(instance)
        logger.info(
            "bijlage_deleted",
            uuid=uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema(tags=["actor klantcontacten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle actor klantcontacten opvragen.",
        description="Alle actor klantcontacten opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek actor klantcontact opvragen.",
        description="Een specifiek actor klantcontact opvragen.",
    ),
    create=extend_schema(
        summary="Maak een actor klantcontact aan.",
        description="Maak een actor klantcontact aan.",
    ),
    update=extend_schema(
        summary="Werk een actor klantcontact in zijn geheel bij.",
        description="Werk een actor klantcontact in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een actor klantcontact deels bij.",
        description="Werk een actor klantcontact deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een aactor klantcontactctor.",
        description="Verwijder een actor klantcontact.",
    ),
)
class ActorKlantcontactViewSet(viewsets.ModelViewSet):
    """Iets dat of iemand die voor de gemeente werkzaamheden uitvoert."""

    queryset = ActorKlantcontact.objects.order_by("-pk").select_related(
        "actor",
        "klantcontact",
    )
    serializer_class = ActorKlantcontactSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filterset_class = ActorKlantcontactFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        relation = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "actor_klantcontact_created",
            uuid=str(relation.uuid),
            actor_uuid=str(relation.actor.uuid) if relation.actor else None,
            klantcontact_uuid=str(relation.klantcontact.uuid)
            if relation.klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        relation = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "actor_klantcontact_updated",
            uuid=str(relation.uuid),
            actor_uuid=str(relation.actor.uuid) if relation.actor else None,
            klantcontact_uuid=str(relation.klantcontact.uuid)
            if relation.klantcontact
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        actor_uuid = str(instance.actor.uuid) if instance.actor else None
        klantcontact_uuid = (
            str(instance.klantcontact.uuid) if instance.klantcontact else None
        )
        super().perform_destroy(instance)
        logger.info(
            "actor_klantcontact_deleted",
            uuid=uuid,
            actor_uuid=actor_uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema(tags=["maak-klantcontact"])
@extend_schema_view(
    create=extend_schema(
        summary="Maak een KlantContact, Betrokkene en een OnderwerpObject aan.",
        description="Maak een KlantContact, Betrokkene en een OnderwerpObject aan.",
    ),
)
class MaakKlantcontactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Endpoint om in één request een Klantcontact met een Betrokkene en een OnderwerpObject
    aan te maken. De aangemaakte objecten worden automatisch aan elkaar gekoppeld.
    """

    serializer_class = MaakKlantcontactSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        result = serializer.save()
        klantcontact = result["klantcontact"]
        betrokkene = result.get("betrokkene")
        onderwerpobject = result.get("onderwerpobject")

        token_auth = self.request.auth
        logger.info(
            "klantcontact_geregistreerd",
            uuid=str(klantcontact.uuid),
            onderwerp=klantcontact.onderwerp,
            plaatsgevonden_op=klantcontact.plaatsgevonden_op.isoformat()
            if klantcontact.plaatsgevonden_op
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
            betrokkene_uuid=str(betrokkene.uuid) if betrokkene else None,
            onderwerpobject_uuid=str(onderwerpobject.uuid) if onderwerpobject else None,
        )
