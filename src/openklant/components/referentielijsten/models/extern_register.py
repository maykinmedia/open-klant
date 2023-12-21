from django.db import models
from django.utils.translation import gettext_lazy as _


class ExternRegister(models.Model):
    """
    Registers buiten het domein van klantinteracties
    waarin objecten zijn geregistreerd die binnen het domein van klantinteracties een rol (kunnen) spelen.
    """

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
    locatie = models.CharField(
        _("locatie"),
        help_text=_("Kort (40 karakters) tekstveld voor een omschrijving."),
        max_length=40,
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
        verbose_name = _("extern register")
        verbose_name_plural = _("externe registers")
