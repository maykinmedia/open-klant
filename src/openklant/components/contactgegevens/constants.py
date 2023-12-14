from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class GeslachtChoices(TextChoices):
    man = "m", _("Man")
    vrouw = "v", _("Vrouw")
    overig = "o", _("Overig")


class RelationChocies(TextChoices):
    local = "local", _("Local")
    remote = "remote", _("Remote")
