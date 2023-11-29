import uuid

from django.core.exceptions import ValidationError
from django.core.validators import validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from .constants import SoortPartij
from .mixins import BezoekadresMixin, ContactnaamMixin, CorrespondentieadresMixin


class Partij(BezoekadresMixin, CorrespondentieadresMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de partij."),
    )
    voorkeurs_digitaal_adres = models.ForeignKey(
        "klantinteracties.DigitaalAdres",
        on_delete=models.CASCADE,
        related_name="voorkeurs_partij",
        verbose_name=_("voorkeurs digitaal adres"),
        help_text=_("'Partij' gaf voorkeur aan voor contact via 'Digitaal adres'"),
        null=True,
        blank=True,
    )
    vertegenwoordigde = models.ManyToManyField(
        "self",
        verbose_name=_("vertegenwoordigde"),
        help_text=_("'Partij' die een andere 'Partij' vertegenwoordigde."),
        blank=True,
        null=True,
    )
    nummer = models.CharField(
        _("nummer"),
        help_text=_(
            "Uniek identificerend nummer dat tijdens communicatie tussen mensen kan "
            "worden gebruikt om de specifieke partij aan te duiden."
        ),
        validators=[validate_integer],
        max_length=10,
    )
    interne_notitie = models.TextField(
        _("interne notitie"),
        help_text=_(
            "Mededelingen, aantekeningen of bijzonderheden over de partij, bedoeld voor intern gebruik."
        ),
        max_length=1000,
        blank=True,
    )
    soort_partij = models.CharField(
        _("soort partij"),
        help_text=_("Geeft aan van welke specifieke soort partij sprake is."),
        max_length=14,
        choices=SoortPartij.choices,
    )
    indicatie_geheimhouding = models.BooleanField(
        _("indicatie geheimhouding"),
        help_text=_(
            "Geeft aan of de verstrekker van partijgegevens heeft aangegeven dat "
            "deze gegevens als geheim beschouwd moeten worden."
        ),
    )
    voorkeurstaal = models.CharField(
        _("voorkeurstaal"),
        help_text=_(
            "Taal, in ISO 639-2/B formaat, waarin de partij bij voorkeur contact heeft "
            "met de gemeente. Voorbeeld: nld. Zie: https://www.iso.org/standard/4767.html"
        ),
        max_length=3,
        blank=True,
    )
    indicatie_actief = models.BooleanField(
        _("indicatie actief"),
        help_text=_(
            "Geeft aan of de contactgegevens van de partij nog gebruikt morgen worden om contact op te nemen. "
            "Gegevens van niet-actieve partijen mogen hiervoor niet worden gebruikt."
        ),
    )

    class Meta:
        verbose_name = _("partij")
        verbose_name_plural = _("partijen")

        def __str__(self):
            return self.nummer

    def clean(self):
        super().clean()

        if self.voorkeurs_digitaal_adres:
            if self.voorkeurs_digitaal_adres not in self.digitaaladres_set.all():
                raise ValidationError(
                    _("Het voorkeurs adres moet een gelinkte digitaal adres zijn.")
                )


class Organisatie(models.Model):
    partij = models.OneToOneField(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
    )
    naam = models.CharField(
        _("naam"),
        help_text=_("Naam van de organisatie."),
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = _("organisatie")
        verbose_name_plural = _("organisaties")

    def __str__(self):
        return self.naam


class Persoon(ContactnaamMixin):
    partij = models.OneToOneField(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
    )

    class Meta:
        verbose_name = _("persoon")
        verbose_name_plural = _("personen")

    def __str__(self):
        return self.contactnaam_voorletters


class Contactpersoon(ContactnaamMixin):
    partij = models.OneToOneField(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
    )
    organisatie = models.ForeignKey(
        Organisatie,
        on_delete=models.CASCADE,
        verbose_name=_("organistatie"),
        help_text=_("De organisatie waar een contactpersoon voor werkt."),
        null=True,
    )

    class Meta:
        verbose_name = _("contact persoon")
        verbose_name_plural = _("contact personen")

    def __str__(self):
        return self.contactnaam_voorletters


class PartijIdentificator(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de partij-identificator."
        ),
    )
    partij = models.ForeignKey(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
        help_text=_("'Partij' had 'PartijIdentificator'"),
        null=True,
    )
    andere_partij_identificator = models.CharField(
        _("andere partij indetificator"),
        help_text=_(
            "Vrij tekstveld om de verwijzing naar een niet-voorgedefinieerd objecttype, "
            "soort objectID of Register vast te leggen. "
        ),
        max_length=200,
        blank=True,
    )

    # Partij-identificator fields
    partij_identificator_objecttype = models.CharField(
        _("objecttype"),
        help_text=_(
            "Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'."
        ),
        max_length=200,
        blank=True,
    )
    partij_identificator_soort_object_id = models.CharField(
        _("soort object ID"),
        help_text=_(
            "Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'."
        ),
        max_length=200,
        blank=True,
    )
    partij_identificator_object_id = models.CharField(
        _("object ID"),
        help_text=_(
            "Waarde van de eigenschap die het object identificeert, bijvoorbeeld: '123456788'."
        ),
        max_length=200,
        blank=True,
    )
    partij_identificator_register = models.CharField(
        _("register"),
        help_text=_(
            "Binnen het landschap van registers unieke omschrijving van het register waarin "
            "het object is geregistreerd, bijvoorbeeld: 'BRP'."
        ),
        max_length=200,
        blank=True,
    )

    partij_identificator = GegevensGroepType(
        {
            "objecttype": partij_identificator_objecttype,
            "soort_object_id": partij_identificator_soort_object_id,
            "object_id": partij_identificator_object_id,
            "register": partij_identificator_register,
        },
        optional=(
            "objecttype",
            "soort_object_id",
            "object_id",
            "register",
        ),
    )

    class Meta:
        verbose_name = _("partij identificator")
        verbose_name_plural = _("partij identificatoren")
