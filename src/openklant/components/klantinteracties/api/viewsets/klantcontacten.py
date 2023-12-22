from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.utils.mixins import ExpandMixin

from openklant.components.klantinteracties.api.filterset.klantcontacten import (
    BetrokkeneFilterSet,
    KlantcontactFilterSet,
)
from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    BetrokkeneSerializer,
    BijlageSerializer,
    KlantcontactSerializer,
    OnderwerpobjectSerializer,
)
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Bijlage,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.token.authentication import TokenAuthentication
from openklant.components.token.permission import TokenPermissions


class KlantcontactViewSet(ExpandMixin, viewsets.ModelViewSet):
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

    queryset = Klantcontact.objects.order_by("-pk").prefetch_related("bijlage_set")
    serializer_class = KlantcontactSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filterset_class = KlantcontactFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


class BetrokkeneViewSet(viewsets.ModelViewSet):
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
    filterset_class = BetrokkeneFilterSet
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


class OnderwerpobjectViewSet(viewsets.ModelViewSet):
    """
    create:
    Maak een onderwerpobject aan.

    Maak een onderwerpobject aan.

    list:
    Alle onderwerpobjecten opvragen.

    Alle onderwerpobjecten opvragen.

    retrieve:
    Een specifiek onderwerpobject opvragen.

    Een specifiek onderwerpobject opvragen.

    update:
    Werk een onderwerpobject in zijn geheel bij.

    Werk een onderwerpobject in zijn geheel bij.

    partial_update:
    Werk een onderwerpobject deels bij.

    Werk een onderwerpobject deels bij.

    destroy:
    Verwijder een onderwerpobject.

    Verwijder een onderwerpobject.
    """

    queryset = Onderwerpobject.objects.order_by("-pk")
    serializer_class = OnderwerpobjectSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "objectidentificator_objecttype",
        "objectidentificator_soort_object_id",
        "objectidentificator_object_id",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)


class BijlageViewSet(viewsets.ModelViewSet):
    """
    create:
    Maak een bijlage aan.

    Maak een bijlage aan.

    list:
    Alle bijlagen opvragen.

    Alle bijlagen opvragen.

    retrieve:
    Een specifiek bijlage opvragen.

    Een specifiek bijlage opvragen.

    update:
    Werk een bijlage in zijn geheel bij.

    Werk een bijlage in zijn geheel bij.

    partial_update:
    Werk een bijlage deels bij.

    Werk een bijlage deels bij.

    destroy:
    Verwijder een bijlage.

    Verwijder een bijlage.
    """

    queryset = Bijlage.objects.order_by("-pk")
    serializer_class = BijlageSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "objectidentificator_objecttype",
        "objectidentificator_soort_object_id",
        "objectidentificator_object_id",
    ]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenPermissions,)
