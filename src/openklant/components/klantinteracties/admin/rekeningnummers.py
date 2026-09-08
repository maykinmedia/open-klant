from django.contrib import admin

from ..models.rekeningnummers import Rekeningnummer


@admin.register(Rekeningnummer)
class RekeningnummerAdmin(admin.ModelAdmin):
    list_display = ("iban", "bic", "partij")
    search_fields = (
        "uuid",
        "iban",
        "bic",
    )
    autocomplete_fields = ("partij",)
    readonly_fields = ("uuid",)
