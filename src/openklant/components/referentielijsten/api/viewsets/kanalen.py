from rest_framework import viewsets

from ...models import Kanaal
from ..serializers import KanaalSerializer


class KanaalViewSet(viewsets.ModelViewSet):
    __doc__ = Kanaal.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = Kanaal.objects.order_by("-pk")
    serializer_class = KanaalSerializer
