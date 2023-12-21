from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from ...models import ExternRegister
from ..serializers import ExternRegisterSerializer


class ExternRegisterViewSet(viewsets.ModelViewSet):
    lookup_field = "code"
    pagination_class = PageNumberPagination
    queryset = ExternRegister.objects.order_by("-pk")
    serializer_class = ExternRegisterSerializer
