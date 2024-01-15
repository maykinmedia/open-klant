from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ...models import Kanaal
from ..serializers import KanaalSerializer


@extend_schema(
    tags=["Kanalen"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="getkanalen",
        description="De operatie waarmee gegevens van de referentielijst Kanalen kunnen worden gezocht.",
    ),
    create=extend_schema(
        operation_id="postkanaal",
        description="De operatie waarmee gegevens van de referentielijst Kanalen kunnen worden geregistreerd.",
    ),
    retrieve=extend_schema(
        operation_id="getkanaal",
        description="De operatie waarmee gegevens van de referentielijst Kanalen kunnen worden geselecteerd.",
    ),
    update=extend_schema(
        operation_id="putkanaal",
        description="De operatie waarmee gegevens van de referentielijst Kanalen kunnen worden gewijzigd.",
    ),
    destroy=extend_schema(
        operation_id="delkanaal",
        description="De operatie waarmee gegevens van de referentielijst Kanalen kunnen worden verwijderd.",
    ),
)
class KanaalViewSet(viewsets.ModelViewSet):
    __doc__ = Kanaal.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = Kanaal.objects.order_by("-pk")
    serializer_class = KanaalSerializer
