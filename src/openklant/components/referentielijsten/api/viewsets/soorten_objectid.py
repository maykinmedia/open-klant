from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from ...models import SoortObjectid
from ..serializers import SoortObjectidSerializer


class SoortObjectidViewSet(viewsets.ModelViewSet):
    lookup_field = "code"
    pagination_class = PageNumberPagination
    queryset = SoortObjectid.objects.order_by("-pk")
    serializer_class = SoortObjectidSerializer
