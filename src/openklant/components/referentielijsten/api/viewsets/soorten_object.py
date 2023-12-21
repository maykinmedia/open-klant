from rest_framework import viewsets

from ...models import SoortObject
from ..serializers import SoortObjectSerializer


class SoortObjectViewSet(viewsets.ModelViewSet):
    __doc__ = SoortObject.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = SoortObject.objects.order_by("-pk")
    serializer_class = SoortObjectSerializer
