from django.db import models
from django.utils.translation import gettext_lazy as _


class Land(models.Model):
    """Alle huidige en voormalige landen met hun codes, namen en geldigheidsinformatie."""

    landcode = models.CharField(
        _("landcode"),
        help_text=_(
            "Unieke technische identificerende code, primair bedoeld voor gebruik bij "
            "interacties tussen IT-systemen."
        ),
        max_length=40,
        null=False,
        blank=False,
        unique=True,
    )
    landnaam = models.CharField(
        _("landnaam"),
        help_text=_("Kort (80 karakters) tekstveld voor een naam."),
        max_length=80,
        null=False,
        blank=False,
    )
    ingangsdatum_land = models.DateField(
        _("ingangsdatum land"),
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst significante "
            "onderdeel. Een voorbeeld: 2022-02-21 representeert 21 februari 2022."
        ),
        null=False,
        blank=False,
    )

    einddatum_land = models.DateField(
        _("einddatum land"),
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst significante "
            "onderdeel. Een voorbeeld: 2022-02-21 representeert 21 februari 2022."
        ),
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("land")
        verbose_name_plural = _("landen")
        constraints = [
            models.CheckConstraint(
                name="eind_gte_ingang",
                check=models.Q(einddatum_land__gte=models.F("ingangsdatum_land")),
            )
        ]
