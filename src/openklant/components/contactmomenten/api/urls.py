from django.conf import settings
from django.conf.urls import url
from django.urls import include, path

from vng_api_common import routers
from vng_api_common.schema import SchemaView as _SchemaView

from .schema import info
from .viewsets import (
    ContactMomentAuditTrailViewSet,
    ContactMomentViewSet,
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


class SchemaView(_SchemaView):
    schema_path = settings.SPEC_URL["contactmomenten"]
    info = info


# TODO: the EndpointEnumerator seems to choke on path and re_path

urlpatterns = [
    url(
        r"^v(?P<version>\d+)/",
        include(
            [
                # API documentation
                url(
                    r"^schema/openapi(?P<format>\.json|\.yaml)$",
                    SchemaView.without_ui(cache_timeout=None),
                    name="schema-json-contactmomenten",
                ),
                url(
                    r"^schema/$",
                    SchemaView.with_ui("redoc", cache_timeout=None),
                    name="schema-redoc-contactmomenten",
                ),
                # actual API
                url(r"^", include(router.urls)),
                # should not be picked up by drf-yasg
                path("", router.APIRootView.as_view(), name="api-root-contactmomenten"),
                path("", include("vng_api_common.api.urls")),
            ]
        ),
    )
]
