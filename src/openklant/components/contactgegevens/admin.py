from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from openklant.components.contactgegevens.models import Organisatie, Persoon


@admin.register(Persoon)
class PersoonAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "contactgegevens",
                    "geboortedatum",
                    "overlijdensdatum",
                ]
            },
        ),
        (
            _("Persoon gegevens"),
            {
                "fields": [
                    "geslacht",
                    "voornamen",
                    "voorvoegsel",
                    "geslachtsnaam",
                ]
            },
        ),
        (
            _("Adres gegevens"),
            {
                "fields": [
                    "adres_adresregel1",
                    "adres_adresregel2",
                    "adres_adresregel3",
                    "adres_land",
                ]
            },
        ),
        (
            _("Land gegevens"),
            {
                "fields": [
                    "land_code",
                ]
            },
        ),
    ]
    extra = 0


@admin.register(Organisatie)
class OrganisatieAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "contactgegevens",
                    "handelsnaam",
                    "oprichtingsdatum",
                    "opheffingsdatum",
                ]
            },
        ),
        (
            _("Adres gegevens"),
            {
                "fields": [
                    "adres_adresregel1",
                    "adres_adresregel2",
                    "adres_adresregel3",
                    "adres_land",
                ]
            },
        ),
        (
            _("Land gegevens"),
            {
                "fields": [
                    "land_code",
                ]
            },
        ),
    ]
    extra = 0
