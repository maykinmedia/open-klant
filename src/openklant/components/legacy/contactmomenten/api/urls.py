from django.urls import include, path, re_path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
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
    re_path(
        r"^v(?P<version>\d+)/",
        include(
            [
                re_path(r"^", include(router.urls)),
                path("", router.APIRootView.as_view(), name="api-root-contactmomenten"),
                path(
                    "jwtsecret/", CreateJWTSecretView.as_view(), name="jwtsecret-create"
                ),
                path(
                    "schema/openapi.json",
                    SpectacularJSONAPIView.as_view(
                        urlconf="openklant.components.legacy.contactmomenten.api.urls",
                        custom_settings=info,
                    ),
                    name="schema-json-contactmomenten",
                ),
                path(
                    "schema/openapi.yaml",
                    SpectacularYAMLAPIView.as_view(
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
