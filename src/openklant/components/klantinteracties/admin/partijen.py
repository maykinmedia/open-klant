from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from openklant.components.klantinteracties.models.rekeningnummers import Rekeningnummer
from openklant.components.klantinteracties.models.validators import (
    PartijIdentificatorTypesValidator,
    PartijIdentificatorUniquenessValidator,
)

from ..models.constants import SoortPartij
from ..models.digitaal_adres import DigitaalAdres
from ..models.klantcontacten import Betrokkene
from ..models.partijen import (
    Categorie,
    CategorieRelatie,
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
    Persoon,
    Vertegenwoordigden,
)


class PartijIdentificatorAdminForm(forms.ModelForm):
    class Meta:
        model = PartijIdentificator
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        PartijIdentificatorTypesValidator()(
            code_register=cleaned_data["partij_identificator_code_register"],
            code_objecttype=cleaned_data["partij_identificator_code_objecttype"],
            code_soort_object_id=cleaned_data[
                "partij_identificator_code_soort_object_id"
            ],
            object_id=cleaned_data["partij_identificator_object_id"],
        )

        PartijIdentificatorUniquenessValidator(
            code_soort_object_id=cleaned_data[
                "partij_identificator_code_soort_object_id"
            ],
            sub_identificator_van=cleaned_data["sub_identificator_van"],
        )()

        return cleaned_data


class CategorieRelatieInlineAdmin(admin.StackedInline):
    model = CategorieRelatie
    readonly_fields = ("uuid",)
    autocomplete_fields = ("categorie",)
    fields = (
        "uuid",
        "categorie",
        "begin_datum",
        "eind_datum",
    )
    extra = 0


class PartijIdentificatorInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = PartijIdentificator
    form = PartijIdentificatorAdminForm
    extra = 0


class BetrokkeneInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = Betrokkene
    extra = 0


class DigitaalAdresInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = DigitaalAdres
    extra = 0


class RekeningnummerInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = Rekeningnummer
    extra = 0


class PersoonInlineAdmin(admin.StackedInline):
    model = Persoon
    extra = 0


class VertegenwoordigdenInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = Vertegenwoordigden
    fk_name = "vertegenwoordigende_partij"
    extra = 0


class ContactpersoonInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
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
        CategorieRelatieInlineAdmin,
        ContactpersoonInlineAdmin,
        OrganisatieInlineAdmin,
        DigitaalAdresInlineAdmin,
        RekeningnummerInlineAdmin,
        BetrokkeneInlineAdmin,
        VertegenwoordigdenInlineAdmin,
        PartijIdentificatorInlineAdmin,
    )
    search_fields = ("nummer", "uuid", "voorkeurs_digitaal_adres__adres")
    autocomplete_fields = ("voorkeurs_digitaal_adres",)
    readonly_fields = ("uuid",)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "uuid",
                    "voorkeurs_digitaal_adres",
                    "voorkeurs_rekeningnummer",
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


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    search_fields = ("naam",)
    fields = (
        "uuid",
        "naam",
    )
