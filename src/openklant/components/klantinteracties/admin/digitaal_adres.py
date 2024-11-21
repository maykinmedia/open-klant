from django import forms
from django.contrib import admin

from ..api.validators import SoortDigitaalAdresValidator
from ..models.digitaal_adres import DigitaalAdres


class DigitaalAdresAdminForm(forms.ModelForm):
    class Meta:
        model = DigitaalAdres
        fields = "__all__"

    def clean_adres(self):
        data = self.cleaned_data
        SoortDigitaalAdresValidator()(
            soort_digitaal_adres=data.get("soort_digitaal_adres"), value=data["adres"]
        )
        return data["adres"]


@admin.register(DigitaalAdres)
class DigitaalAdresAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    search_fields = ("adres",)
    autocomplete_fields = ("partij",)
    form = DigitaalAdresAdminForm
