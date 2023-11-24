from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.contactgegevens.api.filtersets import (
    OrganisatieFilterSet,
    PersoonFilterSet,
)
from openklant.components.contactgegevens.api.serializers import (
    ContactgegevensSerializer,
    OrganisatieSerializer,
    PersoonSerializer,
)
from openklant.components.contactgegevens.models import (
    Contactgegevens,
    Organisatie,
    Persoon,
)


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
    filterset_class = OrganisatieFilterSet


class PersoonViewSet(viewsets.ModelViewSet):
    """
    De contact gegevens van een specifieke persoon

    create:
    Maak een persoon aan.

    Maak een persoon aan.

    list:
    Alle personen opvragen.

    Alle personen opvragen.

    retrieve:
    Een specifiek persoon opvragen.

    Een specifiek persoon opvragen.

    update:
    Werk een persoon in zijn geheel bij.

    Werk een persoon in zijn geheel bij.

    partial_update:
    Werk een persoon deels bij.

    Werk een persoon deels bij.

    destroy:
    Verwijder een persoon.

    Verwijder een persoon.
    """

    queryset = Persoon.objects.order_by("-pk")
    serializer_class = PersoonSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filterset_class = PersoonFilterSet


class ContactgegevensViewSet(viewsets.ModelViewSet):
    """
    De contact gegevens van een specifieke persoon

    create:
    Maak een persoon aan.

    Maak een persoon aan.

    list:
    Alle personen opvragen.

    Alle personen opvragen.

    retrieve:
    Een specifiek persoon opvragen.

    Een specifiek persoon opvragen.

    update:
    Werk een persoon in zijn geheel bij.

    Werk een persoon in zijn geheel bij.

    partial_update:
    Werk een persoon deels bij.

    Werk een persoon deels bij.

    destroy:
    Verwijder een persoon.

    Verwijder een persoon.
    """

    queryset = Contactgegevens.objects.order_by("-pk")
    serializer_class = ContactgegevensSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
