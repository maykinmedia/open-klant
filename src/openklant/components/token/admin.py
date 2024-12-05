from django.contrib import admin

from .models import TokenAuth


@admin.register(TokenAuth)
class TokenAuthAdmin(admin.ModelAdmin):
    list_display = (
        "identifier",
        "contact_person",
        "organization",
        "administration",
        "application",
    )
    readonly_fields = ("token",)
