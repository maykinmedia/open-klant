from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.contactgegevens.api.serializers import OrganisatieSerializer
from openklant.components.contactgegevens.models import Organisatie


class OrganisatieViewSet(viewsets.ModelViewSet):
    """
    De contact gegevens van een specifieke organisatie

    create:
    Maak een organisatie aan.

    Maak een organisatie aan.

    list:
    Alle organisaties opvragen.

    Alle organisaties opvragen.

    retrieve:
    Een specifiek organisatie opvragen.

    Een specifiek organisatie opvragen.

    update:
    Werk een organisatie in zijn geheel bij.

    Werk een organisatie in zijn geheel bij.

    partial_update:
    Werk een organisatie deels bij.

    Werk een organisatie deels bij.

    destroy:
    Verwijder een organisatie.

    Verwijder een organisatie.
    """

    queryset = Organisatie.objects.order_by("-pk")
    serializer_class = OrganisatieSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
