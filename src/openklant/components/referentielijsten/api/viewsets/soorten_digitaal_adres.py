from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from ...models import SoortDigitaalAdres
from ..serializers import SoortDigitaalAdresSerializer


class SoortDigitaalAdresViewSet(viewsets.ModelViewSet):
    lookup_field = "code"
    pagination_class = PageNumberPagination
    queryset = SoortDigitaalAdres.objects.order_by("-pk")
    serializer_class = SoortDigitaalAdresSerializer
