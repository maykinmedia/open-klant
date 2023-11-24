from django.utils.translation import gettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class GeslachtChoices(DjangoChoices):
    man = ChoiceItem("m", _("Man"))
    vrouw = ChoiceItem("v", _("Vrouw"))
    overig = ChoiceItem("o", _("Overig"))


class RelationChocies(DjangoChoices):
    local = ChoiceItem("local", _("Local"))
    remote = ChoiceItem("remote", _("Remote"))
