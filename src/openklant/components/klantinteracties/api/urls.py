from django.urls import include, path, re_path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)
from vng_api_common import routers

from openklant.components.klantinteracties.api.viewsets.actoren import ActorViewSet
from openklant.components.klantinteracties.api.viewsets.digitaal_adres import (
    DigitaalAdresViewSet,
)
from openklant.components.klantinteracties.api.viewsets.internetaken import (
    InterneTaakViewSet,
)
from openklant.components.klantinteracties.api.viewsets.klantcontacten import (
    ActorKlantcontactViewSet,
    BetrokkeneViewSet,
    BijlageViewSet,
    KlantContactBetrokkeneOnderwerpObjectViewSet,
    KlantcontactViewSet,
    OnderwerpobjectViewSet,
)
from openklant.components.klantinteracties.api.viewsets.partijen import (
    CategorieRelatieViewSet,
    CategorieViewSet,
    PartijIdentificatorViewSet,
    PartijViewSet,
    VertegenwoordigdenViewSet,
)
from openklant.components.klantinteracties.api.viewsets.rekeningnummers import (
    RekeningnummerViewSet,
)

from .schema import custom_settings

app_name = "klantinteracties"

router = routers.DefaultRouter()
router.register("actoren", ActorViewSet)

router.register("digitaleadressen", DigitaalAdresViewSet)

router.register("rekeningnummers", RekeningnummerViewSet)

router.register("actorklantcontacten", ActorKlantcontactViewSet)
router.register("klantcontacten", KlantcontactViewSet)
router.register("betrokkenen", BetrokkeneViewSet)
router.register("onderwerpobjecten", OnderwerpobjectViewSet)
router.register("bijlagen", BijlageViewSet)
router.register(
    "klantcontact-convenience",
    KlantContactBetrokkeneOnderwerpObjectViewSet,
    basename="klantcontact-convenience",
)

router.register("internetaken", InterneTaakViewSet)

router.register("categorieen", CategorieViewSet)
router.register("categorie-relaties", CategorieRelatieViewSet)
router.register("partijen", PartijViewSet)
router.register("partij-identificatoren", PartijIdentificatorViewSet)
router.register("vertegenwoordigingen", VertegenwoordigdenViewSet)

urlpatterns = [
    re_path(
        r"^v(?P<version>\d+)/",
        include(
            [
                re_path(r"^", include(router.urls)),
                path(
                    "", router.APIRootView.as_view(), name="api-root-klantinteracties"
                ),
                path(
                    "schema/openapi.json",
                    SpectacularJSONAPIView.as_view(
                        urlconf="openklant.components.klantinteracties.api.urls",
                        custom_settings=custom_settings,
                    ),
                    name="schema-json-klantinteracties",
                ),
                path(
                    "schema/openapi.yaml",
                    SpectacularYAMLAPIView.as_view(
                        urlconf="openklant.components.klantinteracties.api.urls",
                        custom_settings=custom_settings,
                    ),
                    name="schema-yaml-klantinteracties",
                ),
                path(
                    "schema/",
                    SpectacularRedocView.as_view(
                        url_name="klantinteracties:schema-yaml-klantinteracties"
                    ),
                    name="schema-redoc-klantinteracties",
                ),
            ]
        ),
    ),
]
