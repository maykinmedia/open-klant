from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractIndicatieActiefModel(models.Model):
    "Objecten met indicateActief"

    code = models.CharField(
        _("code"),
        help_text=_(
            "Unieke technische identificerende code, primair bedoeld voor gebruik bij interacties tussen IT-systemen."
        ),
        max_length=40,
        null=False,
        blank=False,
        unique=True,
    )
    indicatie_actief = models.BooleanField(
        _("indicatie actief"),
        help_text=_("Indicatie voor een waarde `Ja` of een waarde `Nee`."),
        null=False,
        blank=False,
    )
    naam = models.CharField(
        _("naam"),
        help_text=_("Kort (80 karakters) tekstveld voor een naam."),
        max_length=80,
        null=False,
        blank=False,
    )

    class Meta:
        abstract = True
