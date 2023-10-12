import uuid

from django.core.validators import MinLengthValidator, validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from .constants import Initiator, Klantcontrol


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


class Betrokkene(models.Model):
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
    # TODO: Add fk to Digital adres
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

    # Contactnaam model fields:
    contactnaam_voorletters = models.CharField(
        _("Voorletters"),
        help_text=_(
            "Een afkorting van de voornamen. Meestal de beginletter, maar in sommige gevallen "
            "de beginletter gecombineerd met de tweede letter van een voornaam."
        ),
        max_length=10,
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
    Contactnaam = GegevensGroepType(
        {
            "voorletters": contactnaam_voorletters,
            "voornaam": contactnaam_voornaam,
            "voorvoegsel achternaam": contactnaam_voorvoegsel_achternaam,
            "achternaam": contactnaam_achternaam,
        }
    )
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
        verbose_name = _("betrokkene bij klantcontact")
