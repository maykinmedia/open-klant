from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
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
from openklant.components.klantinteracties.models.partijen import (
    Categorie,
    CategorieRelatie,
    Partij,
    PartijIdentificator,
    Vertegenwoordigden,
)
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions
from openklant.components.utils.mixins import ExpandMixin
from openklant.utils.decorators import handle_db_exceptions


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
        )
        .prefetch_related(
            "betrokkene_set",
            "digitaaladres_set",
            "partijidentificator_set",
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


@extend_schema(tags=["partij-identificatoren"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle partij-identificatoren opvragen.",
        description="Alle partij-identificatoren opvragen.",
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

    queryset = PartijIdentificator.objects.order_by("-pk").select_related("partij")
    serializer_class = PartijIdentificatorSerializer
    lookup_field = "uuid"
    pagination_class = DynamicPageSizePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "andere_partij_identificator",
        "partij_identificator_code_objecttype",
        "partij_identificator_code_soort_object_id",
        "partij_identificator_object_id",
        "partij_identificator_code_register",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)

    @handle_db_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
