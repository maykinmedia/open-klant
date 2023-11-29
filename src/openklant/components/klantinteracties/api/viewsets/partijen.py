from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.filterset.partijen import PartijFilterSet
from openklant.components.klantinteracties.api.serializers.partijen import (
    OrganisatieRetrieveSerializer,
    PartijIdentificatorSerializer,
    PartijSerializer,
)
from openklant.components.klantinteracties.models.partijen import (
    Organisatie,
    Partij,
    PartijIdentificator,
)
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions


class OrganisatieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Geformaliseerde entiteit die geen natuurlijk persoon is
    en maatschappelijke activiteiten uitvoert.

    list:
    Alle organisaties opvragen.
    Alle organisaties opvragen.
    retrieve:

    Een specifiek organisatie opvragen.
    Een specifiek organisatie opvragen.
    """

    queryset = Organisatie.objects.order_by("-pk")
    serializer_class = OrganisatieRetrieveSerializer
    lookup_field = "id"
    pagination_class = PageNumberPagination


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
    filterset_class = PartijFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
