from django.contrib import admin

from ..models.internetaken import InterneTaak


class InterneTaakInlineAdmin(admin.StackedInline):
    model = InterneTaak
    extra = 0
    autocomplete_fields = ("klantcontact",)
