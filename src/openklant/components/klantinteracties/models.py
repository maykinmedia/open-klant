import uuid

from django.core.validators import MinLengthValidator, validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from .constants import SoortPartij


class Partij(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de partij."),
    )
    nummer = models.CharField(
        _("Nummer"),
        help_text=_(
            "Uniek identificerend nummer dat tijdens communicatie tussen mensen kan "
            "worden gebruikt om de specifieke partij aan te duiden."
        ),
        validators=[validate_integer],
        max_length=10,
    )
    interne_notitie = models.CharField(
        _("Interne notitie"),
        help_text=_(
            "Mededelingen, aantekeningen of bijzonderheden over de partij, bedoeld voor intern gebruik."
        ),
        max_length=1000,
        blank=True,
    )
    soort_partij = models.CharField(
        _("Soort partij"),
        help_text=_("Geeft aan van welke specifieke soort partij sprake is."),
        max_length=14,
        choices=SoortPartij.choices,
    )
    indicatie_geheimhouding = models.BooleanField(
        _("Indicatie geheimhouding"),
        help_text=_(
            "Geeft aan of de verstrekker van partijgegevens heeft aangegeven dat "
            "deze gegevens als geheim beschouwd moeten worden."
        ),
    )
    voorkeurskanaal = models.CharField(
        _("Voorkeurskanaal"),
        help_text=_(
            "Kanaal dat de partij bij voorkeur gebruikt voor contact met de gemeente."
        ),
        max_length=50,
        blank=True,
    )
    voorkeurstaal = models.CharField(
        _("Voorkeurstaal"),
        help_text=_(
            "Taal waarin de partij bij voorkeur contact heeft met de gemeente."
        ),
        max_length=255,
        blank=True,
    )
    indicatie_actief = models.BooleanField(
        _("Indicatie actief"),
        help_text=_(
            "Geeft aan of de contactgegevens van de partij nog gebruikt morgen worden om contact op te nemen. "
            "Gegevens van niet-actieve partijen mogen hiervoor niet worden gebruikt."
        ),
    )

    # Correspondentieadres model fields:
    correspondentieadres_nummeraanduiding_id = models.UUIDField(
        verbose_name=_("Nummeraanduiding ID"),
        help_text=_(
            "Identificatie van het adres bij de Basisregistratie Adressen en Gebouwen."
        ),
        unique=True,
        blank=True,
        null=True,
    )
    correspondentieadres_adresregel1 = models.CharField(
        _("Adresregel 1"),
        help_text=_(
            "Eerste deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    correspondentieadres_adresregel2 = models.CharField(
        _("Adresregel 2"),
        help_text=_(
            "Tweede deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    correspondentieadres_adresregel3 = models.CharField(
        _("Adresregel 3"),
        help_text=_(
            "Derde deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    correspondentieadres_land = models.CharField(
        _("Land"),
        help_text=_(
            "Een code, opgenomen in Tabel 34, Landentabel, die het land (buiten Nederland) "
            "aangeeft alwaar de ingeschrevene verblijft."
        ),
        validators=[
            MinLengthValidator(limit_value=4),
            validate_integer,
        ],
        max_length=4,
        blank=True,
    )

    # Bezoekadres model fields:
    bezoekadres_nummeraanduiding_id = models.UUIDField(
        verbose_name=_("Nummeraanduiding ID"),
        help_text=_(
            "Identificatie van het adres bij de Basisregistratie Adressen en Gebouwen."
        ),
        unique=True,
        blank=True,
        null=True,
    )
    bezoekadres_adresregel1 = models.CharField(
        _("Adresregel 1"),
        help_text=_(
            "Eerste deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    bezoekadres_adresregel2 = models.CharField(
        _("Adresregel 2"),
        help_text=_(
            "Tweede deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    bezoekadres_adresregel3 = models.CharField(
        _("Adresregel 3"),
        help_text=_(
            "Derde deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    bezoekadres_land = models.CharField(
        _("Land"),
        help_text=_(
            "Een code, opgenomen in Tabel 34, Landentabel, die het land (buiten Nederland) "
            "aangeeft alwaar de ingeschrevene verblijft."
        ),
        validators=[
            MinLengthValidator(limit_value=4),
            validate_integer,
        ],
        max_length=4,
        blank=True,
    )

    # Group types:
    correspondentieadres = GegevensGroepType(
        {
            "nummeraanduiding id": correspondentieadres_nummeraanduiding_id,
            "adresregel 1": correspondentieadres_adresregel1,
            "adresregel 2": correspondentieadres_adresregel2,
            "adresregel 3": correspondentieadres_adresregel3,
            "land": correspondentieadres_land,
        },
    )
    bezoekadres = GegevensGroepType(
        {
            "nummeraanduiding id": bezoekadres_nummeraanduiding_id,
            "adresregel 1": bezoekadres_adresregel1,
            "adresregel 2": bezoekadres_adresregel2,
            "adresregel 3": bezoekadres_adresregel3,
            "land": bezoekadres_land,
        }
    )

    class Meta:
        verbose_name = _("partij")
        verbose_name_plural = _("partijen")


class Organisatie(models.Model):
    partij = models.ForeignKey(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("Partij"),
        related_name="organisatie",
        null=True,
    )
    naam = models.CharField(
        _("Naam"),
        help_text=_("Naam van de organisatie."),
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = _("organisatie")
        verbose_name_plural = _("organisaties")

        def __str__(self) -> str:
            return self.naam


class Persoon(models.Model):
    partij = models.ForeignKey(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("Partij"),
        related_name="persoon",
        null=True,
    )
    # TODO: check if the max length is correct
    contactnaam_voorletters = models.CharField(
        _("Voorletters"),
        help_text=_(
            "Een afkorting van de voornamen. Meestal de beginletter, maar in sommige gevallen "
            "de beginletter gecombineerd met de tweede letter van een voornaam."
        ),
        max_length=6,
    )
    contactnaam_voornaam = models.CharField(
        _("Voornaam"),
        help_text=_(
            "De voornaam die de persoon wil gebruiken tijdens communicatie met de gemeente."
        ),
        max_length=200,
        blank=True,
    )
    contactnaam_voorvoegsel_achternaam = models.CharField(
        _("Voorvoegsel achternaam"),
        help_text=_(
            "Een eventueel voorvoegsel dat hoort bij de achternaam die de persoon "
            "wil gebruiken tijdens communicatie met de gemeente."
        ),
        max_length=10,
        blank=True,
    )
    contactnaam_achternaam = models.CharField(
        _("Achternaam"),
        help_text=_(
            "Een achternaam die de persoon wil gebruiken tijdens communicatie met de gemeente."
        ),
        max_length=200,
        blank=True,
    )

    Contactnaam = GegevensGroepType(
        {
            "voorletters": contactnaam_voorletters,
            "voornaam": contactnaam_voornaam,
            "voorvoegsel achternaam": contactnaam_voorvoegsel_achternaam,
            "achternaam": contactnaam_achternaam,
        }
    )

    class Meta:
        verbose_name = _("persoon")
        verbose_name_plural = _("personen")

        def __str__(self) -> str:
            return self.contactnaam_voorletters


class Contactpersoon(models.Model):
    partij = models.ForeignKey(
        Partij,
        on_delete=models.CASCADE,
        verbose_name=_("Partij"),
        related_name="contact_persoon",
        null=True,
    )
    organisatie = models.ForeignKey(
        Organisatie,
        on_delete=models.CASCADE,
        verbose_name=_("Organistatie"),
        related_name="contact_personen",
        help_text=_("De organisatie waar een contactpersoon voor werkt."),
        null=True,
    )
    # TODO: check if the max length is correct
    contactnaam_voorletters = models.CharField(
        _("Voorletters"),
        help_text=_(
            "Een afkorting van de voornamen. Meestal de beginletter, maar in sommige gevallen "
            "de beginletter gecombineerd met de tweede letter van een voornaam."
        ),
        max_length=6,
    )
    contactnaam_voornaam = models.CharField(
        _("Voornaam"),
        help_text=_(
            "De voornaam die de persoon wil gebruiken tijdens communicatie met de gemeente."
        ),
        max_length=200,
        blank=True,
    )
    contactnaam_voorvoegsel_achternaam = models.CharField(
        _("Voorvoegsel achternaam"),
        help_text=_(
            "Een eventueel voorvoegsel dat hoort bij de achternaam die de persoon "
            "wil gebruiken tijdens communicatie met de gemeente."
        ),
        max_length=10,
        blank=True,
    )
    contactnaam_achternaam = models.CharField(
        _("Achternaam"),
        help_text=_(
            "Een achternaam die de persoon wil gebruiken tijdens communicatie met de gemeente."
        ),
        max_length=200,
        blank=True,
    )

    Contactnaam = GegevensGroepType(
        {
            "voorletters": contactnaam_voorletters,
            "voornaam": contactnaam_voornaam,
            "voorvoegsel achternaam": contactnaam_voorvoegsel_achternaam,
            "achternaam": contactnaam_achternaam,
        }
    )

    class Meta:
        verbose_name = _("contact persoon")
        verbose_name_plural = _("contact personen")

        def __str__(self) -> str:
            return self.contactnaam_voorletters
