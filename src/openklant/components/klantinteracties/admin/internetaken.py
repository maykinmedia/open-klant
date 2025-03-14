from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.internetaken import InterneTaak


class InterneTaakInlineAdmin(admin.StackedInline):
    model = InterneTaak
    extra = 0
    autocomplete_fields = ("klantcontact",)
    readonly_fields = ("uuid",)


class ActorInlineAdmin(admin.StackedInline):
    model = InterneTaak.actoren.through
    raw_id_fields = ("actor",)
    verbose_name = _("Actor")
    verbose_name_plural = _("Actoren")
    extra = 0


@admin.register(InterneTaak)
class InterneTaakAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    fields = (
        "uuid",
        "klantcontact",
        "nummer",
        "gevraagde_handeling",
        "toelichting",
        "status",
        "toegewezen_op",
        "afgehandeld_op",
    )
    list_display = (
        "nummer",
        "status",
        "toegewezen_op",
        "afgehandeld_op",
    )
    search_fields = (
        "nummer",
        "uuid",
    )
    list_filter = (
        "actoren",
        "status",
    )
    readonly_fields = (
        "uuid",
        "toegewezen_op",
    )
    inlines = (ActorInlineAdmin,)
