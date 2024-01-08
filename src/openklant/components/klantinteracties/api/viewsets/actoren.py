from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.filterset.actoren import ActorenFilterSet
from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorSerializer,
)
from openklant.components.klantinteracties.models.actoren import Actor
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions


class ActorViewSet(viewsets.ModelViewSet):
    """
    Iets dat of iemand die voor de gemeente werkzaamheden uitvoert.

    create:
    Maak een actor aan.

    Maak een actor aan.

    list:
    Alle actoren opvragen.

    Alle actoren opvragen.

    retrieve:
    Een specifiek actor opvragen.

    Een specifiek actor opvragen.

    update:
    Werk een actor in zijn geheel bij.

    Werk een actor in zijn geheel bij.

    partial_update:
    Werk een actor deels bij.

    Werk een actor deels bij.

    destroy:
    Verwijder een actor.

    Verwijder een actor.
    """

    queryset = Actor.objects.order_by("-pk").select_related(
        "geautomatiseerdeactor",
        "medewerker",
        "organisatorischeeenheid",
    )
    serializer_class = ActorSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filterset_class = ActorenFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
