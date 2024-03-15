import uuid

from django.core.validators import validate_integer
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from openklant.components.utils.mixins import APIMixin
from openklant.components.utils.number_generator import number_generator

from .constants import Klantcontrol
from .mixins import BezoekadresMixin, ContactnaamMixin, CorrespondentieadresMixin


class Klantcontact(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de betrokkene bij klantcontact."
        ),
    )
    nummer = models.CharField(
        _("nummer"),
        help_text=_(
            "Uniek identificerend nummer dat tijdens communicatie tussen mensen kan "
            "worden gebruikt om het specifieke klantcontact aan te duiden."
        ),
        validators=[validate_integer],
        max_length=10,
        unique=True,
        blank=True,
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

    def save(self, *args, **kwargs):
        number_generator(self, Klantcontact)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.onderwerp} ({self.nummer})"


class Betrokkene(
    APIMixin, BezoekadresMixin, CorrespondentieadresMixin, ContactnaamMixin
):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de betrokkene bij klantcontact."
        ),
    )
    partij = models.ForeignKey(
        "klantinteracties.Partij",
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
        help_text=_("'Betrokkene bij klantcontact' was 'Partij'"),
        null=True,
        blank=True,
    )
    klantcontact = models.ForeignKey(
        Klantcontact,
        on_delete=models.CASCADE,
        verbose_name=_("klantcontact"),
        help_text=_("'Klantcontact' had 'Betrokkene bij klantcontact'"),
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
        if self.get_full_name():
            if self.organisatienaam:
                return f"{self.organisatienaam} ({self.get_full_name()})"
            return self.get_full_name()

        return str(self.partij)


class Onderwerpobject(models.Model):
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

    onderwerpobjectidentificator_object_id = models.CharField(
        _("object ID"),
        help_text=_(
            "Waarde van de eigenschap die het object identificeert, bijvoorbeeld: '123456788'."
        ),
        max_length=200,
        blank=True,
    )
    onderwerpobjectidentificator_code_objecttype = models.CharField(
        _("code objecttype"),
        help_text=_(
            "Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'."
        ),
        max_length=200,
        blank=True,
    )
    onderwerpobjectidentificator_code_register = models.CharField(
        _("code register"),
        help_text=_(
            "Binnen het landschap van registers unieke omschrijving van het register waarin "
            "het object is geregistreerd, bijvoorbeeld: 'BRP'."
        ),
        max_length=200,
        blank=True,
    )
    onderwerpobjectidentificator_code_soort_object_id = models.CharField(
        _("code soort object ID"),
        help_text=_(
            "Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'."
        ),
        max_length=200,
        blank=True,
    )

    onderwerpobjectidentificator = GegevensGroepType(
        {
            "object_id": onderwerpobjectidentificator_object_id,
            "code_objecttype": onderwerpobjectidentificator_code_objecttype,
            "code_register": onderwerpobjectidentificator_code_register,
            "code_soort_object_id": onderwerpobjectidentificator_code_soort_object_id,
        },
        optional=(
            "object_id",
            "code_objecttype",
            "code_register",
            "code_soort_object_id",
        ),
    )

    class Meta:
        verbose_name = _("onderwerpobject")
        verbose_name_plural = _("onderwerpobjecten")

    def __str__(self):
        soort_object = self.onderwerpobjectidentificator_code_soort_object_id
        object = self.onderwerpobjectidentificator_object_id

        return f"{self.klantcontact} - ({soort_object} - {object})"


class Bijlage(APIMixin, models.Model):
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

    bijlageidentificator_object_id = models.CharField(
        _("object ID"),
        help_text=_(
            "Waarde van de eigenschap die het object identificeert, bijvoorbeeld: '123456788'."
        ),
        max_length=200,
        blank=True,
    )
    bijlageidentificator_code_objecttype = models.CharField(
        _("code objecttype"),
        help_text=_(
            "Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'."
        ),
        max_length=200,
        blank=True,
    )
    bijlageidentificator_code_register = models.CharField(
        _("code register"),
        help_text=_(
            "Binnen het landschap van registers unieke omschrijving van het register waarin "
            "het object is geregistreerd, bijvoorbeeld: 'BRP'."
        ),
        max_length=200,
        blank=True,
    )
    bijlageidentificator_code_soort_object_id = models.CharField(
        _("code soort object ID"),
        help_text=_(
            "Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'."
        ),
        max_length=200,
        blank=True,
    )

    bijlageidentificator = GegevensGroepType(
        {
            "object_id": bijlageidentificator_object_id,
            "code_objecttype": bijlageidentificator_code_objecttype,
            "code_register": bijlageidentificator_code_register,
            "code_soort_object_id": bijlageidentificator_code_soort_object_id,
        },
        optional=(
            "object_id",
            "code_objecttype",
            "code_register",
            "code_soort_object_id",
        ),
    )

    class Meta:
        verbose_name = _("bijlage")
        verbose_name_plural = _("bijlagen")

    def __str__(self):
        soort_object = self.bijlageidentificator_code_soort_object_id
        object = self.bijlageidentificator_object_id

        return f"{self.klantcontact} - ({soort_object} - {object})"
