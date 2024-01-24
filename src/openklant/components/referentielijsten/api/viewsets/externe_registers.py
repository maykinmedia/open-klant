from rest_framework import viewsets

from ...models import ExternRegister
from ..serializers import ExternRegisterSerializer


class ExternRegisterViewSet(viewsets.ModelViewSet):
    __doc__ = ExternRegister.__doc__
    lookup_field = "code"
    pagination_class = None
    queryset = ExternRegister.objects.order_by("-pk")
    serializer_class = ExternRegisterSerializer
