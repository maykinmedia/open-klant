from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..admin.internezaken import InterneTaakInlineAdmin
from ..models.klantcontacten import Betrokkene, Bijlage, Klantcontact, Onderwerpobject


class BetrokkeneInlineAdmin(admin.StackedInline):
    model = Betrokkene
    search_fields = (
        "contactnaam_voorletters",
        "contactnaam_voorvoegsel_achternaam",
        "contactnaam_achternaam",
    )
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "klantcontact",
                    "rol",
                    "organisatienaam",
                    "initiator",
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
        (
            _("Contactnaam velden"),
            {
                "fields": [
                    "contactnaam_voorletters",
                    "contactnaam_voornaam",
                    "contactnaam_voorvoegsel_achternaam",
                    "contactnaam_achternaam",
                ]
            },
        ),
    ]
    extra = 0


@admin.register(Betrokkene)
class BetrokkeneAdmin(admin.ModelAdmin):
    search_fields = (
        "contactnaam_voorletters",
        "contactnaam_voorvoegsel_achternaam",
        "contactnaam_achternaam",
    )
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "klantcontact",
                    "rol",
                    "organisatienaam",
                    "initiator",
                ]
            },
        ),
        (
            _("Persoonsgegevens"),
            {
                "fields": [
                    "contactnaam_voorletters",
                    "contactnaam_voornaam",
                    "contactnaam_voorvoegsel_achternaam",
                    "contactnaam_achternaam",
                ]
            },
        ),
        (
            _("Bezoekadres"),
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
            _("Correspondentieadres"),
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


class WasOnderwerpobjectInlineAdmin(admin.StackedInline):
    model = Onderwerpobject
    fk_name = "was_klantcontact"
    raw_id_field = ["was_klantcontact"]
    extra = 0


class BijlageInlineAdmin(admin.StackedInline):
    model = Bijlage
    extra = 0


@admin.register(Klantcontact)
class KlantcontactAdmin(admin.ModelAdmin):
    list_display = ["nummer", "kanaal", "indicatie_contact_gelukt", "betrokkene_namen"]
    list_filter = [
        "indicatie_contact_gelukt",
    ]
    inlines = [
        BetrokkeneInlineAdmin,
        WasOnderwerpobjectInlineAdmin,
        BijlageInlineAdmin,
        InterneTaakInlineAdmin,
    ]
    search_fields = ("nummer",)
    autocomplete_fields = ["actoren"]
    date_hierarchy = "plaatsgevonden_op"

    @admin.display(empty_value="---")
    def betrokkene_namen(self, obj):
        if betrokkene := obj.betrokkene_set.all():
            return [person.get_contactnaam() for person in betrokkene]

    betrokkene_namen.short_description = _("betrokkene namen")
