from django.contrib import admin

from ..models.internetaken import InterneTaak


class InterneTaakInlineAdmin(admin.StackedInline):
    model = InterneTaak
    extra = 0
    autocomplete_fields = ("klantcontact",)


@admin.register(InterneTaak)
class InterneTaakAdmin(admin.ModelAdmin):
    list_display = (
        "nummer",
        "status",
        "toegewezen_op",
    )
    list_filter = (
        "actor",
        "status",
    )
    readonly_fields = ("toegewezen_op",)
