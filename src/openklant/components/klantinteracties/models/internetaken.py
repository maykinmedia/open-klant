import uuid

from django.core.validators import validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from .actoren import Actor
from .constants import Taakstatus
from .klantcontacten import Klantcontact


class InterneTaak(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de interne taak."),
    )
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        verbose_name=_("actor"),
        help_text=_("De actor aan wie de interne taak werd toegewezen."),
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

    class Meta:
        verbose_name = _("interne taak")
        verbose_name_plural = _("interne taken")
