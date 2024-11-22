from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.actoren import (
    Actor,
    ActorKlantcontact,
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


class ActorKlantcontactInlineAdmin(admin.StackedInline):
    readonly_fields = ("uuid",)
    model = ActorKlantcontact
    extra = 0


class InterneTaakInlineAdmin(admin.StackedInline):
    model = Actor.internetaak_set.through
    raw_id_fields = ("internetaak",)
    verbose_name = _("Interne taak")
    verbose_name_plural = _("Interne taken")
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
        ActorKlantcontactInlineAdmin,
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
            _("Actoridentificator velden"),
            {
                "fields": [
                    "actoridentificator_code_objecttype",
                    "actoridentificator_code_soort_object_id",
                    "actoridentificator_object_id",
                    "actoridentificator_code_register",
                ]
            },
        ),
    )
