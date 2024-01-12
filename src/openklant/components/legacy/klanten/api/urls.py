from django.conf.urls import url
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularJSONAPIView,
    SpectacularRedocView,
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
    url(
        r"^v(?P<version>\d+)/",
        include(
            [
                url(r"^", include(router.urls)),
                path("", router.APIRootView.as_view(), name="api-root-klanten"),
                path(
                    "jwtsecret/", CreateJWTSecretView.as_view(), name="jwtsecret-create"
                ),
                path(
                    "schema/openapi.json",
                    SpectacularJSONAPIView.as_view(),
                    name="schema-json-klanten",
                ),
                path(
                    "schema/openapi.yaml",
                    SpectacularAPIView.as_view(
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
