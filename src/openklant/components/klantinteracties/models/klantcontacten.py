import uuid

from django.core.validators import validate_integer
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .actoren import Actor
from .constants import Klantcontrol
from .digitaal_adres import DigitaalAdres
from .mixins import (
    BezoekadresMixin,
    ContactnaamMixin,
    CorrespondentieadresMixin,
    ObjectidentificatorMixin,
)


class Klantcontact(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de betrokkene bij klantcontact."
        ),
    )
    actoren = models.ManyToManyField(
        Actor,
        verbose_name=_("actoren"),
        related_name="klantcontacten",
        help_text=_(
            "De actoren die tijdens het klantcontant contact had met klanten of hun vertegenwoordigers."
        ),
        blank=False,
    )
    nummer = models.CharField(
        _("nummer"),
        help_text=_(
            "Uniek identificerend nummer dat tijdens communicatie tussen mensen kan "
            "worden gebruikt om het specifieke klantcontact aan te duiden."
        ),
        validators=[validate_integer],
        max_length=10,
    )
    kanaal = models.CharField(
        _("kanaal"),
        help_text=_("Communicatiekanaal dat bij het klantcontact werd gebruikt."),
        max_length=50,
    )
    onderwerp = models.CharField(
        _("onderwerp"),
        help_text=_("Datgene waarover het klantcontact ging."),
        max_length=200,
    )
    inhoud = models.TextField(
        _("inhoud"),
        help_text=_(
            "Informatie die tijdens het klantcontact werd overgebracht of uitgewisseld, "
            "voor zover die voor betrokkenen of actoren relevant is."
        ),
        max_length=1000,
        blank=True,
    )
    indicatie_contact_gelukt = models.BooleanField(
        _("indicatie contact gelukt"),
        help_text=(
            "Geeft, indien bekend, aan of de poging contact tussen de gemeente "
            "en inwoner(s) of organisatie(s) tot stand te brengen succesvol was."
        ),
        null=True,
    )
    taal = models.CharField(
        _("taal"),
        help_text=_(
            "Taal, in ISO 639-2/B formaat, waarin de partij bij voorkeur contact heeft "
            "met de gemeente. Voorbeeld: nld. Zie: https://www.iso.org/standard/4767.html"
        ),
        max_length=3,
    )
    vertrouwelijk = models.BooleanField(
        _("vertrouwelijk"),
        help_text=_(
            "Geeft aan of onderwerp, inhoud en kenmerken van het klantcontact vertrouwelijk moeten worden behandeld."
        ),
    )
    plaatsgevonden_op = models.DateTimeField(
        _("plaatsgevonden op"),
        help_text=_(
            "Datum en tijdstip waarop het klantontact plaatsvond. Als het klantcontact "
            "een gesprek betrof, is dit het moment waarop het gesprek begon. "
            "Als het klantcontact verzending of ontvangst van informatie betrof, "
            "is dit bij benadering het moment waarop informatie door gemeente verzonden of ontvangen werd."
        ),
        default=timezone.now,
        blank=False,
    )

    class Meta:
        verbose_name = _("klantcontact")
        verbose_name_plural = _("klantcontacten")

    def __str__(self):
        return self.nummer


class Betrokkene(BezoekadresMixin, CorrespondentieadresMixin, ContactnaamMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de betrokkene bij klantcontact."
        ),
    )
    klantcontact = models.ForeignKey(
        Klantcontact,
        on_delete=models.CASCADE,
        verbose_name=_("klantcontact"),
        help_text=_("'Klantcontact' had 'Betrokkene bij klantcontact'"),
    )
    digitaal_adres = models.ForeignKey(
        DigitaalAdres,
        on_delete=models.CASCADE,
        verbose_name=_("digitaal adres"),
        help_text=_("'Digitaal Adres' had 'Betrokkene bij klantcontact'"),
        null=True,
        blank=True,
    )
    rol = models.CharField(
        _("rol"),
        help_text=_(
            "Rol die de betrokkene bij klantcontact tijdens dat contact vervulde."
        ),
        choices=Klantcontrol.choices,
        max_length=17,
    )
    organisatienaam = models.CharField(
        _("organisatienaam"),
        help_text=_(
            "Naam van de organisatie waarmee de betrokkene bij klantcontact een relatie had."
        ),
        max_length=200,
        blank=True,
    )
    # TODO: add help_text when it is provided
    initiator = models.BooleanField(
        _("initiator"),
    )

    class Meta:
        verbose_name = _("betrokkene bij klantcontact")
        verbose_name_plural = _("betrokkenen bij klantcontact")

    def __str__(self):
        return self.get_contactnaam()


class Onderwerpobject(ObjectidentificatorMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van het onderwerpdeel."),
    )
    klantcontact = models.ForeignKey(
        Klantcontact,
        on_delete=models.CASCADE,
        verbose_name=_("klantcontact"),
        help_text=_("'Klantcontact' ging over 'Onderwerpobject'"),
        null=True,
    )
    was_klantcontact = models.ForeignKey(
        Klantcontact,
        on_delete=models.CASCADE,
        verbose_name=_("was klantcontact"),
        related_name="was_onderwerpobject",
        help_text=_("'Onderwerpobject' was 'Klantcontact'"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("onderwerpobject")
        verbose_name_plural = _("onderwerpobjecten")


class Bijlage(ObjectidentificatorMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van het inhoudsdeel."),
    )
    klantcontact = models.ForeignKey(
        Klantcontact,
        on_delete=models.CASCADE,
        verbose_name=_("klantcontact"),
        help_text=_("'Klantcontact' omvatte 'Bijlage'"),
        null=True,
    )

    class Meta:
        verbose_name = _("bijlage")
        verbose_name_plural = _("bijlagen")
