from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from openklant.components.klantinteracties.models.actoren import ActorKlantcontact

from ..models.klantcontacten import Betrokkene, Bijlage, Klantcontact, Onderwerpobject
from .internetaken import InterneTaakInlineAdmin


class BetrokkeneInlineAdmin(admin.StackedInline):
    model = Betrokkene
    search_fields = (
        "contactnaam_voorletters",
        "contactnaam_voorvoegsel_achternaam",
        "contactnaam_achternaam",
    )
    autocomplete_fields = ("partij",)
    readonly_fields = ("uuid",)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "uuid",
                    "partij",
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
                    "bezoekadres_straatnaam",
                    "bezoekadres_huisnummer",
                    "bezoekadres_huisnummertoevoeging",
                    "bezoekadres_postcode",
                    "bezoekadres_stad",
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
                    "correspondentieadres_straatnaam",
                    "correspondentieadres_huisnummer",
                    "correspondentieadres_huisnummertoevoeging",
                    "correspondentieadres_postcode",
                    "correspondentieadres_stad",
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
        "uuid",
        "contactnaam_voorletters",
        "contactnaam_voorvoegsel_achternaam",
        "contactnaam_achternaam",
    )
    autocomplete_fields = ("partij",)
    readonly_fields = ("uuid",)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "uuid",
                    "partij",
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
                    "bezoekadres_straatnaam",
                    "bezoekadres_huisnummer",
                    "bezoekadres_huisnummertoevoeging",
                    "bezoekadres_postcode",
                    "bezoekadres_stad",
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
                    "correspondentieadres_straatnaam",
                    "correspondentieadres_huisnummer",
                    "correspondentieadres_huisnummertoevoeging",
                    "correspondentieadres_postcode",
                    "correspondentieadres_stad",
                    "correspondentieadres_adresregel1",
                    "correspondentieadres_adresregel2",
                    "correspondentieadres_adresregel3",
                    "correspondentieadres_land",
                ]
            },
        ),
    ]


class OnderwerpobjectInlineAdmin(admin.StackedInline):
    model = Onderwerpobject
    fk_name = "klantcontact"
    raw_id_fields = ("was_klantcontact",)
    readonly_fields = ("uuid",)
    extra = 0


class BijlageInlineAdmin(admin.StackedInline):
    model = Bijlage
    extra = 0
    readonly_fields = ("uuid",)


class ActorKlantcontactInlineAdmin(admin.StackedInline):
    model = ActorKlantcontact
    extra = 0
    readonly_fields = ("uuid",)
    raw_id_fields = ("actor",)


@admin.register(Klantcontact)
class KlantcontactAdmin(admin.ModelAdmin):
    list_display = ["nummer", "kanaal", "indicatie_contact_gelukt", "betrokkene_namen"]
    list_filter = [
        "indicatie_contact_gelukt",
    ]
    inlines = [
        ActorKlantcontactInlineAdmin,
        BetrokkeneInlineAdmin,
        OnderwerpobjectInlineAdmin,
        BijlageInlineAdmin,
        InterneTaakInlineAdmin,
    ]
    search_fields = (
        "nummer",
        "uuid",
    )
    date_hierarchy = "plaatsgevonden_op"
    readonly_fields = ("uuid",)

    @admin.display(empty_value="---")
    def betrokkene_namen(self, obj):
        if betrokkene := obj.betrokkene_set.all():
            return [person.get_full_name() for person in betrokkene]

    betrokkene_namen.short_description = _("betrokkene namen")
