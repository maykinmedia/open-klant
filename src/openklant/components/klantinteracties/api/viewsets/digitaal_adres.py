from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresSerializer,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres


class DigitaalAdresViewSet(viewsets.ModelViewSet):
    """
    Digitaal adres dat een betrokkene bij klantcontact verstrekte
    voor gebruik bij opvolging van een klantcontact.

    create:
    Maak een digitaal adres aan.

    Maak een digitaal adres aan.

    list:
    Alle digitale adressen opvragen.

    Alle digitale adressen opvragen.

    retrieve:
    Een specifiek digitaal adres opvragen.

    Een specifiek digitaal adres opvragen.

    update:
    Werk een digitaal adres in zijn geheel bij.

    Werk een digitaal adres in zijn geheel bij.

    partial_update:
    Werk een digitaal adres deels bij.

    Werk een digitaal adres deels bij.

    destroy:
    Verwijder een digitaal adres.

    Verwijder een digitaal adres.
    """

    queryset = DigitaalAdres.objects.order_by("-pk")
    serializer_class = DigitaalAdresSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
