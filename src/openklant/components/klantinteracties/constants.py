from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class SoortDigitaalAdres(TextChoices):
    email = "email", _("Email")
    telefoonnummer = "telefoonnummer", _("Telefoonnummer")
    overig = "overig", _("Overig")
