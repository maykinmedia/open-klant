from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class InitiatiefNemer(TextChoices):
    gemeente = "gemeente", _("gemeente")
    klant = "klant", _("klant")


class ObjectTypes(TextChoices):
    zaak = "zaak", _("Zaak")


class Rol(TextChoices):
    belanghebbende = "belanghebbende", _("Belanghebbende")
    gesprekspartner = "gesprekspartner", _("Gesprekspartner")
