from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.constants import SoortPartij
from ..models.partijen import Contactpersoon, Organisatie, Partij, Persoon


class PersoonInlineAdmin(admin.StackedInline):
    model = Persoon
    extra = 0


class ContactpersoonInlineAdmin(admin.StackedInline):
    model = Contactpersoon
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
    inlines = (PersoonInlineAdmin, ContactpersoonInlineAdmin, OrganisatieInlineAdmin)
    autocomplete_fields = (
        "betrokkene",
        "digitaal_adres",
        "voorkeurs_digitaal_adres",
    )
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "betrokkene",
                    "digitaal_adres",
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
        if people := obj.persoon_set.all():
            return [person.get_contactnaam() for person in people]

    def get_contactpersonen(self, obj):
        if people := obj.contactpersoon_set.all():
            return [person.get_contactnaam() for person in people]

    def get_organisaties(self, obj):
        if organisaties := obj.organisatie_set.all():
            return [organisatie.naam for organisatie in organisaties]
