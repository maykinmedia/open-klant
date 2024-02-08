from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.filterset.klantcontacten import (
    ActorKlantcontactFilterSet,
    BetrokkeneFilterSet,
    KlantcontactFilterSet,
)
from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    ActorKlantcontactSerializer,
    BetrokkeneSerializer,
    BijlageSerializer,
    KlantcontactSerializer,
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
from openklant.components.token.permission import TokenPermissions
from openklant.components.utils.mixins import ExpandMixin


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
    )
    serializer_class = KlantcontactSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filterset_class = KlantcontactFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


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
class BetrokkeneViewSet(viewsets.ModelViewSet):
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
    pagination_class = PageNumberPagination
    filterset_class = BetrokkeneFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


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
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "objectidentificator_objecttype",
        "objectidentificator_soort_object_id",
        "objectidentificator_object_id",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


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
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "objectidentificator_objecttype",
        "objectidentificator_soort_object_id",
        "objectidentificator_object_id",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


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
    pagination_class = PageNumberPagination
    filterset_class = ActorKlantcontactFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
