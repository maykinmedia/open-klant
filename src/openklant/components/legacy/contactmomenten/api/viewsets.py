import logging

from django.db.models import Prefetch

from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ValidationError
from rest_framework.settings import api_settings
from vng_api_common.api.views import CreateJWTSecretView as VNGCreateJWTSecretView
from vng_api_common.audittrails.viewsets import (
    AuditTrailViewSet,
    AuditTrailViewsetMixin,
)
from vng_api_common.permissions import AuthScopesRequired
from vng_api_common.viewsets import CheckQueryParamsMixin

from openklant.components.legacy.authorization import JWTDummyAuthentication

from ..models.contactmomenten import (
    ContactMoment,
    KlantContactMoment,
    ObjectContactMoment,
)
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


@extend_schema(
    tags=["contactmomenten"],
)
@extend_schema_view(
    list=extend_schema(
        summary="Alle CONTACTMOMENTen opvragen.",
        description="Alle CONTACTMOMENTen opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek CONTACTMOMENT opvragen.",
        description="Een specifiek CONTACTMOMENT opvragen.",
        parameters=[
            OpenApiParameter(
                name="expand",
                description="Haal details van inline resources direct op.",
                type=str,
                enum=ContactMomentSerializer.Meta.expandable_fields,
            ),
        ],
    ),
    update=extend_schema(
        summary="Werk een CONTACTMOMENT in zijn geheel bij.",
        description="Werk een CONTACTMOMENT in zijn geheel bij.",
    ),
    partial_update=extend_schema(
        summary="Werk een CONTACTMOMENT deels bij.",
        description="Werk een CONTACTMOMENT deels bij.",
    ),
    create=extend_schema(
        summary="Maak een CONTACTMOMENT aan.",
        description="Maak een CONTACTMOMENT aan.",
    ),
    destroy=extend_schema(
        summary="Verwijder een CONTACTMOMENT.",
        description="Verwijder een CONTACTMOMENT.",
    ),
)
class ContactMomentViewSet(
    CheckQueryParamsMixin,
    NotificationViewSetMixin,
    AuditTrailViewsetMixin,
    viewsets.ModelViewSet,
):
    """Opvragen en bewerken van CONTACTMOMENTen."""

    queryset = (
        ContactMoment.objects.all()
        .prefetch_related(
            Prefetch(
                "klantcontactmoment_set",
                queryset=KlantContactMoment.objects.order_by("-pk"),
            )
        )
        .prefetch_related(
            Prefetch(
                "objectcontactmoment_set",
                queryset=ObjectContactMoment.objects.order_by("-pk"),
            )
        )
        .order_by("-registratiedatum")
    )
    serializer_class = ContactMomentSerializer
    filterset_class = ContactMomentFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    authentication_classes = (JWTDummyAuthentication,)
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

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["objectcontactmomenten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle OBJECT-CONTACTMOMENT relaties opvragen.",
        description="Alle OBJECT-CONTACTMOMENT relaties opvragen.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek OBJECT-CONTACTMOMENT relatie opvragen.",
        description="Een specifiek OBJECT-CONTACTMOMENT relatie opvragen.",
    ),
    create=extend_schema(
        summary="Maak een OBJECT-CONTACTMOMENT relatie aan.",
        description="""Maak een OBJECT-CONTACTMOMENT relatie aan.

**LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

Andere API's, zoals de Zaken API, gebruiken dit
endpoint bij het synchroniseren van relaties.""",
    ),
    destroy=extend_schema(
        summary="Verwijder een OBJECT-CONTACTMOMENT relatie.",
        description="""Verwijder een OBJECT-CONTACTMOMENT relatie.

**LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

Andere API's, zoals de Zaken API, gebruiken dit
endpoint bij het synchroniseren van relaties.""",
    ),
)
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
    """

    queryset = ObjectContactMoment.objects.order_by("-pk")
    serializer_class = ObjectContactMomentSerializer
    filterset_class = ObjectContactMomentFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    authentication_classes = (JWTDummyAuthentication,)
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


@extend_schema(tags=["contactmomenten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle audit trail regels behorend bij de CONTACTMOMENT.",
        description="Alle audit trail regels behorend bij de CONTACTMOMENT.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke audit trail regel opvragen. ",
        description="Een specifieke audit trail regel opvragen",
    ),
)
class ContactMomentAuditTrailViewSet(AuditTrailViewSet):
    """Opvragen van de audit trail regels."""

    main_resource_lookup_field = "contactmoment_uuid"
    authentication_classes = (JWTDummyAuthentication,)

    def initialize_request(self, request, *args, **kwargs):
        # workaround for drf-nested-viewset injecting the URL kwarg into request.data
        return super(viewsets.GenericViewSet, self).initialize_request(
            request, *args, **kwargs
        )


@extend_schema(tags=["klantcontactmomenten"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle KLANT-CONTACTMOMENT relaties opvragen.",
        description="""Alle KLANT-CONTACTMOMENT relaties opvragen.

 Deze lijst kan gefilterd wordt met query-string parameters.""",
    ),
    retrieve=extend_schema(
        summary="Een specifieke KLANT-CONTACTMOMENT relatie opvragen.",
        description="Een specifieke KLANT-CONTACTMOMENT relatie opvragen.",
    ),
    update=extend_schema(
        summary="Werk een KLANT-CONTACTMOMENT in zijn geheel bij.",
        description="""Werk een KLANT-CONTACTMOMENT in zijn geheel bij.

*AFWIJKING: Werk een KLANT-CONTACTMOMENT in zijn geheel bij.""",
    ),
    partial_update=extend_schema(
        summary="Werk een KLANT-CONTACTMOMENT deels bij. ",
        description="""Werk een KLANT-CONTACTMOMENT deels bij.

*AFWIJKING: Werk een KLANT-CONTACTMOMENT deels bij.""",
    ),
    create=extend_schema(
        summary="Maak een KLANT-CONTACTMOMENT relatie aan.",
        description="""Maak een KLANT-CONTACTMOMENT relatie aan.

Registreer een CONTACTMOMENT bij een KLANT.

**Er wordt gevalideerd op**

* geldigheid `contactmoment` URL
* geldigheid `klant` URL
* de combinatie `contactmoment` en `klant` moet uniek zijn""",
    ),
    destroy=extend_schema(
        summary="Verwijder een KLANT-CONTACTMOMENT relatie.",
        description="Verwijder een KLANT-CONTACTMOMENT relatie.",
    ),
)
class KlantContactMomentViewSet(CheckQueryParamsMixin, viewsets.ModelViewSet):
    """
    Opvragen en verwijderen van OBJECT-CONTACTMOMENT relaties.

    Het betreft een relatie tussen een KLANT (uit de Klanten API) en een CONTACTMOMENT.
    """

    queryset = KlantContactMoment.objects.order_by("-pk")
    serializer_class = KlantContactMomentSerializer
    filterset_class = KlantContactMomentFilter
    pagination_class = PageNumberPagination
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    authentication_classes = (JWTDummyAuthentication,)
    required_scopes = {
        "list": SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
        "retrieve": SCOPE_CONTACTMOMENTEN_ALLES_LEZEN,
        "create": SCOPE_CONTACTMOMENTEN_AANMAKEN,
        "update": SCOPE_CONTACTMOMENTEN_AANMAKEN,
        "partial_update": SCOPE_CONTACTMOMENTEN_AANMAKEN,
        "destroy": SCOPE_CONTACTMOMENTEN_ALLES_VERWIJDEREN,
    }


@extend_schema(exclude=True)
class CreateJWTSecretView(VNGCreateJWTSecretView):
    pass
