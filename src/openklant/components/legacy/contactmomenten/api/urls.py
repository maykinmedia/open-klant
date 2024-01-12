from django.conf.urls import url
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularJSONAPIView,
    SpectacularRedocView,
)
from vng_api_common import routers

from .schema import info
from .viewsets import (
    ContactMomentAuditTrailViewSet,
    ContactMomentViewSet,
    CreateJWTSecretView,
    KlantContactMomentViewSet,
    ObjectContactMomentViewSet,
)

router = routers.DefaultRouter()
router.register(
    "contactmomenten",
    ContactMomentViewSet,
    [routers.nested("audittrail", ContactMomentAuditTrailViewSet)],
)
router.register("objectcontactmomenten", ObjectContactMomentViewSet)
router.register("klantcontactmomenten", KlantContactMomentViewSet)

urlpatterns = [
    url(
        r"^v(?P<version>\d+)/",
        include(
            [
                url(r"^", include(router.urls)),
                path("", router.APIRootView.as_view(), name="api-root-contactmomenten"),
                path(
                    "jwtsecret/", CreateJWTSecretView.as_view(), name="jwtsecret-create"
                ),
                path(
                    "schema/openapi.json",
                    SpectacularJSONAPIView.as_view(),
                    name="schema-json-contactmomenten",
                ),
                path(
                    "schema/openapi.yaml",
                    SpectacularAPIView.as_view(
                        urlconf="openklant.components.legacy.contactmomenten.api.urls",
                        custom_settings=info,
                    ),
                    name="schema-yaml-contactmomenten",
                ),
                path(
                    "schema/",
                    SpectacularRedocView.as_view(
                        url_name="schema-yaml-contactmomenten"
                    ),
                    name="schema-redoc-contactmomenten",
                ),
            ]
        ),
    ),
]
