from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from vng_api_common.audittrails.viewsets import AuditTrailViewsetMixin

from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    BetrokkeneSerializer,
    KlantcontactSerializer,
)
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Klantcontact,
)


class KlantcontactViewSet(
    NotificationViewSetMixin, AuditTrailViewsetMixin, viewsets.ModelViewSet
):
    """
    Contact tussen een klant of een vertegenwoordiger van een
    klant en de gemeente over een onderwerp.

    create:
    Maak een klant contact aan.

    Maak een klant contact aan.

    list:
    Alle klanten contacten opvragen.

    Alle klanten contacten opvragen.

    retrieve:
    Een specifiek klant contact opvragen.

    Een specifiek klant contact opvragen.

    update:
    Werk een klant contact in zijn geheel bij.

    Werk een klant contact in zijn geheel bij.

    partial_update:
    Werk een klant contact deels bij.

    Werk een klant contact deels bij.

    destroy:
    Verwijder een klant contact.

    Verwijder een klant contact.
    """

    queryset = Klantcontact.objects.order_by("-pk")
    serializer_class = KlantcontactSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination


class BetrokkeneViewSet(
    NotificationViewSetMixin, AuditTrailViewsetMixin, viewsets.ModelViewSet
):
    """
    Ofwel betrokkenheid van een partij bij een klantcontact, eventueel aangevuld met
    specifiek voor opvolging van dat klantcontact te gebruiken contactgegevens, ofwel
    voor opvolging van een klantcontact te gebruiken contactgegevens van een tijdens
    dat klantcontact niet als partij gekende persoon.

    create:
    Maak een betrokkene aan.

    Maak een betrokkene aan.

    list:
    Alle betrokkeneen opvragen.

    Alle betrokkeneen opvragen.

    retrieve:
    Een specifiek betrokkene opvragen.

    Een specifiek betrokkene opvragen.

    update:
    Werk een betrokkene in zijn geheel bij.

    Werk een betrokkene in zijn geheel bij.

    partial_update:
    Werk een betrokkene deels bij.

    Werk een betrokkene deels bij.

    destroy:
    Verwijder een betrokkene.

    Verwijder een betrokkene.
    """

    queryset = Betrokkene.objects.order_by("-pk")
    serializer_class = BetrokkeneSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
