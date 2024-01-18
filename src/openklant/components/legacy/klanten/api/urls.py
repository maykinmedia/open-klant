from django.urls import include, path, re_path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)
from vng_api_common import routers

from .schema import info
from .viewsets import CreateJWTSecretView, KlantAuditTrailViewSet, KlantViewSet

router = routers.DefaultRouter()
router.register(
    "klanten",
    KlantViewSet,
    [
        routers.nested(
            "audittrail",
            KlantAuditTrailViewSet,
            basename="audittrail",
        )
    ],
)

urlpatterns = [
    re_path(
        r"^v(?P<version>\d+)/",
        include(
            [
                re_path(r"^", include(router.urls)),
                path("", router.APIRootView.as_view(), name="api-root-klanten"),
                path(
                    "jwtsecret/", CreateJWTSecretView.as_view(), name="jwtsecret-create"
                ),
                path(
                    "schema/openapi.json",
                    SpectacularJSONAPIView.as_view(
                        urlconf="openklant.components.legacy.klanten.api.urls",
                        custom_settings=info,
                    ),
                    name="schema-json-klanten",
                ),
                path(
                    "schema/openapi.yaml",
                    SpectacularYAMLAPIView.as_view(
                        urlconf="openklant.components.legacy.klanten.api.urls",
                        custom_settings=info,
                    ),
                    name="schema-yaml-klanten",
                ),
                path(
                    "schema/",
                    SpectacularRedocView.as_view(url_name="schema-yaml-klanten"),
                    name="schema-redoc-klanten",
                ),
            ]
        ),
    ),
]
