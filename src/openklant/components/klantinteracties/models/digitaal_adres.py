import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models.klantcontacten import Betrokkene
from openklant.components.klantinteracties.models.partijen import Partij
from openklant.components.utils.mixins import APIMixin


class DigitaalAdres(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van het digitaal adres."),
    )
    partij = models.ForeignKey(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
        help_text=_("'Digitaal Adres' was 'Partij'"),
        null=True,
        blank=True,
    )
    betrokkene = models.ForeignKey(
        Betrokkene,
        on_delete=models.CASCADE,
        verbose_name=_("betrokkene"),
        help_text=_("'Digitaal Adres' had 'Betrokkene bij klantcontact'"),
        blank=True,
        null=True,
    )
    soort_digitaal_adres = models.CharField(
        _("soort digitaal adres"),
        help_text=_(
            "Typering van het digitale adres die aangeeft via welk(e) kanaal of kanalen "
            "met dit adres contact kan worden opgenomen."
        ),
        max_length=255,
        choices=SoortDigitaalAdres.choices,
    )
    is_standaard_adres = models.BooleanField(
        _("Is standaard adres"),
        help_text=_(
            "Geeft aan of dit digitaal adres het standaard adres is voor het `soortDigitaalAdres`"
        ),
        default=False,
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
        blank=True,
    )
    referentie = models.SlugField(
        _("referentie"),
        help_text=_(
            "Machine-leesbare tag voor unieke identificatie van het digitaal adres."
        ),
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("digitaal adres")
        constraints = [
            models.UniqueConstraint(
                fields=["partij", "soort_digitaal_adres"],
                condition=models.Q(is_standaard_adres=True),
                name="unique_default_per_partij_and_soort",
            ),
            models.UniqueConstraint(
                fields=["partij", "referentie"],
                name="unique_referentie_per_parij",
                condition=models.Q(partij__isnull=False),
            ),
        ]

    def __str__(self):
        return f"{self.betrokkene} - {self.adres}"

    def save(self, *args, **kwargs):
        if self.is_standaard_adres:
            # Because there can only be one default address per `soort_digitaal_adres`
            # and `partij`, mark all other addresses as non-default
            DigitaalAdres.objects.filter(
                soort_digitaal_adres=self.soort_digitaal_adres,
                partij=self.partij,
                is_standaard_adres=True,
            ).update(is_standaard_adres=False)

        super().save(*args, **kwargs)
