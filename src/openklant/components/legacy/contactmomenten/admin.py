from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models.contactmomenten import (
    ContactMoment,
    KlantContactMoment,
    Medewerker,
    ObjectContactMoment,
)


@admin.register(ContactMoment)
class ContactMomentAdmin(DynamicArrayMixin, admin.ModelAdmin):
    list_display = ["kanaal"]


@admin.register(ObjectContactMoment)
class ObjectContactMomentAdmin(admin.ModelAdmin):
    list_display = ["contactmoment", "object"]


@admin.register(Medewerker)
class MedewerkerAdmin(admin.ModelAdmin):
    list_display = ["contactmoment", "identificatie"]


@admin.register(KlantContactMoment)
class KlantContactMomentAdmin(admin.ModelAdmin):
    list_display = ["klant", "contactmoment"]
