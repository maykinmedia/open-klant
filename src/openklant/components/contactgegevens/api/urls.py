from django.conf.urls import url
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularJSONAPIView,
    SpectacularRedocView,
)
from vng_api_common import routers

from openklant.components.contactgegevens.api.viewset import (
    ContactgegevensViewSet,
    OrganisatieViewSet,
    PersoonViewSet,
)

from .schema import info

app_name = "contactgegevens"

router = routers.DefaultRouter()
router.register("organisatie", OrganisatieViewSet)
router.register("persoon", PersoonViewSet)
router.register("contactgegevens", ContactgegevensViewSet)

urlpatterns = [
    url(
        r"^v(?P<version>\d+)/",
        include(
            [
                url(r"^", include(router.urls)),
                path("", router.APIRootView.as_view(), name="api-root-contactgegevens"),
                path(
                    "schema/openapi.json",
                    SpectacularJSONAPIView.as_view(),
                    name="schema-json-contactgegevens",
                ),
                path(
                    "schema/openapi.yaml",
                    SpectacularAPIView.as_view(
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
