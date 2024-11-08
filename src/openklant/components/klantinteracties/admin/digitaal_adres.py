from django import forms
from django.contrib import admin

from ..api.validators import OptionalEmailValidator
from ..models.digitaal_adres import DigitaalAdres


class BaseAdresAdminForm(forms.ModelForm):
    class Meta:
        fields = "__all__"

    def clean_adres(self):
        data = self.cleaned_data
        OptionalEmailValidator()(data["adres"], data.get("soort_digitaal_adres"))
        return data["adres"]


class DigitaalAdresAdminForm(BaseAdresAdminForm):
    class Meta:
        model = DigitaalAdres
        fields = "__all__"


@admin.register(DigitaalAdres)
class DigitaalAdresAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    search_fields = ("adres",)
    autocomplete_fields = ("partij",)
    form = DigitaalAdresAdminForm
