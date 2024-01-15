from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ...models import SoortDigitaalAdres
from ..serializers import SoortDigitaalAdresSerializer


@extend_schema(
    tags=["Soorten digitaal adres"],
)
@extend_schema_view(
    list=extend_schema(
        operation_id="getsoortendigitaaladres",
        description="De operatie waarmee gegevens van de referentielijst Soorten digitaal adres kunnen worden gezocht.",
    ),
    create=extend_schema(
        operation_id="postsoortdigitaaladres",
        description="De operatie waarmee gegevens van de referentielijst Soorten digitaal adres kunnen worden geregistreerd.",
    ),
    retrieve=extend_schema(
        operation_id="getsoortdigitaaladres",
        description="De operatie waarmee gegevens van de referentielijst Soorten digitaal adres kunnen worden geselecteerd.",
    ),
    update=extend_schema(
        operation_id="putsoortdigitaaladres",
        description="De operatie waarmee gegevens van de referentielijst Soorten digitaal adres kunnen worden gewijzigd.",
    ),
    destroy=extend_schema(
        operation_id="delsoortdigitaaladres",
        description="De operatie waarmee gegevens van de referentielijst Soorten digitaal adres kunnen worden verwijderd.",
    ),
)
class SoortDigitaalAdresViewSet(viewsets.ModelViewSet):
    __doc__ = SoortDigitaalAdres.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = SoortDigitaalAdres.objects.order_by("-pk")
    serializer_class = SoortDigitaalAdresSerializer
