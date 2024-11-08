from django.contrib import admin

from ..models.digitaal_adres import BetrokkeneAdres
from .digitaal_adres import BaseAdresAdminForm


class BetrokkeneAdresAdminForm(BaseAdresAdminForm):
    class Meta:
        model = BetrokkeneAdres
        fields = "__all__"


@admin.register(BetrokkeneAdres)
class BetrokkeneAdresAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    search_fields = ("adres",)
    autocomplete_fields = ("betrokkene",)
    form = BetrokkeneAdresAdminForm
