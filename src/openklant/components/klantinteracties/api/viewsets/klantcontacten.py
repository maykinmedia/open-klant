from django.conf import settings
from django.db import models, transaction
from django.urls import reverse

import structlog
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from notifications_api_common.cloudevents import process_cloudevent
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response
from vng_api_common.pagination import DynamicPageSizePagination
from vng_api_common.viewsets import CheckQueryParamsMixin

from openklant.cloud_events.constants import (
    ZAAK_GEKOPPELD,
    ZAAK_ONTKOPPELD,
)
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
from openklant.components.klantinteracties.metrics import (
    betrokkenen_create_counter,
    betrokkenen_delete_counter,
    betrokkenen_update_counter,
    klantcontacten_create_counter,
    klantcontacten_delete_counter,
    klantcontacten_update_counter,
)
from openklant.components.klantinteracties.models import DigitaalAdres
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
from openklant.components.utils.api import get_related_object_uuid
from openklant.components.utils.mixins import ExpandMixin

logger = structlog.stdlib.get_logger(__name__)


@extend_schema(tags=["klanten contacten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle klanten contacten opvragen.",
        description="Alle klanten contacten opvragen.",
        parameters=[OpenApiParameter(name="nummer", deprecated=True)],
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
class KlantcontactViewSet(CheckQueryParamsMixin, ExpandMixin, viewsets.ModelViewSet):
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
        instance = serializer.instance
        uuid = str(instance.uuid)
        token_auth: TokenAuth = self.request.auth
        klantcontacten_create_counter.add(1)
        logger.info(
            "klantcontact_created",
            uuid=uuid,
            nummer=instance.nummer,
            onderwerp=instance.onderwerp,
            plaatsgevonden_op=instance.plaatsgevonden_op.isoformat()
            if instance.plaatsgevonden_op
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = serializer.instance
        uuid = str(instance.uuid)
        token_auth: TokenAuth = self.request.auth
        klantcontacten_update_counter.add(1)
        logger.info(
            "klantcontact_updated",
            uuid=uuid,
            nummer=instance.nummer,
            onderwerp=instance.onderwerp,
            plaatsgevonden_op=instance.plaatsgevonden_op.isoformat()
            if instance.plaatsgevonden_op
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth: TokenAuth = self.request.auth
        uuid = str(instance.uuid)
        super().perform_destroy(instance)

        klantcontacten_delete_counter.add(1)
        logger.info(
            "klantcontact_deleted",
            uuid=uuid,
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
        parameters=[
            OpenApiParameter(name="hadKlantcontact__nummer", deprecated=True),
            OpenApiParameter(name="wasPartij__nummer", deprecated=True),
        ],
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
class BetrokkeneViewSet(CheckQueryParamsMixin, ExpandMixin, viewsets.ModelViewSet):
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
        instance = serializer.instance
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        partij_uuid = get_related_object_uuid(instance, "partij")
        klantcontact_uuid = get_related_object_uuid(instance, "klantcontact")

        betrokkenen_create_counter.add(1)
        logger.info(
            "betrokkene_created",
            uuid=uuid,
            partij_uuid=partij_uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = serializer.instance

        uuid = str(instance.uuid)
        partij_uuid = get_related_object_uuid(instance, "partij")
        klantcontact_uuid = get_related_object_uuid(instance, "klantcontact")
        token_auth = self.request.auth

        betrokkenen_update_counter.add(1)
        logger.info(
            "betrokkene_updated",
            uuid=uuid,
            partij_uuid=partij_uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        uuid = str(instance.uuid)
        partij_uuid = get_related_object_uuid(instance, "partij")
        klantcontact_uuid = get_related_object_uuid(instance, "klantcontact")
        token_auth = self.request.auth
        super().perform_destroy(instance)

        betrokkenen_delete_counter.add(1)
        logger.info(
            "betrokkene_deleted",
            uuid=uuid,
            partij_uuid=partij_uuid,
            klantcontact_uuid=klantcontact_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


class OnderwerpobjectDeleteResponseSerializer(serializers.Serializer):
    behouden = serializers.ListField(
        child=serializers.URLField(
            help_text="URL van een overgebleven Klantcontact resource"
        ),
        help_text="Lijst van Klantcontact URLs die behouden blijven",
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
        parameters=[
            OpenApiParameter(
                name="cascade",
                description=(
                    "Als `true`, worden gerelateerde Klantcontacten en DigitaalAdressen verwijderd "
                    "indien ze niet door andere Onderwerpobjecten worden gebruikt."
                ),
                required=False,
                default=False,
                type=bool,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Onderwerpobject succesvol verwijderd (zonder cascade)."
            ),
            status.HTTP_200_OK: OpenApiResponse(
                description=(
                    "Onderwerpobject verwijderd met cascade=true. "
                    "`behouden` bevat resterende Klantcontact URLs."
                ),
                response=OnderwerpobjectDeleteResponseSerializer,
            ),
        },
    ),
)
class OnderwerpobjectViewSet(CheckQueryParamsMixin, viewsets.ModelViewSet):
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
        object_type = instance.onderwerpobjectidentificator.get("code_objecttype")
        soort_object_id = instance.onderwerpobjectidentificator.get(
            "code_soort_object_id"
        )
        if (
            object_type == "zaak"
            and soort_object_id == "uuid"
            and settings.ENABLE_CLOUD_EVENTS
            and instance.klantcontact is not None
        ):
            link_to_url = reverse(
                "klantinteracties:onderwerpobject-detail",
                kwargs={
                    "uuid": str(instance.uuid),
                    "version": self.request.version or "1",
                },
            )

            process_cloudevent(
                type=ZAAK_GEKOPPELD,
                subject=instance.onderwerpobjectidentificator.get("object_id"),
                data={
                    "zaak": f"urn:uuid:{instance.onderwerpobjectidentificator.get('object_id')}",
                    "linkTo": self.request.build_absolute_uri(link_to_url),
                    "label": str(instance.klantcontact),
                    "linkObjectType": "Onderwerpobject",
                },
            )

    @transaction.atomic
    def perform_update(self, serializer):
        old_instance = Onderwerpobject.objects.get(pk=serializer.instance.pk)

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

        old_ident = old_instance.onderwerpobjectidentificator or {}
        new_ident = instance.onderwerpobjectidentificator or {}

        was_zaak = (
            old_ident.get("code_objecttype") == "zaak"
            and old_ident.get("code_soort_object_id") == "uuid"
            and old_instance.klantcontact is not None
        )

        is_zaak_now = (
            new_ident.get("code_objecttype") == "zaak"
            and new_ident.get("code_soort_object_id") == "uuid"
            and instance.klantcontact is not None
        )

        identificator_changed = old_ident != new_ident

        if settings.ENABLE_CLOUD_EVENTS and was_zaak and identificator_changed:
            link_to_url = reverse(
                "klantinteracties:onderwerpobject-detail",
                kwargs={
                    "uuid": str(old_instance.uuid),
                    "version": self.request.version or "1",
                },
            )

            transaction.on_commit(
                lambda: process_cloudevent(
                    type=ZAAK_ONTKOPPELD,
                    subject=old_ident.get("object_id"),
                    data={
                        "zaak": f"urn:uuid:{old_ident.get('object_id')}",
                        "linkTo": self.request.build_absolute_uri(link_to_url),
                        "label": str(old_instance.klantcontact),
                        "linkObjectType": "Onderwerpobject",
                    },
                )
            )
        if settings.ENABLE_CLOUD_EVENTS and is_zaak_now and identificator_changed:
            link_to_url = reverse(
                "klantinteracties:onderwerpobject-detail",
                kwargs={
                    "uuid": str(instance.uuid),
                    "version": self.request.version or "1",
                },
            )

            transaction.on_commit(
                lambda: process_cloudevent(
                    type=ZAAK_GEKOPPELD,
                    subject=new_ident.get("object_id"),
                    data={
                        "zaak": f"urn:uuid:{new_ident.get('object_id')}",
                        "linkTo": self.request.build_absolute_uri(link_to_url),
                        "label": str(instance.klantcontact),
                        "linkObjectType": "Onderwerpobject",
                    },
                )
            )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cascade = request.query_params.get("cascade", "false").lower() == "true"

        token_auth = request.auth
        remaining_klantcontacts = []

        klantcontact_uuid = (
            str(instance.klantcontact.uuid) if instance.klantcontact else None
        )
        was_klantcontact_uuid = (
            str(instance.was_klantcontact.uuid) if instance.was_klantcontact else None
        )

        object_type = instance.onderwerpobjectidentificator.get("code_objecttype")
        soort_object_id = instance.onderwerpobjectidentificator.get(
            "code_soort_object_id"
        )

        if (
            settings.ENABLE_CLOUD_EVENTS
            and object_type == "zaak"
            and soort_object_id == "uuid"
            and instance.klantcontact is not None
        ):
            link_to_url = reverse(
                "klantinteracties:onderwerpobject-detail",
                kwargs={
                    "uuid": str(instance.uuid),
                    "version": request.version or "1",
                },
            )

            transaction.on_commit(
                lambda: process_cloudevent(
                    type=ZAAK_ONTKOPPELD,
                    subject=instance.onderwerpobjectidentificator.get("object_id"),
                    data={
                        "zaak": f"urn:uuid:{instance.onderwerpobjectidentificator.get('object_id')}",
                        "linkTo": request.build_absolute_uri(link_to_url),
                        "label": str(instance.klantcontact),
                        "linkObjectType": "Onderwerpobject",
                    },
                )
            )

        if cascade:
            for kc in (instance.klantcontact, instance.was_klantcontact):
                if not kc:
                    continue

                has_other_connection = (
                    Onderwerpobject.objects.filter(
                        models.Q(klantcontact=kc) | models.Q(was_klantcontact=kc)
                    )
                    .exclude(pk=instance.pk)
                    .exists()
                )

                if has_other_connection:
                    remaining_klantcontacts.append(
                        request.build_absolute_uri(
                            reverse(
                                "klantinteracties:klantcontact-detail",
                                kwargs={
                                    "uuid": kc.uuid,
                                    "version": request.version or "1",
                                },
                            )
                        )
                    )
                    continue

                betrokkenen = Betrokkene.objects.filter(klantcontact=kc)
                DigitaalAdres.objects.filter(
                    betrokkene__in=betrokkenen,
                    partij__isnull=True,
                ).delete()

                kc.delete()

        instance.delete()

        logger.info(
            "onderwerpobject_deleted",
            uuid=str(instance.uuid),
            cascade=cascade,
            klantcontact_uuid=klantcontact_uuid,
            was_klantcontact_uuid=was_klantcontact_uuid,
            remaining_klantcontacten=remaining_klantcontacts if cascade else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

        if cascade:
            return Response(
                {
                    "behouden": remaining_klantcontacts,
                },
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


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
class BijlageViewSet(CheckQueryParamsMixin, viewsets.ModelViewSet):
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
class ActorKlantcontactViewSet(CheckQueryParamsMixin, viewsets.ModelViewSet):
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
