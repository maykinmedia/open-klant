from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from ...models import Taal
from ..serializers import TaalSerializer


class TaalViewSet(viewsets.ModelViewSet):
    lookup_field = "code"
    pagination_class = PageNumberPagination
    queryset = Taal.objects.order_by("-pk")
    serializer_class = TaalSerializer
