from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.constants import SoortPartij
from ..models.digitaal_adres import DigitaalAdres
from ..models.klantcontacten import Betrokkene
from ..models.partijen import Categorie, Contactpersoon, Organisatie, Partij, Persoon


class CategorieInlineAdmin(admin.StackedInline):
    model = Categorie
    extra = 0


class BetrokkeneInlineAdmin(admin.StackedInline):
    model = Betrokkene
    extra = 0


class DigitaalAdresInlineAdmin(admin.StackedInline):
    model = DigitaalAdres
    extra = 0


class PersoonInlineAdmin(admin.StackedInline):
    model = Persoon
    extra = 0


class ContactpersoonInlineAdmin(admin.StackedInline):
    model = Contactpersoon
    fk_name = "partij"
    raw_id_field = ["partij"]
    extra = 0


class OrganisatieInlineAdmin(admin.StackedInline):
    model = Organisatie
    extra = 0


@admin.register(Partij)
class PartijAdmin(admin.ModelAdmin):
    list_display = (
        "nummer",
        "get_name",
        "soort_partij",
        "indicatie_actief",
    )
    list_filter = (
        "soort_partij",
        "indicatie_actief",
    )
    inlines = (
        PersoonInlineAdmin,
        CategorieInlineAdmin,
        ContactpersoonInlineAdmin,
        OrganisatieInlineAdmin,
        DigitaalAdresInlineAdmin,
        BetrokkeneInlineAdmin,
    )
    search_fields = ("partij",)
    autocomplete_fields = ("voorkeurs_digitaal_adres",)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "voorkeurs_digitaal_adres",
                    "vertegenwoordigde",
                    "nummer",
                    "interne_notitie",
                    "soort_partij",
                    "indicatie_geheimhouding",
                    "voorkeurstaal",
                    "indicatie_actief",
                ]
            },
        ),
        (
            _("Bezoekadres velden"),
            {
                "fields": [
                    "bezoekadres_nummeraanduiding_id",
                    "bezoekadres_adresregel1",
                    "bezoekadres_adresregel2",
                    "bezoekadres_adresregel3",
                    "bezoekadres_land",
                ]
            },
        ),
        (
            _("Correspondentieadres velden"),
            {
                "fields": [
                    "correspondentieadres_nummeraanduiding_id",
                    "correspondentieadres_adresregel1",
                    "correspondentieadres_adresregel2",
                    "correspondentieadres_adresregel3",
                    "correspondentieadres_land",
                ]
            },
        ),
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "voorkeurs_digitaal_adres",
            )
        )

    @admin.display(empty_value="---")
    def get_name(self, obj):
        match obj.soort_partij:
            case SoortPartij.persoon:
                return self.get_personen(obj)
            case SoortPartij.contactpersoon:
                return self.get_contactpersonen(obj)
            case SoortPartij.organisatie:
                return self.get_organisaties(obj)

    get_name.short_description = _("naam")

    def get_personen(self, obj):
        if persoon := obj.persoon:
            return persoon.get_full_name()

    def get_contactpersonen(self, obj):
        if contactpersoon := obj.contactpersoon:
            return contactpersoon.get_full_name()

    def get_organisaties(self, obj):
        if organisatie := obj.organisatie:
            return organisatie.naam
