import uuid

from django.core.validators import validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from .actoren import Actor
from .constants import Taakstatus
from .klantcontacten import Klantcontact


class InterneTaak(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de interne taak."),
    )
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        verbose_name=_("Actor"),
        related_name="interne_taak",
        help_text=_("De actor aan wie de interne taak werd toegewezen."),
        null=True,
    )
    klantcontact = models.ForeignKey(
        Klantcontact,
        on_delete=models.CASCADE,
        verbose_name=_("Klantcontact"),
        related_name="interne_taak",
        help_text=_(
            "Het klantcontact dat aanleiding gaf tot het ontstaan van een interne taak."
        ),
        null=True,
    )
    nummer = models.CharField(
        _("Nummer"),
        help_text=_(
            "Uniek identificerend nummer dat tijdens communicatie tussen mensen kan "
            "worden gebruikt om de specifieke interne taak aan te duiden."
        ),
        validators=[validate_integer],
        max_length=10,
    )
    gevraagde_handeling = models.CharField(
        _("Gevraagde handeling"),
        help_text=_("Handeling die moet worden uitgevoerd om de taak af te ronden."),
        max_length=200,
    )
    toelichting = models.CharField(
        _("Toelichting"),
        help_text=_(
            "Toelichting die, aanvullend bij de inhoud van het klantcontact dat "
            "aanleiding gaf tot de taak en de gevraagde handeling, "
            "bijdraagt aan het kunnen afhandelen van de taak."
        ),
        max_length=400,
    )
    status = models.CharField(
        _("Status"),
        help_text=_("Aanduiding van de vordering bij afhandeling van de interne taak."),
        choices=Taakstatus.choices,
        max_length=12,
    )
    toegewezen_op = models.DateTimeField(
        _("Toegewezen op"),
        help_text=_(
            "Datum en tijdstip waarop de interne taak aan een actor werd toegewezen."
        ),
        blank=False,
    )

    class Meta:
        verbose_name = _("interne taak")
        verbose_name_plural = _("interne taken")
