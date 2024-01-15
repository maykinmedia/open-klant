from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ...models import Land
from ..serializers import LandSerializer


@extend_schema(
    tags=["Landen"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="getlanden",
        description="De operatie waarmee gegevens van de referentielijst Landen kunnen worden gezocht.",
    ),
    create=extend_schema(
        operation_id="postland",
        description="De operatie waarmee gegevens van de referentielijst Landen kunnen worden geregistreerd.",
    ),
    retrieve=extend_schema(
        operation_id="getlanden",
        description="De operatie waarmee gegevens van de referentielijst Landen kunnen worden geselecteerd.",
    ),
    update=extend_schema(
        operation_id="putland",
        description="De operatie waarmee gegevens van de referentielijst Landen kunnen worden gewijzigd.",
    ),
    destroy=extend_schema(
        operation_id="delland",
        description="De operatie waarmee gegevens van de referentielijst Landen kunnen worden verwijderd.",
    ),
)
class LandViewSet(viewsets.ModelViewSet):
    __doc__ = Land.__doc__
    lookup_field = "landcode"
    pagination_class = None
    queryset = Land.objects.order_by("-pk")
    serializer_class = LandSerializer
