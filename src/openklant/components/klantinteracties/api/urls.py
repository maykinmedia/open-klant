from django.conf import settings
from django.urls import include, path, re_path

from vng_api_common import routers
from vng_api_common.schema import SchemaView as _SchemaView

from openklant.components.klantinteracties.api.viewsets.actoren import (
    ActorViewSet,
    GeautomatiseerdeActorViewSet,
    MedewerkerViewSet,
    OrganisatorischeEenheidViewSet,
)
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
    ContactpersoonViewSet,
    OrganisatieViewSet,
    PartijIdentificatorViewSet,
    PartijViewSet,
    PersoonViewSet,
)

from .schema import info

router = routers.DefaultRouter()
router.register("actoren", ActorViewSet)
router.register("geautomatiseerde_actoren", GeautomatiseerdeActorViewSet)
router.register("medewerker", MedewerkerViewSet)
router.register("organisatorische_eenheid", OrganisatorischeEenheidViewSet)

router.register("digitaal_adres", DigitaalAdresViewSet)

router.register("klantcontact", KlantcontactViewSet)
router.register("betrokkene", BetrokkeneViewSet)
router.register("onderwerpobject", OnderwerpobjectViewSet)
router.register("bijlage", BijlageViewSet)

router.register("interne_taak", InterneTaakViewSet)

router.register("partij", PartijViewSet)
router.register("organisatie", OrganisatieViewSet)
router.register("persoon", PersoonViewSet)
router.register("contact_persoon", ContactpersoonViewSet)
router.register("partij_identificator", PartijIdentificatorViewSet)


class SchemaView(_SchemaView):
    schema_path = settings.SPEC_URL["klantinteracties"]
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
                    name="schema-json-contactmomenten",
                ),
                re_path(
                    r"^schema/$",
                    SchemaView.with_ui("redoc", cache_timeout=None),
                    name="schema-redoc-contactmomenten",
                ),
                # actual API
                re_path(r"^", include(router.urls)),
                # should not be picked up by drf-yasg
                path("", router.APIRootView.as_view(), name="api-root-contactmomenten"),
                path("", include("vng_api_common.api.urls")),
            ]
        ),
    )
]
