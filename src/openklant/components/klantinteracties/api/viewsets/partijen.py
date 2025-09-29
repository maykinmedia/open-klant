from django.db import transaction

import structlog
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import viewsets
from vng_api_common.pagination import DynamicPageSizePagination

from openklant.components.klantinteracties.api.filterset.partijen import (
    CategorieRelatieFilterSet,
    PartijDetailFilterSet,
    PartijFilterSet,
    VertegenwoordigdenFilterSet,
)
from openklant.components.klantinteracties.api.schema import (
    PARTIJ_IDENTIFICATOR_DESCRIPTION_CREATE,
    PARTIJ_IDENTIFICATOR_DESCRIPTION_UPDATE,
)
from openklant.components.klantinteracties.api.serializers.partijen import (
    CategorieRelatieSerializer,
    CategorieSerializer,
    PartijIdentificatorSerializer,
    PartijSerializer,
    VertegenwoordigdenSerializer,
)
from openklant.components.klantinteracties.kanalen import KANAAL_PARTIJ
from openklant.components.klantinteracties.metrics import (
    partijen_create_counter,
    partijen_delete_counter,
    partijen_update_counter,
)
from openklant.components.klantinteracties.models.partijen import (
    Categorie,
    CategorieRelatie,
    Partij,
    PartijIdentificator,
    Vertegenwoordigden,
)
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions
from openklant.components.utils.api import get_related_object_uuid
from openklant.components.utils.mixins import ExpandMixin
from openklant.utils.decorators import handle_db_exceptions

logger = structlog.get_logger(__name__)


@extend_schema(tags=["partijen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle partijen opvragen.",
        description="Alle partijen opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek partij opvragen.",
        description="Een specifiek partij opvragen.",
    ),
    create=extend_schema(
        summary="Maak een partij aan.",
        description=PARTIJ_IDENTIFICATOR_DESCRIPTION_CREATE,
    ),
    update=extend_schema(
        summary="Werk een partij in zijn geheel bij.",
        description=PARTIJ_IDENTIFICATOR_DESCRIPTION_UPDATE,
    ),
    partial_update=extend_schema(
        summary="Werk een partij deels bij.",
        description=PARTIJ_IDENTIFICATOR_DESCRIPTION_UPDATE,
    ),
    destroy=extend_schema(
        summary="Verwijder een partij.",
        description="Verwijder een partij.",
    ),
)
class PartijViewSet(NotificationViewSetMixin, ExpandMixin, viewsets.ModelViewSet):
    """Persoon of organisatie waarmee de gemeente een relatie heeft."""

    queryset = (
        Partij.objects.order_by("-pk")
        .select_related(
            "organisatie",
            "persoon",
            "contactpersoon",
            "voorkeurs_digitaal_adres",
            "voorkeurs_rekeningnummer",
        )
        .prefetch_related(
            "betrokkene_set",
            "digitaaladres_set",
            "categorierelatie_set",
            "partijidentificator_set",
            "rekeningnummer_set",
            "vertegenwoordigende",
        )
    )
    serializer_class = PartijSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
    notifications_kanaal = KANAAL_PARTIJ

    @property
    def filterset_class(self):
        """
        support expand in the detail endpoint
        """
        if self.detail:
            return PartijDetailFilterSet
        return PartijFilterSet

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = serializer.instance
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        organisatie_uuid = get_related_object_uuid(instance, "organisatie")
        persoon_uuid = get_related_object_uuid(instance, "persoon")

        partijen_create_counter.add(
            1,
            attributes={
                "uuid": uuid,
                "organisatie_uuid": organisatie_uuid,
                "persoon_uuid": persoon_uuid,
            },
        )
        logger.info(
            "partij_created",
            uuid=uuid,
            organisatie_uuid=organisatie_uuid,
            persoon_uuid=persoon_uuid,
            token_identifier=getattr(token_auth, "identifier", None),
            token_application=getattr(token_auth, "application", None),
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = serializer.instance
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        organisatie_uuid = get_related_object_uuid(instance, "organisatie")
        persoon_uuid = get_related_object_uuid(instance, "persoon")

        partijen_update_counter.add(
            1,
            attributes={
                "uuid": uuid,
                "organisatie_uuid": organisatie_uuid,
                "persoon_uuid": persoon_uuid,
            },
        )
        logger.info(
            "partij_updated",
            uuid=uuid,
            organisatie_uuid=organisatie_uuid,
            persoon_uuid=persoon_uuid,
            token_identifier=getattr(token_auth, "identifier", None),
            token_application=getattr(token_auth, "application", None),
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        organisatie_uuid = get_related_object_uuid(instance, "organisatie")
        persoon_uuid = get_related_object_uuid(instance, "persoon")
        super().perform_destroy(instance)

        partijen_delete_counter.add(
            1,
            attributes={
                "uuid": uuid,
                "organisatie_uuid": organisatie_uuid,
                "persoon_uuid": persoon_uuid,
            },
        )
        logger.info(
            "partij_deleted",
            uuid=uuid,
            organisatie_uuid=organisatie_uuid,
            persoon_uuid=persoon_uuid,
            token_identifier=getattr(token_auth, "identifier", None),
            token_application=getattr(token_auth, "application", None),
        )


@extend_schema(tags=["vertegenwoordigingen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle vertegenwoordigingen opvragen.",
        description="Alle vertegenwoordigingen opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek vertegenwoordiging opvragen.",
        description="Een specifiek vertegenwoordiging opvragen.",
    ),
    create=extend_schema(
        summary="Maak een vertegenwoordiging aan.",
        description="Maak een vertegenwoordiging aan.",
    ),
    update=extend_schema(
        summary="Werk een vertegenwoordiging in zijn geheel bij.",
        description="Werk een vertegenwoordiging in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een vertegenwoordiging deels bij.",
        description="Werk een vertegenwoordiging deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een vertegenwoordiging.",
        description="Verwijder een vertegenwoordiging.",
    ),
)
class VertegenwoordigdenViewSet(viewsets.ModelViewSet):
    """Persoon of organisatie waarmee de gemeente een relatie heeft."""

    queryset = Vertegenwoordigden.objects.order_by("-pk").select_related(
        "vertegenwoordigende_partij",
        "vertegenwoordigde_partij",
    )
    serializer_class = VertegenwoordigdenSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filterset_class = VertegenwoordigdenFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "vertegenwoordiging_created",
            uuid=str(obj.uuid),
            vertegenwoordigde_partij_uuid=str(obj.vertegenwoordigde_partij.uuid)
            if obj.vertegenwoordigde_partij
            else None,
            vertegenwoordigende_partij_uuid=str(obj.vertegenwoordigende_partij.uuid)
            if obj.vertegenwoordigende_partij
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "vertegenwoordiging_updated",
            uuid=str(obj.uuid),
            vertegenwoordigde_partij_uuid=str(obj.vertegenwoordigde_partij.uuid)
            if obj.vertegenwoordigde_partij
            else None,
            vertegenwoordigende_partij_uuid=str(obj.vertegenwoordigende_partij.uuid)
            if obj.vertegenwoordigende_partij
            else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        vertegenwoordigde_partij_uuid = (
            str(instance.vertegenwoordigde_partij.uuid)
            if instance.vertegenwoordigde_partij
            else None
        )
        vertegenwoordigende_partij_uuid = (
            str(instance.vertegenwoordigende_partij.uuid)
            if instance.vertegenwoordigende_partij
            else None
        )
        super().perform_destroy(instance)
        logger.info(
            "vertegenwoordiging_deleted",
            uuid=uuid,
            vertegenwoordigde_partij_uuid=vertegenwoordigde_partij_uuid,
            vertegenwoordigende_partij_uuid=vertegenwoordigende_partij_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema(tags=["categorie relaties"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle categorie relaties opvragen.",
        description="Alle categorie relaties opvragen, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek categorie relatie opvragen..",
        description="Een specifiek categorie relatie opvragen, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    create=extend_schema(
        summary="Maak een categorie relatie aan.",
        description="Maak een categorie relatie aan, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    update=extend_schema(
        summary="Werk een categorie relatie in zijn geheel bij.",
        description="Werk een categorie relatie deels bij, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    partial_update=extend_schema(
        summary="Werk een categorie relatie deels bij.",
        description="Werk een categorie relatie deels bij, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    destroy=extend_schema(
        summary="Verwijder een categorie relatie.",
        description="Verwijder een categorie relatie, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
)
class CategorieRelatieViewSet(viewsets.ModelViewSet):
    """De categorie relatie van een partij, Let op: Dit endpoint is EXPERIMENTEEL."""

    queryset = CategorieRelatie.objects.order_by("-pk").select_related(
        "partij",
        "categorie",
    )
    serializer_class = CategorieRelatieSerializer
    lookup_field = "uuid"
    filterset_class = CategorieRelatieFilterSet
    pagination_class = DynamicPageSizePagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "categorie_relatie_created",
            uuid=str(obj.uuid),
            partij_uuid=str(obj.partij.uuid) if obj.partij else None,
            categorie_uuid=str(obj.categorie.uuid) if obj.categorie else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "categorie_relatie_updated",
            uuid=str(obj.uuid),
            partij_uuid=str(obj.partij.uuid) if obj.partij else None,
            categorie_uuid=str(obj.categorie.uuid) if obj.categorie else None,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        partij_uuid = str(instance.partij.uuid) if instance.partij else None
        categorie_uuid = str(instance.categorie.uuid) if instance.categorie else None
        super().perform_destroy(instance)
        logger.info(
            "categorie_relatie_deleted",
            uuid=uuid,
            partij_uuid=partij_uuid,
            categorie_uuid=categorie_uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema(tags=["categorieën"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle categorieën opvragen.",
        description="Alle categorieën opvragen, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek categorie opvragen..",
        description="Een specifiek categorie opvragen, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    create=extend_schema(
        summary="Maak een categorie aan.",
        description="Maak een categorie aan, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    update=extend_schema(
        summary="Werk een categorie in zijn geheel bij.",
        description="Werk een categorie deels bij, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    partial_update=extend_schema(
        summary="Werk een categorie deels bij.",
        description="Werk een categorie deels bij, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
    destroy=extend_schema(
        summary="Verwijder een categorie.",
        description="Verwijder een categorie, Let op: Dit endpoint is EXPERIMENTEEL.",
    ),
)
class CategorieViewSet(viewsets.ModelViewSet):
    """De categorie van een partij, Let op: Dit endpoint is EXPERIMENTEEL."""

    queryset = Categorie.objects.order_by("-pk")
    serializer_class = CategorieSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "categorie_created",
            uuid=str(obj.uuid),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "categorie_updated",
            uuid=str(obj.uuid),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        super().perform_destroy(instance)
        logger.info(
            "categorie_deleted",
            uuid=uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )


@extend_schema_view(
    list=extend_schema(
        summary="Alle partij-identificatoren opvragen.",
        description="Alle partij-identificatoren opvragen.",
        parameters=[
            OpenApiParameter(name="anderePartijIdentificator", deprecated=True)
        ],
    ),
    retrieve=extend_schema(
        summary="Een specifiek partij-identificator opvragen.",
        description="Een specifiek partij-identificator opvragen.",
    ),
    create=extend_schema(
        summary="Maak een partij-identificator aan.",
        description="Maak een partij-identificator aan.",
    ),
    update=extend_schema(
        summary="Werk een partij-identificator in zijn geheel bij.",
        description="Werk een partij-identificator in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een partij-identificator deels bij.",
        description="Werk een partij-identificator deels bij.",
    ),
    destroy=extend_schema(
        summary="Verwijder een partij-identificator.",
        description="Verwijder een partij-identificator.",
    ),
)
class PartijIdentificatorViewSet(viewsets.ModelViewSet):
    """Gegevens die een partij in een basisregistratie of ander extern register uniek identificeren."""

    queryset = PartijIdentificator.objects.order_by("-pk").select_related(
        "partij",
        "sub_identificator_van",
    )
    serializer_class = PartijIdentificatorSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filterset_fields = [
        "andere_partij_identificator",
        "partij_identificator_code_objecttype",
        "partij_identificator_code_soort_object_id",
        "partij_identificator_object_id",
        "partij_identificator_code_register",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "partijidentificator_created",
            uuid=str(obj.uuid),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        super().perform_update(serializer)
        obj = serializer.instance
        token_auth = self.request.auth
        logger.info(
            "partijidentificator_updated",
            uuid=str(obj.uuid),
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        token_auth = self.request.auth
        uuid = str(instance.uuid)
        super().perform_destroy(instance)
        logger.info(
            "partijidentificator_deleted",
            uuid=uuid,
            token_identifier=token_auth.identifier,
            token_application=token_auth.application,
        )

    @handle_db_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
