from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from openklant.components.contactgegevens.models import Organisatie, Persoon


@admin.register(Persoon)
class PersoonAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "uuid",
                    "geslacht",
                    "voornamen",
                    "voorvoegsel",
                    "geslachtsnaam",
                    "geboortedatum",
                    "overlijdensdatum",
                    "land",
                ]
            },
        ),
        (
            _("Adres gegevens"),
            {
                "fields": [
                    "adres_straatnaam",
                    "adres_huisnummer",
                    "adres_huisnummertoevoeging",
                    "adres_postcode",
                    "adres_stad",
                    "adres_adresregel1",
                    "adres_adresregel2",
                    "adres_adresregel3",
                    "adres_land",
                ]
            },
        ),
    ]
    extra = 0


@admin.register(Organisatie)
class OrganisatieAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "uuid",
                    "handelsnaam",
                    "oprichtingsdatum",
                    "opheffingsdatum",
                    "land",
                ]
            },
        ),
        (
            _("Adres gegevens"),
            {
                "fields": [
                    "adres_straatnaam",
                    "adres_huisnummer",
                    "adres_huisnummertoevoeging",
                    "adres_postcode",
                    "adres_stad",
                    "adres_adresregel1",
                    "adres_adresregel2",
                    "adres_adresregel3",
                    "adres_land",
                ]
            },
        ),
    ]
    extra = 0
