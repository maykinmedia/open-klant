from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ...models import Taal
from ..serializers import TaalSerializer


@extend_schema(
    tags=["Talen"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="gettalen",
        description="De operatie waarmee gegevens van de referentielijst Talen kunnen worden gezocht.",
    ),
    create=extend_schema(
        operation_id="posttaal",
        description="De operatie waarmee gegevens van de referentielijst Talen kunnen worden geregistreerd.",
    ),
    retrieve=extend_schema(
        operation_id="gettaal",
        description="De operatie waarmee gegevens van de referentielijst Talen kunnen worden geselecteerd.",
    ),
    update=extend_schema(
        operation_id="puttaal",
        description="De operatie waarmee gegevens van de referentielijst Talen kunnen worden gewijzigd.",
    ),
    destroy=extend_schema(
        operation_id="deltaal",
        description="De operatie waarmee gegevens van de referentielijst Talen kunnen worden verwijderd.",
    ),
)
class TaalViewSet(viewsets.ModelViewSet):
    __doc__ = Taal.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = Taal.objects.order_by("-pk")
    serializer_class = TaalSerializer
