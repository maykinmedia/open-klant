from django.conf import settings
from django.urls import include, path

from vng_api_common import routers

from . import viewsets

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
        "v<slug:version>/",
        include(
            [
                # TODO API documentation
                # re_path(r"^schema/openapi(?P<format>\.json|\.yaml)$",
                path("", include(router.urls)),
            ]
        ),
    ),
]
