from django.core.validators import MinLengthValidator, validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType


class BezoekAdresMixin(models.Model):
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
        abstract = True


class CorrespondentieAdresMixin(models.Model):
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

    correspondentieadres = GegevensGroepType(
        {
            "nummeraanduiding id": correspondentieadres_nummeraanduiding_id,
            "adresregel 1": correspondentieadres_adresregel1,
            "adresregel 2": correspondentieadres_adresregel2,
            "adresregel 3": correspondentieadres_adresregel3,
            "land": correspondentieadres_land,
        },
    )

    class Meta:
        abstract = True


class ContactNaamMixin(models.Model):
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

    Contactnaam = GegevensGroepType(
        {
            "voorletters": contactnaam_voorletters,
            "voornaam": contactnaam_voornaam,
            "voorvoegsel achternaam": contactnaam_voorvoegsel_achternaam,
            "achternaam": contactnaam_achternaam,
        }
    )

    class Meta:
        abstract = True


class ActorIdentifcatorMixin(models.Model):
    actoridentifcator_objecttype = models.CharField(
        _("Objecttype"),
        help_text=_(
            "Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'."
        ),
        max_length=200,
        blank=False,
    )
    actoridentifcator_soort_object_id = models.CharField(
        _("Soort Object ID"),
        help_text=_(
            "Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'."
        ),
        max_length=200,
        blank=False,
    )
    actoridentifcator_object_id = models.CharField(
        _("Object ID"),
        help_text=_(
            "Waarde van de eigenschap die het object identificeert, bijvoorbeeld: '123456788'."
        ),
        max_length=200,
        blank=False,
    )
    actoridentifcator_register = models.CharField(
        _("Object ID"),
        help_text=_(
            "Binnen het landschap van registers unieke omschrijving van het register waarin "
            "het object is geregistreerd, bijvoorbeeld: 'BRP'."
        ),
        max_length=200,
        blank=False,
    )

    actoridentifcator = GegevensGroepType(
        {
            "objecttype": actoridentifcator_objecttype,
            "soort object id": actoridentifcator_soort_object_id,
            "object id": actoridentifcator_object_id,
            "register": actoridentifcator_register,
        }
    )

    class Meta:
        abstract = True
