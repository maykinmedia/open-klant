from django.contrib import admin

from ordered_model.admin import OrderedInlineModelAdminMixin

from ..models.internetaken import InterneTaak
from .actoren import ActorThoughTabularInlineAdmin


class InterneTaakInlineAdmin(admin.StackedInline):
    model = InterneTaak
    extra = 0
    autocomplete_fields = ("klantcontact",)
    readonly_fields = ("uuid",)


@admin.register(InterneTaak)
class InterneTaakAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    readonly_fields = ("uuid",)
    list_display = (
        "nummer",
        "status",
        "toegewezen_op",
        "afgehandeld_op",
    )
    list_filter = (
        "actoren",
        "status",
    )
    readonly_fields = (
        "uuid",
        "toegewezen_op",
    )
    inlines = (ActorThoughTabularInlineAdmin,)
