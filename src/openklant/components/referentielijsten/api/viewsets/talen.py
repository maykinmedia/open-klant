from rest_framework import viewsets

from ...models import Taal
from ..serializers import TaalSerializer


class TaalViewSet(viewsets.ModelViewSet):
    __doc__ = Taal.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = Taal.objects.order_by("-pk")
    serializer_class = TaalSerializer
