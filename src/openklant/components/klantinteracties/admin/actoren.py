from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..admin.internezaken import InterneTaakInlineAdmin
from ..models.actoren import (
    Actor,
    GeautomatiseerdeActor,
    Medewerker,
    OrganisatorischeEenheid,
)


class GeautomatiseerdeActorInlineAdmin(admin.StackedInline):
    model = GeautomatiseerdeActor
    fields = ("functie", "omschrijving")
    extra = 0


class MedewerkerInlineAdmin(admin.StackedInline):
    model = Medewerker
    fields = ("functie", "emailadres", "telefoonnummer")
    extra = 0


class OrganisatorischeEenheidInlineAdmin(admin.StackedInline):
    model = OrganisatorischeEenheid
    fields = ("omschrijving", "emailadres", "faxnummer", "telefoonnummer")
    extra = 0


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = (
        "naam",
        "soort_actor",
        "indicatie_actief",
    )
    list_filter = (
        "soort_actor",
        "indicatie_actief",
    )
    search_fields = ("naam",)
    inlines = (
        GeautomatiseerdeActorInlineAdmin,
        MedewerkerInlineAdmin,
        OrganisatorischeEenheidInlineAdmin,
        InterneTaakInlineAdmin,
    )
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "naam",
                    "soort_actor",
                    "indicatie_actief",
                ]
            },
        ),
        (
            _("Objectidentificator velden"),
            {
                "fields": [
                    "objectidentificator_objecttype",
                    "objectidentificator_soort_object_id",
                    "objectidentificator_object_id",
                    "objectidentificator_register",
                ]
            },
        ),
    )
