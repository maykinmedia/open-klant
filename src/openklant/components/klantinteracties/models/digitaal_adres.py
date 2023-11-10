import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from openklant.components.klantinteracties.models.klantcontacten import Betrokkene


class DigitaalAdres(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van het digitaal adres."),
    )
    betrokkene = models.ForeignKey(
        Betrokkene,
        on_delete=models.CASCADE,
        verbose_name=_("betrokkene"),
        help_text=_("'Digitaal Adres' had 'Betrokkene bij klantcontact'"),
        null=True,
    )
    soort_digitaal_adres = models.CharField(
        _("soort digitaal adres"),
        help_text=_(
            "Typering van het digitale adres die aangeeft via welk(e) kanaal of kanalen "
            "met dit adres contact kan worden opgenomen."
        ),
        max_length=255,
    )
    adres = models.CharField(
        _("adres"),
        help_text=_(
            "Digitaal adres waarmee een persoon of organisatie bereikt kan worden."
        ),
        max_length=80,
    )
    omschrijving = models.CharField(
        _("omschrijving"),
        help_text=_("Omschrijving van het digitaal adres."),
        max_length=40,
    )

    class Meta:
        verbose_name = _("digitaal adres")

    def __str__(self):
        return self.adres
