from django.utils.translation import gettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class InitiatiefNemer(DjangoChoices):
    gemeente = ChoiceItem("gemeente", _("gemeente"))
    klant = ChoiceItem("klant", _("klant"))


class ObjectTypes(DjangoChoices):
    zaak = ChoiceItem("zaak", _("Zaak"))


class Rol(DjangoChoices):
    belanghebbende = ChoiceItem("belanghebbende",  _("Belanghebbende"))
    gesprekspartner = ChoiceItem("gesprekspartner",  _("Gesprekspartner"))


class Status(DjangoChoices):
    nieuw = ChoiceItem("nieuw",  _("Nieuw"))
    in_behandeling = ChoiceItem("in_behandeling",  _("In behandeling"))
    afgehandeld = ChoiceItem("afgehandeld",  _("Afgehandeld"))
