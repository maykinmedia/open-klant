import uuid

from django.core.validators import validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import Initiator


class Klantcontact(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de betrokkene bij klantcontact."
        ),
    )
    # TODO: add fk to Actor
    # TODO: add fk to Onderwerpobject
    # TODO: add fk to Inhoudsobject
    nummer = models.CharField(
        _("Nummer"),
        help_text=_(
            "Uniek identificerend nummer dat tijdens communicatie tussen mensen kan "
            "worden gebruikt om het specifieke klantcontact aan te duiden."
        ),
        validators=[validate_integer],
        max_length=10,
    )
    kanaal = models.CharField(
        _("Kanaal"),
        help_text=_("Communicatiekanaal dat bij het klantcontact werd gebruikt."),
        max_length=50,
    )
    onderwerp = models.CharField(
        _("Onderwerp"),
        help_text=_("Datgene waarover het klantcontact ging."),
        max_length=200,
    )
    inhoud = models.CharField(
        _("Inhoud"),
        help_text=_(
            "Informatie die tijdens het klantcontact werd overgebracht of uitgewisseld, "
            "voor zover die voor betrokkenen of actoren relevant is."
        ),
        max_length=1000,
        blank=True,
    )
    initiator = models.CharField(
        _("Initiator"),
        help_text=_("Degene die het klantcontact initieerde."),
        choices=Initiator.choices,
        max_length=17,
    )
    indicatie_contact_gelukt = models.BooleanField(
        _("Indicatie contact gelukt"),
        help_text=(
            "Geeft, indien bekend, aan of de poging contact tussen de gemeente "
            "en inwoner(s) of organisatie(s) tot stand te brengen succesvol was."
        ),
        null=True,
    )
    taal = models.CharField(
        _("Taal"),
        help_text=_("Taal die bij het klantcontact werd gesproken of geschreven."),
        max_length=255,
    )
    vertrouwelijk = models.BooleanField(
        _("Vertrouwelijk"),
        help_text=_(
            "Geeft aan of onderwerp, inhoud en kenmerken van het klantcontact vertrouwelijk moeten worden behandeld."
        ),
    )
    # TODO: does this field require auto_now?
    plaatsgevonden_op = models.DateTimeField(
        _("Plaatsgevonden op"),
        help_text=_(
            "Datum en tijdstip waarop het klantontact plaatsvond. Als het klantcontact "
            "een gesprek betrof, is dit het moment waarop het gesprek begon. "
            "Als het klantcontact verzending of ontvangst van informatie betrof, "
            "is dit bij benadering het moment waarop informatie door gemeente verzonden of ontvangen werd."
        ),
        blank=False,
    )

    class Meta:
        verbose_name = _("klantcontact")
        verbose_name_plural = _("klantcontacten")
