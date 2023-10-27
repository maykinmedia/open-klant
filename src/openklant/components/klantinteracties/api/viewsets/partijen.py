from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.serializers.partijen import (
    ContactpersoonSerializer,
    OrganisatieSerializer,
    PartijIdentificatorSerializer,
    PartijSerializer,
    PersoonSerializer,
)
from openklant.components.klantinteracties.models.partijen import (
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
    Persoon,
)


class PartijViewSet(viewsets.ModelViewSet):
    """
    Persoon of organisatie waarmee de gemeente een relatie heeft.

    create:
    Maak een partij aan.

    Maak een partij aan.

    list:
    Alle partijen opvragen.

    Alle partijen opvragen.

    retrieve:
    Een specifiek partij opvragen.

    Een specifiek partij opvragen.

    update:
    Werk een partij in zijn geheel bij.

    Werk een partij in zijn geheel bij.

    partial_update:
    Werk een partij deels bij.

    Werk een partij deels bij.

    destroy:
    Verwijder een partij.

    Verwijder een partij.
    """

    queryset = Partij.objects.order_by("-pk")
    serializer_class = PartijSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination


class OrganisatieViewSet(viewsets.ModelViewSet):
    """
    Geformaliseerde entiteit die geen natuurlijk persoon is
    en maatschappelijke activiteiten uitvoert.

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
    lookup_field = "id"
    pagination_class = PageNumberPagination


class PersoonViewSet(viewsets.ModelViewSet):
    """
    Natuurlijk persoon.

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
    lookup_field = "id"
    pagination_class = PageNumberPagination


class ContactpersoonViewSet(viewsets.ModelViewSet):
    """
    Natuurlijk persoon die werkte voor een organisatie,
    of natuurlijk persoon die een andere persoon vertegenwoordigde.

    create:
    Maak een contactpersoon aan.

    Maak een contactpersoon aan.

    list:
    Alle contactpersonen opvragen.

    Alle contactpersonen opvragen.

    retrieve:
    Een specifiek contactpersoon opvragen.

    Een specifiek contactpersoon opvragen.

    update:
    Werk een contactpersoon in zijn geheel bij.

    Werk een contactpersoon in zijn geheel bij.

    partial_update:
    Werk een contactpersoon deels bij.

    Werk een contactpersoon deels bij.

    destroy:
    Verwijder een contactpersoon.

    Verwijder een contactpersoon.
    """

    queryset = Contactpersoon.objects.order_by("-pk")
    serializer_class = ContactpersoonSerializer
    lookup_field = "id"
    pagination_class = PageNumberPagination


class PartijIdentificatorViewSet(viewsets.ModelViewSet):
    """
    Gegevens die een partij in een basisregistratie of ander extern register uniek identificeren.

    create:
    Maak een partij-identificator aan.

    Maak een partij-identificator aan.

    list:
    Alle partij-identificatoren opvragen.

    Alle partij-identificatoren opvragen.

    retrieve:
    Een specifiek partij-identificator opvragen.

    Een specifiek partij-identificator opvragen.

    update:
    Werk een partij-identificator in zijn geheel bij.

    Werk een partij-identificator in zijn geheel bij.

    partial_update:
    Werk een partij-identificator deels bij.

    Werk een partij-identificator deels bij.

    destroy:
    Verwijder een partij-identificator.

    Verwijder een partij-identificator.
    """

    queryset = PartijIdentificator.objects.order_by("-pk")
    serializer_class = PartijIdentificatorSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
