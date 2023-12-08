from django.conf import settings
from django.urls import include, path, re_path

from vng_api_common import routers
from vng_api_common.schema import SchemaView as _SchemaView

from ..api.schema import info
from .viewsets import KlantAuditTrailViewSet, KlantViewSet

router = routers.DefaultRouter()
router.register(
    "klanten",
    KlantViewSet,
    [routers.nested("audittrail", KlantAuditTrailViewSet)],
)


class SchemaView(_SchemaView):
    schema_path = settings.SPEC_URL["klanten"]
    info = info


# TODO: the EndpointEnumerator seems to choke on path and re_path

urlpatterns = [
    re_path(
        r"^v(?P<version>\d+)/",
        include(
            [
                # API documentation
                re_path(
                    r"^schema/openapi(?P<format>\.json|\.yaml)$",
                    SchemaView.without_ui(cache_timeout=None),
                    name="schema-json-klanten",
                ),
                re_path(
                    r"^schema/$",
                    SchemaView.with_ui("redoc", cache_timeout=None),
                    name="schema-redoc-klanten",
                ),
                # actual API
                re_path(r"^", include(router.urls)),
                # should not be picked up by drf-yasg
                path("", router.APIRootView.as_view(), name="api-root-klanten"),
                path("", include("vng_api_common.api.urls")),
            ]
        ),
    )
]
