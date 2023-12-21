from rest_framework import viewsets

from ...models import Land
from ..serializers import LandSerializer


class LandViewSet(viewsets.ModelViewSet):
    __doc__ = Land.__doc__
    lookup_field = "landcode"
    pagination_class = None
    queryset = Land.objects.order_by("-pk")
    serializer_class = LandSerializer
