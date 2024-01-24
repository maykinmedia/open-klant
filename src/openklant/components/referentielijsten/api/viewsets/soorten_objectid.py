from rest_framework import viewsets

from ...models import SoortObjectid
from ..serializers import SoortObjectidSerializer


class SoortObjectidViewSet(viewsets.ModelViewSet):
    __doc__ = SoortObjectid.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = SoortObjectid.objects.order_by("-pk")
    serializer_class = SoortObjectidSerializer
