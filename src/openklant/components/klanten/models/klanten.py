import uuid

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.fields import BSNField, RSINField
from vng_api_common.models import APIMixin

from .constants import GeslachtsAanduiding, KlantType, SoortRechtsvorm


class Klant(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke resource identifier (UUID4)"),
    )
    bronorganisatie = RSINField(
        help_text=_(
            "Het RSIN van de Niet-natuurlijk persoon zijnde de "
            "organisatie die de klant heeft gecreeerd. Dit moet een "
            "geldig RSIN zijn van 9 nummers en voldoen aan "
            "https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef"
        ),
    )
    klantnummer = models.CharField(
        max_length=8,
        help_text=_("De unieke identificatie van de klant binnen de bronorganisatie."),
    )
    bedrijfsnaam = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("De bedrijfsnaam van de klant."),
    )
    website_url = models.URLField(
        _("Website URL"),
        max_length=1000,
        help_text=_(
            "Het label of etiket dat aan de specifieke informatiebron, zoals "
            "een webpagina, een bestand of een plaatje op internet is toegewezen "
            "waar de KLANT in de regel op het internet vindbaar is."
        ),
        blank=True,
    )
    voornaam = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("De voornaam, voorletters of roepnaam van de klant."),
    )
    voorvoegsel_achternaam = models.CharField(
        max_length=10,
        blank=True,
        help_text=_("Het voorvoegsel van de achternaam van de klant."),
    )
    achternaam = models.CharField(
        max_length=200, blank=True, help_text=_("De achternaam van de klant.")
    )
    functie = models.CharField(
        max_length=200, blank=True, help_text=_("De functie van de klant.")
    )
    telefoonnummer = models.CharField(
        max_length=20,
        blank=True,
        help_text=_("Het mobiele of vaste telefoonnummer van de klant."),
    )
    emailadres = models.EmailField(
        blank=True, help_text=_("Het e-mail adres van de klant.")
    )
    subject = models.URLField(
        help_text=_("URL-referentie naar een subject"), max_length=1000, blank=True
    )
    subject_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=KlantType.choices,
        help_text=_("Type van de `subject`."),
    )
    aanmaakkanaal = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Het communicatiekanaal waarlangs de klant is aangemaakt."),
    )
    geverifieerd = models.BooleanField(
        default=False, help_text=_("Geeft aan of de KLANT wel of niet geverifieerd is.")
    )

    class Meta:
        verbose_name = "klant"
        verbose_name_plural = "klanten"
        unique_together = ("bronorganisatie", "klantnummer")

    @property
    def subject_identificatie(self):
        if hasattr(self, self.subject_type):
            return getattr(self, self.subject_type)
        return None

    def unique_representation(self):
        return f"{self.bronorganisatie} - {self.klantnummer}"


class NatuurlijkPersoon(models.Model):
    klant = models.OneToOneField(
        Klant, on_delete=models.CASCADE, related_name="natuurlijk_persoon"
    )

    inp_bsn = BSNField(
        blank=True,
        help_text=_(
            "Het burgerservicenummer, bedoeld in artikel 1.1 van de Wet "
            "algemene bepalingen burgerservicenummer."
        ),
    )
    anp_identificatie = models.CharField(
        max_length=17,
        blank=True,
        help_text=_(
            "Het door de gemeente uitgegeven unieke nummer voor een ANDER NATUURLIJK PERSOON"
        ),
    )
    inp_a_nummer = models.CharField(
        max_length=10,
        blank=True,
        help_text=_("Het administratienummer van de persoon, bedoeld in de Wet BRP"),
        validators=[
            RegexValidator(
                regex=r"^[1-9][0-9]{9}$",
                message=_("inpA_nummer must consist of 10 digits"),
                code="a-nummer-incorrect-format",
            )
        ],
    )
    geslachtsnaam = models.CharField(
        max_length=200, blank=True, help_text=_("De stam van de geslachtsnaam.")
    )
    voorvoegsel_geslachtsnaam = models.CharField(max_length=80, blank=True)
    voorletters = models.CharField(
        max_length=20,
        blank=True,
        help_text=_(
            "De verzameling letters die gevormd wordt door de eerste letter van "
            "alle in volgorde voorkomende voornamen."
        ),
    )
    voornamen = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Voornamen bij de naam die de persoon wenst te voeren."),
    )
    geslachtsaanduiding = models.CharField(
        max_length=1,
        blank=True,
        help_text=_(
            "Een aanduiding die aangeeft of de persoon een man of een vrouw is, "
            "of dat het geslacht nog onbekend is."
        ),
        choices=GeslachtsAanduiding.choices,
    )
    geboortedatum = models.CharField(max_length=18, blank=True)

    class Meta:
        verbose_name = "natuurlijk persoon"

    def unique_representation(self):
        return f"{self.inp_bsn or self.anp_identificatie or self.inp_a_nummer}"


class NietNatuurlijkPersoon(models.Model):
    klant = models.OneToOneField(
        Klant,
        on_delete=models.CASCADE,
        related_name="niet_natuurlijk_persoon",
    )

    inn_nnp_id = RSINField(
        blank=True,
        help_text=_(
            "Het door een kamer toegekend uniek nummer voor de INGESCHREVEN NIET-NATUURLIJK PERSOON"
        ),
    )

    ann_identificatie = models.CharField(
        max_length=17,
        blank=True,
        help_text=_(
            "Het door de gemeente uitgegeven unieke nummer voor een ANDER NIET-NATUURLIJK PERSOON"
        ),
    )

    statutaire_naam = models.TextField(
        max_length=500,
        blank=True,
        help_text=_(
            "Naam van de niet-natuurlijke persoon zoals deze is vastgelegd in de "
            "statuten (rechtspersoon) of in de vennootschapsovereenkomst is "
            "overeengekomen (Vennootschap onder firma of Commanditaire vennootschap)."
        ),
    )

    inn_rechtsvorm = models.CharField(
        max_length=50,
        choices=SoortRechtsvorm.choices,
        blank=True,
        help_text=_("De juridische vorm van de NIET-NATUURLIJK PERSOON."),
    )
    bezoekadres = models.CharField(
        max_length=1000,
        blank=True,
        help_text=_("De gegevens over het adres van de NIET-NATUURLIJK PERSOON"),
    )

    class Meta:
        verbose_name = "niet-natuurlijk persoon"

    def unique_representation(self):
        return f"{self.inn_nnp_id or self.ann_identificatie}"


class Vestiging(models.Model):
    """
    Een gebouw of complex van gebouwen waar duurzame uitoefening van de activiteiten
    van een onderneming of rechtspersoon plaatsvindt.
    """

    klant = models.OneToOneField(Klant, on_delete=models.CASCADE)

    vestigings_nummer = models.CharField(
        max_length=24,
        blank=True,
        help_text=_("Een korte unieke aanduiding van de Vestiging."),
    )
    handelsnaam = ArrayField(
        models.TextField(max_length=625, blank=True),
        default=list,
        help_text=_("De naam van de vestiging waaronder gehandeld wordt."),
    )

    class Meta:
        verbose_name = "vestiging"

    def unique_representation(self):
        return f"{self.vestigings_nummer}"


# models for nested objects
class SubVerblijfBuitenland(models.Model):
    """
    Datamodel afwijking, model representatie van de Groepattribuutsoort 'Verblijf buitenland'
    """

    natuurlijkpersoon = models.OneToOneField(
        NatuurlijkPersoon,
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_verblijf_buitenland",
    )
    nietnatuurlijkpersoon = models.OneToOneField(
        NietNatuurlijkPersoon,
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_verblijf_buitenland",
    )
    vestiging = models.OneToOneField(
        Vestiging,
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_verblijf_buitenland",
    )
    lnd_landcode = models.CharField(
        max_length=4,
        help_text=_(
            "De code, behorende bij de landnaam, zoals opgenomen in de Land/Gebied-tabel van de BRP."
        ),
    )
    lnd_landnaam = models.CharField(
        max_length=40,
        help_text=_(
            "De naam van het land, zoals opgenomen in de Land/Gebied-tabel van de BRP."
        ),
    )
    sub_adres_buitenland_1 = models.CharField(max_length=35, blank=True)
    sub_adres_buitenland_2 = models.CharField(max_length=35, blank=True)
    sub_adres_buitenland_3 = models.CharField(max_length=35, blank=True)

    def clean(self):
        super().clean()
        if (
            self.natuurlijkpersoon is None
            and self.nietnatuurlijkpersoon is None
            and self.vestiging is None
        ):
            raise ValidationError(
                "Relations to NatuurlijkPersoon, NietNatuurlijkPersoon or Vestiging "
                "models should be set"
            )


class AdresBase(models.Model):
    huisnummer = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999)], blank=True, null=True
    )
    huisletter = models.CharField(max_length=1, blank=True)
    huisnummertoevoeging = models.CharField(max_length=4, blank=True)
    postcode = models.CharField(max_length=7, blank=True)
    woonplaats_naam = models.CharField(max_length=80, blank=True)

    class Meta:
        abstract = True


class VerblijfsAdres(AdresBase):
    natuurlijkpersoon = models.OneToOneField(
        NatuurlijkPersoon,
        on_delete=models.CASCADE,
        null=True,
        related_name="verblijfsadres",
    )
    vestiging = models.OneToOneField(
        Vestiging,
        on_delete=models.CASCADE,
        null=True,
        related_name="verblijfsadres",
    )
    aoa_identificatie = models.CharField(
        max_length=100, help_text=_("De unieke identificatie van het OBJECT")
    )

    gor_openbare_ruimte_naam = models.CharField(
        max_length=80,
        help_text=_(
            "Een door het bevoegde gemeentelijke orgaan aan een "
            "OPENBARE RUIMTE toegekende benaming"
        ),
    )

    inp_locatiebeschrijving = models.CharField(max_length=1000, blank=True)

    def clean(self):
        super().clean()
        if self.natuurlijkpersoon is None and self.vestiging is None:
            raise ValidationError(
                "Relations to NatuurlijkPersoon or Vestiging models should be set"
            )


class KlantAdres(AdresBase):
    klant = models.OneToOneField(Klant, on_delete=models.CASCADE, related_name="adres")
    straatnaam = models.CharField(max_length=100, blank=True)
    landcode = models.CharField(
        max_length=4,
        blank=True,
        help_text=_(
            "De code, behorende bij de landnaam, zoals opgenomen in de Land/Gebied-tabel van de BRP."
        ),
    )
