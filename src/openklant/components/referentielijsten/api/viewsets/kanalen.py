from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from ...models import Kanaal
from ..serializers import KanaalSerializer


class KanaalViewSet(viewsets.ModelViewSet):
    lookup_field = "code"
    pagination_class = PageNumberPagination
    queryset = Kanaal.objects.order_by("-pk")
    serializer_class = KanaalSerializer
