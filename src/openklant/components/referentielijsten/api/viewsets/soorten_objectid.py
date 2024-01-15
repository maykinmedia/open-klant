from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ...models import SoortObjectid
from ..serializers import SoortObjectidSerializer


@extend_schema(
    tags=["Soorten objectId"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="getsoortenobjectid",
        description="De operatie waarmee gegevens van de referentielijst Soorten objectId kunnen worden gezocht.",
    ),
    create=extend_schema(
        operation_id="postsoortobjectid",
        description="De operatie waarmee gegevens van de referentielijst Soorten objectId kunnen worden geregistreerd.",
    ),
    retrieve=extend_schema(
        operation_id="getsoortobjectid",
        description="De operatie waarmee gegevens van de referentielijst Soorten objectId kunnen worden geselecteerd.",
    ),
    update=extend_schema(
        operation_id="putsoortobjectid",
        description="De operatie waarmee gegevens van de referentielijst Soorten objectId kunnen worden gewijzigd.",
    ),
    destroy=extend_schema(
        operation_id="delsoortobjectid",
        description="De operatie waarmee gegevens van de referentielijst Soorten objectId kunnen worden verwijderd.",
    ),
)
class SoortObjectidViewSet(viewsets.ModelViewSet):
    __doc__ = SoortObjectid.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = SoortObjectid.objects.order_by("-pk")
    serializer_class = SoortObjectidSerializer
