from django.contrib import admin

from ..models.digitaal_adres import DigitaalAdres


@admin.register(DigitaalAdres)
class DigitaalAdresAdmin(admin.ModelAdmin):
    search_fields = ("adres",)
