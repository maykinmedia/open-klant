import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .klantcontacten import Betrokkene
from .partijen import Partij


class DigitaalAdres(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        max_length=40,
        help_text=_(
            "Unieke (technische) identificatiecode van de betrokkene bij klantcontact."
        ),
    )
    partij = models.ForeignKey(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("Digitaal adres"),
        related_name="digitale_adressen",
        help_text=_(
            "Het digitale adres dat de partij voor gebruik bij toekomstig contact met de gemeente verstrekte."
        ),
        null=True,
    )
    betrokkene = models.ForeignKey(
        Betrokkene,
        on_delete=models.CASCADE,
        verbose_name=_("Betrokkene bij klantcontact"),
        related_name="digitale_adressen",
        help_text=_(
            "Het digitale adres dat de betrokkene bij klantcontact opgaf voor gebruik bij opvolging van het "
            "klantcontact."
        ),
        null=True,
    )
    soort_digitaal_adres = models.CharField(
        _("Soort digitaal adres"),
        help_text=_(
            "Typering van het digitale adres die aangeeft via welk(e) kanaal of kanalen "
            "met dit adres contact kan worden opgenomen."
        ),
        max_length=254,
        blank=False,
    )
    adres = models.CharField(
        _("Adres"),
        help_text=_(
            "Digitaal adres waarmee een persoon of organisatie bereikt kan worden."
        ),
        max_length=80,
        blank=False,
    )
    omschrijving = models.CharField(
        _("Omschrijving"),
        help_text=_("Omschrijving van het digitaal adres."),
        max_length=40,
        blank=False,
    )

    class Meta:
        verbose_name = "digitaal Adres"

        def __str__(self):
            return self.adres
