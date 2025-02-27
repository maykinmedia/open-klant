import uuid

from django.core.exceptions import ValidationError
from django.core.validators import validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from openklant.components.utils.mixins import APIMixin
from openklant.components.utils.number_generator import number_generator

from .constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
    SoortPartij,
)
from .mixins import BezoekadresMixin, ContactnaamMixin, CorrespondentieadresMixin


class Partij(APIMixin, BezoekadresMixin, CorrespondentieadresMixin):
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
    voorkeurs_rekeningnummer = models.ForeignKey(
        "klantinteracties.Rekeningnummer",
        on_delete=models.CASCADE,
        related_name="voorkeurs_rekeningnummer",
        verbose_name=_("voorkeurs rekeningnummer"),
        help_text=_("'Partij' gaf voorkeur voor 'rekeningnummer'"),
        null=True,
        blank=True,
    )
    nummer = models.CharField(
        _("nummer"),
        help_text=_(
            "Uniek identificerend nummer dat tijdens communicatie tussen mensen kan "
            "worden gebruikt om de specifieke partij aan te duiden."
        ),
        validators=[validate_integer],
        max_length=10,
        unique=True,
        blank=True,
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
            "deze gegevens als geheim beschouwd moeten worden. Als dit niet aangegeven is "
            "dan wordt dit ingevuld als `null`."
        ),
        null=True,
        default=None,
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

    def clean(self):
        super().clean()

        if self.voorkeurs_digitaal_adres:
            if self.voorkeurs_digitaal_adres not in self.digitaaladres_set.all():
                raise ValidationError(
                    _("Het voorkeurs adres moet een gelinkte digitaal adres zijn.")
                )

        if self.voorkeurs_rekeningnummer:
            if self.voorkeurs_rekeningnummer not in self.rekeningnummer_set.all():
                raise ValidationError(
                    _(
                        "Het voorkeurs rekeningnummer moet een gelinkte rekeningnummer zijn."
                    )
                )

    def save(self, *args, **kwargs):
        number_generator(self, Partij)
        return super().save(*args, **kwargs)

    def __str__(self):
        if soort_partij := self.soort_partij:
            match (soort_partij):
                case SoortPartij.persoon:
                    partij = Persoon.objects.get(partij__uuid=self.uuid)
                case SoortPartij.organisatie:
                    partij = Organisatie.objects.get(partij__uuid=self.uuid)
                case SoortPartij.contactpersoon:
                    partij = Contactpersoon.objects.get(partij__uuid=self.uuid)

            return f"{partij} ({self.nummer})"

        return self.nummer


class Vertegenwoordigden(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de vertegenwoordigden."),
    )
    vertegenwoordigende_partij = models.ForeignKey(
        "klantinteracties.Partij",
        on_delete=models.CASCADE,
        verbose_name=_("vertegenwoordigende partij"),
        related_name="vertegenwoordigende",
        help_text=_("'Partij' die een andere 'Partij' vertegenwoordigde."),
    )
    vertegenwoordigde_partij = models.ForeignKey(
        "klantinteracties.Partij",
        on_delete=models.CASCADE,
        verbose_name=_("vertegenwoordigde partij"),
        related_name="vertegenwoordigde",
        help_text=_("'Partij' vertegenwoordigd wordt door een andere 'Partij'."),
    )

    class Meta:
        verbose_name = _("vertegenwoordigde")
        verbose_name_plural = _("vertegenwoordigden")
        unique_together = (
            "vertegenwoordigende_partij",
            "vertegenwoordigde_partij",
        )

    def clean(self):
        super().clean()

        if self.vertegenwoordigde_partij == self.vertegenwoordigende_partij:
            raise ValidationError(_("De partij kan niet zichzelf vertegenwoordigen."))

    def __str__(self):
        return f"{self.vertegenwoordigende_partij} - {self.vertegenwoordigde_partij}"


class CategorieRelatie(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de Categorie Relatie."),
    )
    partij = models.ForeignKey(
        "klantinteracties.Partij",
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
        help_text=_("De 'categorie relatie' van een 'Partij'."),
        null=True,
        blank=True,
    )
    categorie = models.ForeignKey(
        "klantinteracties.Categorie",
        on_delete=models.CASCADE,
        verbose_name=_("categorie"),
        help_text=_("De 'categorie' van deze 'categorie relatie'."),
        null=True,
        blank=True,
    )
    begin_datum = models.DateField(
        _("begin datum"),
        editable=True,
        null=True,
        blank=True,
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst "
            "significante onderdeel. Een voorbeeld: 2022-02-21"
        ),
    )
    eind_datum = models.DateField(
        _("eind datum"),
        editable=True,
        null=True,
        blank=True,
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst "
            "significante onderdeel. Een voorbeeld: 2022-02-21"
        ),
    )

    class Meta:
        verbose_name = _("categorie relatie")
        verbose_name_plural = _("categorieën relatie")

    def __str__(self):
        if self.categorie and self.partij:
            return f"{self.categorie} - {self.partij}"
        elif self.categorie:
            return self.categorie

        return str(self.uuid)


class Categorie(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de Categorie."),
    )
    naam = models.CharField(
        _("naam"),
        help_text=_("Naam van de categorie."),
        max_length=80,
        blank=True,
    )

    class Meta:
        verbose_name = _("categorie")
        verbose_name_plural = _("categorieën")

    def __str__(self):
        return self.naam


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
        return self.get_full_name()


class Contactpersoon(ContactnaamMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de contactpersoon."),
    )
    partij = models.OneToOneField(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("partij"),
    )
    werkte_voor_partij = models.ForeignKey(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("werkte voor partij"),
        related_name="werkte_voor_partij",
        help_text=_("De organisatie waar een contactpersoon voor werkt."),
        null=True,
    )

    class Meta:
        verbose_name = _("contact persoon")
        verbose_name_plural = _("contact personen")

    def clean(self):
        super().clean()

        if self.werkte_voor_partij:
            if self.werkte_voor_partij.soort_partij != SoortPartij.organisatie:
                raise ValidationError(
                    _("Partij object moet het soort 'organisatie' hebben.")
                )

    def __str__(self):
        return self.get_full_name()


class PartijIdentificator(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_(
            "Unieke (technische) identificatiecode van de partij-identificator."
        ),
    )
    sub_identificator_van = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        verbose_name=_("sub identificator van"),
        help_text=_(
            "The parent PartijIdentificator under which this PartijIdentificator is unique "
            "(e.g. the parent identificator could specify a KVK number and the child "
            "identificator could specify a vestigingsnummer that is unique for the KVK number)."
        ),
        blank=True,
        null=True,
        related_name="parent_partij_identificator",
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
    partij_identificator_code_objecttype = models.CharField(
        _("objecttype"),
        help_text=_("Type van het object, bijvoorbeeld: 'natuurlijk_persoon'."),
        choices=PartijIdentificatorCodeObjectType.choices,
        max_length=200,
        blank=True,
    )
    partij_identificator_code_soort_object_id = models.CharField(
        _("soort object ID"),
        help_text=_(
            "Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'bsn'."
        ),
        choices=PartijIdentificatorCodeSoortObjectId.choices,
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
    partij_identificator_code_register = models.CharField(
        _("register"),
        help_text=_(
            "Binnen het landschap van registers unieke omschrijving van het register waarin "
            "het object is geregistreerd, bijvoorbeeld: 'BRP'."
        ),
        max_length=200,
        choices=PartijIdentificatorCodeRegister.choices,
        blank=True,
    )

    partij_identificator = GegevensGroepType(
        {
            "code_objecttype": partij_identificator_code_objecttype,
            "code_soort_object_id": partij_identificator_code_soort_object_id,
            "object_id": partij_identificator_object_id,
            "code_register": partij_identificator_code_register,
        },
        optional=(
            "code_objecttype",
            "code_soort_object_id",
            "object_id",
            "code_register",
        ),
    )

    class Meta:
        verbose_name = _("partij identificator")
        verbose_name_plural = _("partij identificatoren")

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "partij_identificator_code_objecttype",
                    "partij_identificator_code_soort_object_id",
                    "partij_identificator_object_id",
                    "partij_identificator_code_register",
                ],
                condition=models.Q(sub_identificator_van__isnull=True),
                name="non_scoped_identificator_globally_unique",
                violation_error_message=_(
                    "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie."
                ),
            ),
            models.UniqueConstraint(
                fields=[
                    "partij",
                    "partij_identificator_code_soort_object_id",
                ],
                name="non_scoped_identificator_locally_unique",
                violation_error_message=_(
                    "`CodeSoortObjectId` moet uniek zijn voor de Partij."
                ),
            ),
            models.UniqueConstraint(
                fields=[
                    "sub_identificator_van",
                    "partij_identificator_code_objecttype",
                    "partij_identificator_code_soort_object_id",
                    "partij_identificator_object_id",
                    "partij_identificator_code_register",
                ],
                condition=models.Q(sub_identificator_van__isnull=False),
                name="scoped_identificator_globally_unique",
                violation_error_message=_(
                    "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie."
                ),
            ),
        ]

    def clean_sub_identificator_van(self):
        if self.sub_identificator_van and self.sub_identificator_van == self:
            raise ValidationError(
                {
                    "sub_identificator_van": _(
                        "Een `Partijidentificator` kan geen `subIdentificatorVan` zijn van zichzelf."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.clean_sub_identificator_van()

    def __str__(self):
        return f"{self.partij_identificator_code_soort_object_id} - {self.partij_identificator_object_id}"
