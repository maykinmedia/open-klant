from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ...models import ExternRegister
from ..serializers import ExternRegisterSerializer


@extend_schema(
    tags=["Externe registers"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="getexterneregisters",
        description="De operatie waarmee gegevens van de referentielijst Extern Register kunnen worden gezocht.",
    ),
    create=extend_schema(
        operation_id="postexternregister",
        description="De operatie waarmee gegevens van de referentielijst Extern Register kunnen worden geregistreerd.",
    ),
    retrieve=extend_schema(
        operation_id="getexternregister",
        description="De operatie waarmee gegevens van de referentielijst Extern Register kunnen worden geselecteerd.",
    ),
    update=extend_schema(
        operation_id="putexternregister",
        description="De operatie waarmee gegevens van de referentielijst Extern Register kunnen worden gewijzigd.",
    ),
    destroy=extend_schema(
        operation_id="delexternregister",
        description="De operatie waarmee gegevens van de referentielijst Extern Register kunnen worden verwijderd.",
    ),
)
class ExternRegisterViewSet(viewsets.ModelViewSet):
    __doc__ = ExternRegister.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = ExternRegister.objects.order_by("-pk")
    serializer_class = ExternRegisterSerializer
