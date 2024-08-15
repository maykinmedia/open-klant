import uuid

from django.core.validators import validate_integer
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ordered_model.models import OrderedModel

from openklant.components.utils.number_generator import number_generator

from .constants import Taakstatus
from .klantcontacten import Klantcontact


class InterneTaak(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de interne taak."),
    )
    actoren = models.ManyToManyField(
        "klantinteracties.Actor",
        verbose_name=_("actoren"),
        help_text=_("De actoren aan wie de interne taak werd toegewezen."),
        through="klantinteracties.InterneTakenActorenThoughModel",
    )
    klantcontact = models.ForeignKey(
        Klantcontact,
        on_delete=models.CASCADE,
        verbose_name=_("klantcontact"),
        help_text=_(
            "Het klantcontact dat aanleiding gaf tot het ontstaan van een interne taak."
        ),
    )
    nummer = models.CharField(
        _("nummer"),
        help_text=_(
            "Uniek identificerend nummer dat tijdens communicatie tussen mensen kan "
            "worden gebruikt om de specifieke interne taak aan te duiden."
        ),
        validators=[validate_integer],
        max_length=10,
        unique=True,
        blank=True,
    )
    gevraagde_handeling = models.CharField(
        _("gevraagde handeling"),
        help_text=_("Handeling die moet worden uitgevoerd om de taak af te ronden."),
        max_length=200,
    )
    toelichting = models.TextField(
        _("toelichting"),
        help_text=_(
            "Toelichting die, aanvullend bij de inhoud van het klantcontact dat "
            "aanleiding gaf tot de taak en de gevraagde handeling, "
            "bijdraagt aan het kunnen afhandelen van de taak."
        ),
        max_length=1000,
        blank=True,
    )
    status = models.CharField(
        _("status"),
        help_text=_("Aanduiding van de vordering bij afhandeling van de interne taak."),
        choices=Taakstatus.choices,
        max_length=12,
    )
    toegewezen_op = models.DateTimeField(
        _("toegewezen op"),
        help_text=_(
            "Datum en tijdstip waarop de interne taak aan een actor werd toegewezen."
        ),
        auto_now_add=True,
        blank=False,
    )
    afgehandeld_op = models.DateTimeField(
        _("afgehandeld op"),
        help_text=_(
            "Datum en tijdstip wanneer de interne taak was afgehandeld: EXPERIMENTEEL."
        ),
        editable=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("interne taak")
        verbose_name_plural = _("interne taken")

    def save(self, *args, **kwargs):
        number_generator(self, InterneTaak)
        if self.afgehandeld_op is None:
            if self.status == Taakstatus.verwerkt:
                self.afgehandeld_op = timezone.now()
        else:
            if self.status == Taakstatus.te_verwerken:
                self.afgehandeld_op = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.klantcontact} - ({self.nummer})"


# Added for deprecated toegewezen_aan_actor field to return correct order
class InterneTakenActorenThoughModel(OrderedModel):
    actor = models.ForeignKey("klantinteracties.Actor", on_delete=models.CASCADE)
    internetaak = models.ForeignKey(
        "klantinteracties.InterneTaak", on_delete=models.CASCADE
    )
    order_with_respect_to = "internetaak"

    class Meta:
        ordering = ("actor", "order")
