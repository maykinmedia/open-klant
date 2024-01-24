from rest_framework import viewsets

from ...models import SoortDigitaalAdres
from ..serializers import SoortDigitaalAdresSerializer


class SoortDigitaalAdresViewSet(viewsets.ModelViewSet):
    __doc__ = SoortDigitaalAdres.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = SoortDigitaalAdres.objects.order_by("-pk")
    serializer_class = SoortDigitaalAdresSerializer
