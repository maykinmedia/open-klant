from django.contrib import admin

from .models import (
    Klant,
    KlantAdres,
    NatuurlijkPersoon,
    SubVerblijfBuitenland,
    VerblijfsAdres,
    Vestiging,
)


@admin.register(Klant)
class KlantAdmin(admin.ModelAdmin):
    list_display = ["bronorganisatie", "klantnummer"]


@admin.register(NatuurlijkPersoon)
class NatuurlijkPersoonAdmin(admin.ModelAdmin):
    list_display = ["klant", "inp_bsn", "anp_identificatie", "inp_a_nummer"]


@admin.register(Vestiging)
class VestigingAdmin(admin.ModelAdmin):
    list_display = ["klant", "vestigings_nummer"]


@admin.register(SubVerblijfBuitenland)
class SubVerblijfBuitenlandAdmin(admin.ModelAdmin):
    list_display = ["natuurlijkpersoon", "vestiging", "lnd_landcode"]


@admin.register(VerblijfsAdres)
class VerblijfsAdresAdmin(admin.ModelAdmin):
    list_display = ["natuurlijkpersoon", "vestiging", "aoa_identificatie"]


@admin.register(KlantAdres)
class KlanAdresAdmin(admin.ModelAdmin):
    list_display = ["klant", "straatnaam", "huisnummer"]
