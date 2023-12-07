from django.conf import settings
from django.conf.urls import url
from django.urls import include, path

from vng_api_common import routers
from vng_api_common.schema import SchemaView as _SchemaView

from openklant.components.klantinteracties.api.viewsets.actoren import ActorViewSet
from openklant.components.klantinteracties.api.viewsets.digitaal_adres import (
    DigitaalAdresViewSet,
)
from openklant.components.klantinteracties.api.viewsets.internetaken import (
    InterneTaakViewSet,
)
from openklant.components.klantinteracties.api.viewsets.klantcontacten import (
    BetrokkeneViewSet,
    BijlageViewSet,
    KlantcontactViewSet,
    OnderwerpobjectViewSet,
)
from openklant.components.klantinteracties.api.viewsets.partijen import (
    PartijIdentificatorViewSet,
    PartijViewSet,
)

from .schema import info

app_name = "klantinteracties"

router = routers.DefaultRouter()
router.register("actoren", ActorViewSet)

router.register("digitaleadressen", DigitaalAdresViewSet)

router.register("klantcontacten", KlantcontactViewSet)
router.register("betrokkenen", BetrokkeneViewSet)
router.register("onderwerpobjecten", OnderwerpobjectViewSet)
router.register("bijlagen", BijlageViewSet)

router.register("internetaken", InterneTaakViewSet)

router.register("partijen", PartijViewSet)
router.register("partij-identificatoren", PartijIdentificatorViewSet)


class SchemaView(_SchemaView):
    schema_path = settings.SPEC_URL["klantinteracties"]
    info = info


# TODO: the EndpointEnumerator seems to choke on path and re_path

urlpatterns = [
    url(
        r"^v(?P<version>\d+)/",
        include(
            [
                # should not be picked up by drf-yasgs
                url(
                    r"^schema/openapi(?P<format>\.json|\.yaml)$",
                    SchemaView.without_ui(cache_timeout=None),
                    name="schema-json-klantinteracties",
                ),
                url(
                    r"^schema/$",
                    SchemaView.with_ui("redoc", cache_timeout=None),
                    name="schema-redoc-klantinteracties",
                ),
                # actual API
                url(r"^", include(router.urls)),
                path(
                    "", router.APIRootView.as_view(), name="api-root-klantinteracties"
                ),
                path("", include("vng_api_common.api.urls")),
            ]
        ),
    ),
]