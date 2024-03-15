from django.contrib import admin

from ..models.digitaal_adres import DigitaalAdres


@admin.register(DigitaalAdres)
class DigitaalAdresAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    search_fields = ("adres",)
    autocomplete_fields = ("partij",)
