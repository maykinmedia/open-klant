from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..admin.internezaken import InterneTaakInlineAdmin
from ..models.actoren import Actor


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = [
        "naam",
        "soort_actor",
        "indicatie_actief",
    ]
    list_filter = [
        "soort_actor",
        "indicatie_actief",
    ]
    search_fields = ("naam",)
    inlines = [InterneTaakInlineAdmin]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "naam",
                    "soort_actor",
                    "indicatie_actief",
                ]
            },
        ),
        (
            _("Objectidentificator velden"),
            {
                "fields": [
                    "objectidentificator_objecttype",
                    "objectidentificator_soort_object_id",
                    "objectidentificator_object_id",
                    "objectidentificator_register",
                ]
            },
        ),
    ]
