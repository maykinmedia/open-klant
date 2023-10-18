from django.core.validators import MinLengthValidator, validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType


class BezoekAdresMixin(models.Model):
    # TODO: Check if this is correct.
    bezoekadres_nummeraanduiding_id = models.CharField(
        _("nummeraanduiding id"),
        help_text=_(
            "Identificatie van het adres bij de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=255,
        blank=True,
    )
    bezoekadres_adresregel1 = models.CharField(
        _("adresregel 1"),
        help_text=_(
            "Eerste deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    bezoekadres_adresregel2 = models.CharField(
        _("adresregel 2"),
        help_text=_(
            "Tweede deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    bezoekadres_adresregel3 = models.CharField(
        _("adresregel 3"),
        help_text=_(
            "Derde deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    bezoekadres_land = models.CharField(
        _("land"),
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

    bezoekadres = GegevensGroepType(
        {
            "nummeraanduiding_id": bezoekadres_nummeraanduiding_id,
            "adresregel_1": bezoekadres_adresregel1,
            "adresregel_2": bezoekadres_adresregel2,
            "adresregel_3": bezoekadres_adresregel3,
            "land": bezoekadres_land,
        }
    )

    class Meta:
        abstract = True


class CorrespondentieAdresMixin(models.Model):
    # TODO: Check if this is correct.
    correspondentieadres_nummeraanduiding_id = models.CharField(
        _("nummeraanduiding ID"),
        help_text=_(
            "Identificatie van het adres bij de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=255,
        blank=True,
    )
    correspondentieadres_adresregel1 = models.CharField(
        _("adresregel 1"),
        help_text=_(
            "Eerste deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    correspondentieadres_adresregel2 = models.CharField(
        _("adresregel 2"),
        help_text=_(
            "Tweede deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    correspondentieadres_adresregel3 = models.CharField(
        _("adresregel 3"),
        help_text=_(
            "Derde deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    correspondentieadres_land = models.CharField(
        _("land"),
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

    correspondentieadres = GegevensGroepType(
        {
            "nummeraanduiding_id": correspondentieadres_nummeraanduiding_id,
            "adresregel_1": correspondentieadres_adresregel1,
            "adresregel_2": correspondentieadres_adresregel2,
            "adresregel_3": correspondentieadres_adresregel3,
            "land": correspondentieadres_land,
        },
    )

    class Meta:
        abstract = True


class ContactNaamMixin(models.Model):
    contactnaam_voorletters = models.CharField(
        _("voorletters"),
        help_text=_(
            "Een afkorting van de voornamen. Meestal de beginletter, maar in sommige gevallen "
            "de beginletter gecombineerd met de tweede letter van een voornaam."
        ),
        max_length=10,
    )
    contactnaam_voornaam = models.CharField(
        _("voornaam"),
        help_text=_(
            "De voornaam die de persoon wil gebruiken tijdens communicatie met de gemeente."
        ),
        max_length=200,
        blank=True,
    )
    contactnaam_voorvoegsel_achternaam = models.CharField(
        _("voorvoegsel achternaam"),
        help_text=_(
            "Een eventueel voorvoegsel dat hoort bij de achternaam die de persoon "
            "wil gebruiken tijdens communicatie met de gemeente."
        ),
        max_length=10,
        blank=True,
    )
    contactnaam_achternaam = models.CharField(
        _("achternaam"),
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
            "voorvoegsel_achternaam": contactnaam_voorvoegsel_achternaam,
            "achternaam": contactnaam_achternaam,
        }
    )

    class Meta:
        abstract = True


class IdentificatorMixin(models.Model):
    identificator_objecttype = models.CharField(
        _("objecttype"),
        help_text=_(
            "Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'."
        ),
        max_length=200,
        blank=False,
    )
    identificator_soort_object_id = models.CharField(
        _("soort object id"),
        help_text=_(
            "Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'."
        ),
        max_length=200,
        blank=False,
    )
    identificator_object_id = models.CharField(
        _("object id"),
        help_text=_(
            "Waarde van de eigenschap die het object identificeert, bijvoorbeeld: '123456788'."
        ),
        max_length=200,
        blank=False,
    )
    identificator_register = models.CharField(
        _("register"),
        help_text=_(
            "Binnen het landschap van registers unieke omschrijving van het register waarin "
            "het object is geregistreerd, bijvoorbeeld: 'BRP'."
        ),
        max_length=200,
        blank=False,
    )

    identificator = GegevensGroepType(
        {
            "objecttype": identificator_objecttype,
            "soort_object_id": identificator_soort_object_id,
            "object_id": identificator_object_id,
            "register": identificator_register,
        }
    )

    class Meta:
        abstract = True
