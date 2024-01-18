from django.urls import include, path, re_path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)
from vng_api_common import routers

from openklant.components.contactgegevens.api.viewset import (
    OrganisatieViewSet,
    PersoonViewSet,
)

from .schema import info

app_name = "contactgegevens"

router = routers.DefaultRouter()
router.register("organisatie", OrganisatieViewSet)
router.register("persoon", PersoonViewSet)

urlpatterns = [
    re_path(
        r"^v(?P<version>\d+)/",
        include(
            [
                re_path(r"^", include(router.urls)),
                path("", router.APIRootView.as_view(), name="api-root-contactgegevens"),
                path(
                    "schema/openapi.json",
                    SpectacularJSONAPIView.as_view(
                        urlconf="openklant.components.contactgegevens.api.urls",
                        custom_settings=info,
                    ),
                    name="schema-json-contactgegevens",
                ),
                path(
                    "schema/openapi.yaml",
                    SpectacularYAMLAPIView.as_view(
                        urlconf="openklant.components.contactgegevens.api.urls",
                        custom_settings=info,
                    ),
                    name="schema-yaml-contactgegevens",
                ),
                path(
                    "schema/",
                    SpectacularRedocView.as_view(
                        url_name="contactgegevens:schema-yaml-contactgegevens"
                    ),
                    name="schema-redoc-contactgegevens",
                ),
            ]
        ),
    ),
]
