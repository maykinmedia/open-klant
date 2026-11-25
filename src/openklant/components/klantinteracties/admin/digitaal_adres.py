from django import forms
from django.contrib import admin

from ..api.validators import SoortDigitaalAdresValidator
from ..constants import SoortDigitaalAdres
from ..models.digitaal_adres import DigitaalAdres


class DigitaalAdresAdminForm(forms.ModelForm):
    class Meta:
        model = DigitaalAdres
        fields = "__all__"

    def clean_adres(self) -> str:
        adres = self.cleaned_data["adres"]
        soort = self.cleaned_data.get("soort_digitaal_adres")
        if soort:
            SoortDigitaalAdresValidator()(SoortDigitaalAdres(soort), adres)
        return adres


@admin.register(DigitaalAdres)
class DigitaalAdresAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    search_fields = (
        "adres",
        "uuid",
    )
    autocomplete_fields = ("partij",)
    raw_id_fields = ("betrokkene",)
    form = DigitaalAdresAdminForm
