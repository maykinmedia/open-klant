import logging

from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ValidationError
from rest_framework.settings import api_settings
from vng_api_common.audittrails.viewsets import (
    AuditTrailViewSet,
    AuditTrailViewsetMixin,
)
from vng_api_common.notifications.viewsets import NotificationViewSetMixin
from vng_api_common.permissions import AuthScopesRequired
from vng_api_common.viewsets import CheckQueryParamsMixin

from ..datamodel.models import ContactMoment, KlantContactMoment, ObjectContactMoment
from .audits import AUDIT_CONTACTMOMENTEN
from .filters import (
    ContactMomentFilter,
    KlantContactMomentFilter,
    ObjectContactMomentFilter,
)
from .kanalen import KANAAL_CONTACTMOMENTEN
from .scopes import (
    SCOPE_CONTACTMOMENTEN_AANMAKEN,
    SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
    SCOPE_CONTACTMOMENTEN_ALLES_VERWIJDEREN,
    SCOPE_CONTACTMOMENTEN_BIJWERKEN,
)
from .serializers import (
    ContactMomentSerializer,
    KlantContactMomentSerializer,
    ObjectContactMomentSerializer,
)
from .validators import ObjectContactMomentDestroyValidator

logger = logging.getLogger(__name__)


class ContactMomentViewSet(
    CheckQueryParamsMixin,
    NotificationViewSetMixin,
    AuditTrailViewsetMixin,
    viewsets.ModelViewSet,
):
    """
    Opvragen en bewerken van CONTACTMOMENTen.

    create:
    Maak een CONTACTMOMENT aan.

    Maak een CONTACTMOMENT aan.

    list:
    Alle CONTACTMOMENTen opvragen.

    Alle CONTACTMOMENTen opvragen.

    retrieve:
    Een specifiek CONTACTMOMENT opvragen.

    Een specifiek CONTACTMOMENT opvragen.

    update:
    Werk een CONTACTMOMENT in zijn geheel bij.

    Werk een CONTACTMOMENT in zijn geheel bij.

    partial_update:
    Werk een CONTACTMOMENT deels bij.

    Werk een CONTACTMOMENT deels bij.

    destroy:
    Verwijder een CONTACTMOMENT.

    Verwijder een CONTACTMOMENT.
    """

    queryset = ContactMoment.objects.all().order_by("-registratiedatum")
    serializer_class = ContactMomentSerializer
    filterset_class = ContactMomentFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
        "retrieve": SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
        "create": SCOPE_CONTACTMOMENTEN_AANMAKEN,
        "update": SCOPE_CONTACTMOMENTEN_BIJWERKEN,
        "partial_update": SCOPE_CONTACTMOMENTEN_BIJWERKEN,
        "destroy": SCOPE_CONTACTMOMENTEN_ALLES_VERWIJDEREN,
    }
    notifications_kanaal = KANAAL_CONTACTMOMENTEN
    audit = AUDIT_CONTACTMOMENTEN


class ObjectContactMomentViewSet(
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en verwijderen van OBJECT-CONTACTMOMENT relaties.

    Het betreft een relatie tussen een willekeurig OBJECT, bijvoorbeeld een
    ZAAK in de Zaken API, en een CONTACTMOMENT.

    create:
    Maak een OBJECT-CONTACTMOMENT relatie aan.

    Maak een OBJECT-CONTACTMOMENT relatie aan.

    **LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

    Andere API's, zoals de Zaken API, gebruiken dit
    endpoint bij het synchroniseren van relaties.

    list:
    Alle OBJECT-CONTACTMOMENT relaties opvragen.

    Alle OBJECT-CONTACTMOMENT relaties opvragen.

    retrieve:
    Een specifiek OBJECT-CONTACTMOMENT relatie opvragen.

    Een specifiek OBJECT-CONTACTMOMENT relatie opvragen.

    destroy:
    Verwijder een OBJECT-CONTACTMOMENT relatie.

    Verwijder een OBJECT-CONTACTMOMENT relatie.

    **LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

    Andere API's, zoals de Zaken API, gebruiken dit
    endpoint bij het synchroniseren van relaties.
    """

    queryset = ObjectContactMoment.objects.all()
    serializer_class = ObjectContactMomentSerializer
    filterset_class = ObjectContactMomentFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
        "retrieve": SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
        "create": SCOPE_CONTACTMOMENTEN_AANMAKEN,
        "destroy": SCOPE_CONTACTMOMENTEN_ALLES_VERWIJDEREN,
    }

    def perform_destroy(self, instance):
        # destroy is only allowed if the remote relation does no longer exist, so check for that
        validator = ObjectContactMomentDestroyValidator()

        try:
            validator(instance)
        except ValidationError as exc:
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: exc}, code=exc.detail[0].code
            )
        else:
            super().perform_destroy(instance)


class ContactMomentAuditTrailViewSet(AuditTrailViewSet):
    """
    Opvragen van de audit trail regels.

    list:
    Alle audit trail regels behorend bij de CONTACTMOMENT.

    Alle audit trail regels behorend bij de CONTACTMOMENT.

    retrieve:
    Een specifieke audit trail regel opvragen.

    Een specifieke audit trail regel opvragen.
    """

    main_resource_lookup_field = "contactmoment_uuid"


class KlantContactMomentViewSet(
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en verwijderen van OBJECT-CONTACTMOMENT relaties.

    Het betreft een relatie tussen een KLANT (uit de Klanten API) en een CONTACTMOMENT.

    create:
    Maak een KLANT-CONTACTMOMENT relatie aan.

    Registreer een CONTACTMOMENT bij een KLANT.

    **Er wordt gevalideerd op**

    * geldigheid `contactmoment` URL
    * geldigheid `klant` URL
    * de combinatie `contactmoment` en `klant` moet uniek zijn

    list:
    Alle KLANT-CONTACTMOMENT relaties opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke KLANT-CONTACTMOMENT relatie opvragen.

    Een specifieke KLANT-CONTACTMOMENT relatie opvragen.

    destroy:
    Verwijder een KLANT-CONTACTMOMENT relatie.

    Verwijder een KLANT-CONTACTMOMENT relatie.
    """

    queryset = KlantContactMoment.objects.all()
    serializer_class = KlantContactMomentSerializer
    filterset_class = KlantContactMomentFilter
    pagination_class = PageNumberPagination
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    required_scopes = {
        "list": SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
        "retrieve": SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
        "create": SCOPE_CONTACTMOMENTEN_AANMAKEN,
        "destroy": SCOPE_CONTACTMOMENTEN_ALLES_VERWIJDEREN,
    }
