from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularJSONAPIView,
    SpectacularRedocView,
)
from vng_api_common import routers

from . import viewsets
from .schema import custom_settings

app_name = "referentielijsten"

router = routers.DefaultRouter()
router.register("externeregisters", viewsets.ExternRegisterViewSet)
router.register("kanalen", viewsets.KanaalViewSet)
router.register("landen", viewsets.LandViewSet)
router.register("soortendigitaaladres", viewsets.SoortDigitaalAdresViewSet)
router.register("soortenobject", viewsets.SoortObjectViewSet)
router.register("soortenobjectid", viewsets.SoortObjectidViewSet)
router.register("talen", viewsets.TaalViewSet)


urlpatterns = [
    path(
        "v0/",
        include(
            [
                # API documentation
                path(
                    "schema/",
                    SpectacularRedocView.as_view(
                        url_name=f"{app_name}:schema-yaml-referentielijsten",
                    ),
                    name="schema-redoc-klantinteracties",
                ),
                path(
                    "schema/openapi.json",
                    SpectacularJSONAPIView.as_view(
                        urlconf="openklant.components.referentielijsten.api.urls",
                        custom_settings=custom_settings,
                    ),
                    name="schema-json-referentielijsten",
                ),
                path(
                    "schema/openapi.yaml",
                    SpectacularAPIView.as_view(
                        urlconf="openklant.components.referentielijsten.api.urls",
                        custom_settings=custom_settings,
                    ),
                    name="schema-yaml-referentielijsten",
                ),
                path("", include(router.urls)),
            ]
        ),
    ),
]
