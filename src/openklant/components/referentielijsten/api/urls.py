from django.conf import settings
from django.urls import include, path, re_path

from vng_api_common import routers, schema

from . import viewsets
from .schema import info

app_name = "referentielijsten"

router = routers.DefaultRouter()
router.register("externeregisters", viewsets.ExternRegisterViewSet)
router.register("kanalen", viewsets.KanaalViewSet)
router.register("landen", viewsets.LandViewSet)
router.register("soortendigitaaladres", viewsets.SoortDigitaalAdresViewSet)
router.register("soortenobject", viewsets.SoortObjectViewSet)
router.register("soortenobjectid", viewsets.SoortObjectidViewSet)
router.register("talen", viewsets.TaalViewSet)


class SchemaView(schema.SchemaView):
    schema_path = settings.SPEC_URL["referentielijsten"]
    info = info


urlpatterns = [
    path(
        "v<version>/",
        include(
            [
                # API documentation
                re_path(
                    r"^schema/openapi(?P<format>\.json|\.yaml)$",
                    SchemaView.without_ui(cache_timeout=None),
                    name="schema-json-referentielijsten",
                ),
                path(
                    "schema/",
                    SchemaView.with_ui("redoc", cache_timeout=None),
                    name="schema-redoc-klantinteracties",
                ),
                path("", include(router.urls)),
            ]
        ),
    ),
]
