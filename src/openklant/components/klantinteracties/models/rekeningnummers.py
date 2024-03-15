import uuid

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from openklant.utils.validators import validate_iban, validate_no_space


class Rekeningnummer(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de interne taak."),
    )
    partij = models.ForeignKey(
        "klantinteracties.Partij",
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
        help_text=_("'Rekeninnummer' van 'Partij'"),
        null=True,
        blank=True,
    )
    iban = models.CharField(
        _("IBAN"),
        help_text=_(
            "Het internationaal bankrekeningnummer, zoals dat door een bankinstelling als "
            "identificator aan een overeenkomst tussen de bank en een of meer subjecten wordt "
            "toegekend, op basis waarvan het SUBJECT in de regel internationaal financieel communiceert."
        ),
        max_length=34,
        validators=[validate_iban],
        blank=False,
    )
    bic = models.CharField(
        _("BIC"),
        help_text=_(
            "De unieke code van de bankinstelling waar het SUBJECT het bankrekeningnummer "
            "heeft waarmee het subject in de regel internationaal financieel communiceert."
        ),
        max_length=11,
        validators=[MinLengthValidator(8), validate_no_space],
        blank=True,
    )

    class Meta:
        verbose_name = _("rekeningnummer")
        verbose_name_plural = _("rekeningnummers")

    def __str__(self):
        return f"{self.partij} - ({self.bic} - {self.iban})"
