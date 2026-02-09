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


class PartijAdminForm(forms.ModelForm):
    class Meta:
        model = Partij
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        if voorkeurs_digitaal_adres := cleaned_data.get("voorkeurs_digitaal_adres"):
            if not self.instance.pk:
                raise forms.ValidationError(
                    {
                        "voorkeurs_digitaal_adres": [
                            _(
                                "Om de `voorkeurs_digitaal_adres` te selecteren,"
                                " moet je eerst de Partij aanmaken en opslaan."
                            )
                        ]
                    }
                )

            if voorkeurs_digitaal_adres not in self.instance.digitaaladres_set.all():
                raise forms.ValidationError(
                    {
                        "voorkeurs_digitaal_adres": [
                            _(
                                "Het voorkeurs adres moet een gelinkte digitaal adres zijn."
                            )
                        ]
                    }
                )

        if voorkeurs_rekeningnummer := cleaned_data.get("voorkeurs_rekeningnummer"):
            if not self.instance.pk:
                raise forms.ValidationError(
                    {
                        "voorkeurs_rekeningnummer": [
                            _(
                                "Om de `voorkeurs_rekeningnummer` te selecteren,"
                                " moet je eerst de Partij aanmaken en opslaan."
                            )
                        ]
                    }
                )

            if voorkeurs_rekeningnummer not in self.instance.rekeningnummer_set.all():
                raise forms.ValidationError(
                    {
                        "voorkeurs_rekeningnummer": [
                            _(
                                "Het voorkeurs rekeningnummer moet een gelinkte rekeningnummer zijn."
                            )
                        ]
                    }
                )

        return cleaned_data


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
            instance=self.instance if self.instance and self.instance.pk else None,
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
    raw_id_fields = ("sub_identificator_van",)
    extra = 0


class BetrokkeneInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = Betrokkene
    raw_id_fields = ("klantcontact",)
    extra = 0


class DigitaalAdresInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = DigitaalAdres
    raw_id_fields = ("betrokkene",)
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
    raw_id_fields = ("vertegenwoordigde_partij",)


class ContactpersoonInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = Contactpersoon
    fk_name = "partij"
    raw_id_fields = ("werkte_voor_partij",)
    extra = 0


class OrganisatieInlineAdmin(admin.StackedInline):
    model = Organisatie
    extra = 0


@admin.register(Partij)
class PartijAdmin(admin.ModelAdmin):
    form = PartijAdminForm
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
                    "referentienummer",
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
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "voorkeurs_rekeningnummer",
                "voorkeurs_digitaal_adres",
                "organisatie",
                "persoon",
                "contactpersoon",
            )
        )

    @admin.display(empty_value="---")
    def get_name(self, obj):
        match obj.soort_partij:
            case SoortPartij.persoon.value:
                return self.get_personen(obj)
            case SoortPartij.contactpersoon.value:
                return self.get_contactpersonen(obj)
            case SoortPartij.organisatie.value:
                return self.get_organisaties(obj)

    get_name.short_description = _("naam")

    def get_personen(self, obj):
        return obj.persoon.get_full_name() if hasattr(obj, "persoon") else "---"

    def get_contactpersonen(self, obj):
        return (
            obj.contactpersoon.get_full_name()
            if hasattr(obj, "contactpersoon")
            else "---"
        )

    def get_organisaties(self, obj):
        return obj.organisatie.naam if hasattr(obj, "organisatie") else "---"


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    search_fields = ("naam",)
    fields = (
        "uuid",
        "naam",
    )


@admin.register(PartijIdentificator)
class PartijIdentificatorAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    search_fields = (
        "uuid",
        "partij__uuid",
        "partij_identificator_object_id",
        "sub_identificator_van__uuid",
        "sub_identificator_van__partij_identificator_object_id",
    )
    list_filter = (
        "partij_identificator_code_objecttype",
        "partij_identificator_code_soort_object_id",
        "partij_identificator_code_register",
    )
    fields = (
        "uuid",
        "partij",
        "sub_identificator_van",
        "andere_partij_identificator",
        "partij_identificator_code_objecttype",
        "partij_identificator_code_soort_object_id",
        "partij_identificator_object_id",
        "partij_identificator_code_register",
    )
    raw_id_fields = ("partij",)
