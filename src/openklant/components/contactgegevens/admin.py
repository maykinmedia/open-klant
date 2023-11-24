from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from openklant.components.contactgegevens.constants import RelationChocies
from openklant.components.contactgegevens.models import (
    Contactgegevens,
    Organisatie,
    Persoon,
)


class PersoonInlineAdmin(admin.StackedInline):
    model = Persoon
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


class OrganisatieInlineAdmin(admin.StackedInline):
    model = Organisatie
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


class RelationFilter(admin.SimpleListFilter):
    title = _("Relation location")
    parameter_name = "relation"

    def lookups(self, request, model_admin):
        return RelationChocies.choices

    def queryset(self, request, queryset):
        match (self.value()):
            case RelationChocies.local:
                return queryset.filter(_relation_url__exact="", _relation__isnull=False)
            case RelationChocies.remote:
                return queryset.filter(_relation__isnull=True).exclude(
                    _relation_url__exact=""
                )


@admin.register(Contactgegevens)
class ContactgegevensAdmin(admin.ModelAdmin):
    list_display = ("id", "relation_indicator")
    inlines = (OrganisatieInlineAdmin, PersoonInlineAdmin)
    list_filter = (RelationFilter,)

    @admin.display(empty_value="---")
    def relation_indicator(self, obj):
        if obj._partij_identificator:
            return RelationChocies.local

        if obj._partij_identificator_url:
            return RelationChocies.local

    relation_indicator.short_description = _("Partij Identificator")
