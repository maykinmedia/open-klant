import uuid

from django.core.validators import validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from .actoren import Actor
from .constants import Initiator, Klantcontrol
from .digitaal_adres import DigitaalAdres
from .mixins import BezoekAdresMixin, ContactNaamMixin, CorrespondentieAdresMixin


class Klantcontact(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de betrokkene bij klantcontact."
        ),
    )
    klantcontact = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="klantcontacten",
        verbose_name=_("Klant contact"),
        help_text=_(
            "De persoon of organisatie die betrokken was bij een klantcontact."
        ),
        blank=True,
        null=True,
    )
    actoren = models.ManyToManyField(
        Actor,
        verbose_name=_("Actoren"),
        related_name="klantcontacten",
        help_text=_(
            "De actoren die tijdens het klantcontant contact had met klanten of hun vertegenwoordigers."
        ),
        blank=False,
    )
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


class Betrokkene(BezoekAdresMixin, CorrespondentieAdresMixin, ContactNaamMixin):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de betrokkene bij klantcontact."
        ),
    )
    klantcontact = models.ForeignKey(
        Klantcontact,
        on_delete=models.CASCADE,
        verbose_name=_("Klantcontact"),
        related_name="betrokkene",
        help_text=_("'Klantcontact' had 'Betrokkene bij klantcontact'"),
        null=False,
    )
    digitaal_adres = models.ForeignKey(
        DigitaalAdres,
        on_delete=models.CASCADE,
        verbose_name=_("Digitaal adres"),
        related_name="partijen",
        help_text=_("'Digitaal Adres' had 'Betrokkene bij klantcontact'"),
        null=True,
    )
    rol = models.CharField(
        _("Rol"),
        help_text=_(
            "Rol die de betrokkene bij klantcontact tijdens dat contact vervulde."
        ),
        choices=Klantcontrol.choices,
        max_length=17,
    )
    organisatienaam = models.CharField(
        _("Organisatienaam"),
        help_text=_(
            "Naam van de organisatie waarmee de betrokkene bij klantcontact een relatie had."
        ),
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = _("betrokkene bij klantcontact")
