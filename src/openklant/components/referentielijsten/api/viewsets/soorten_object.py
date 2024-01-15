from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ...models import SoortObject
from ..serializers import SoortObjectSerializer


@extend_schema(
    tags=["Soorten object"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="getsoortenobject",
        description="De operatie waarmee gegevens van de referentielijst Soorten object kunnen worden gezocht.",
    ),
    create=extend_schema(
        operation_id="postsoortobject",
        description="De operatie waarmee gegevens van de referentielijst Soorten object kunnen worden geregistreerd.",
    ),
    retrieve=extend_schema(
        operation_id="getsoortobject",
        description="De operatie waarmee gegevens van de referentielijst Soorten object kunnen worden geselecteerd.",
    ),
    update=extend_schema(
        operation_id="putsoortobject",
        description="De operatie waarmee gegevens van de referentielijst Soorten object kunnen worden gewijzigd.",
    ),
    delete=extend_schema(
        operation_id="delsoortobject",
        description="De operatie waarmee gegevens van de referentielijst Soorten object kunnen worden verwijderd.",
    ),
)
class SoortObjectViewSet(viewsets.ModelViewSet):
    __doc__ = SoortObject.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = SoortObject.objects.order_by("-pk")
    serializer_class = SoortObjectSerializer
