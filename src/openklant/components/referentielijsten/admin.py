import datetime

from django.contrib import admin

from . import models


@admin.register(models.ExternRegister)
class ExternRegisterAdmin(admin.ModelAdmin):
    list_display = ["code", "naam"]


@admin.register(models.Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ["landcode", "landnaam", "indicatie_actief"]

    @admin.display(boolean=True)
    def indicatie_actief(self, land: models.Land) -> bool:
        return land.ingangsdatum_land <= datetime.date.today() < land.einddatum_land


class CommonAdmin(admin.ModelAdmin):
    list_display = ["code", "naam", "indicatie_actief"]
    list_filter = ["indicatie_actief"]


admin.site.register(
    [
        models.Kanaal,
        models.SoortDigitaalAdres,
        models.SoortObject,
        models.SoortObjectid,
        models.Taal,
    ],
    CommonAdmin,
)
