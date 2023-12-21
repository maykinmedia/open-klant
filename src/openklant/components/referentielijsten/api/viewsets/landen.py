from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from ...models import Land
from ..serializers import LandSerializer


class LandViewSet(viewsets.ModelViewSet):
    # TODO? filterset_class  filter vigerend?
    lookup_field = "landcode"
    pagination_class = PageNumberPagination
    queryset = Land.objects.order_by("-pk")
    serializer_class = LandSerializer
