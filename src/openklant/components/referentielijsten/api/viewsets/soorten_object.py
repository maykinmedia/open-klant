from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from ...models import SoortObject
from ..serializers import SoortObjectSerializer


class SoortObjectViewSet(viewsets.ModelViewSet):
    lookup_field = "code"
    pagination_class = PageNumberPagination
    queryset = SoortObject.objects.order_by("-pk")
    serializer_class = SoortObjectSerializer
