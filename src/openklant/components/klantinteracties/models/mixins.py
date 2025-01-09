from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from openklant.utils.validators import validate_country


class BezoekadresMixin(models.Model):
    # TODO: Check if this is correct.
    bezoekadres_nummeraanduiding_id = models.CharField(
        _("nummeraanduiding ID"),
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
            "ISO 3166-code die het land (buiten Nederland) aangeeft alwaar de ingeschrevene verblijft."
        ),
        validators=[
            MinLengthValidator(limit_value=2),
            validate_country,
        ],
        max_length=2,
        blank=True,
    )

    bezoekadres = GegevensGroepType(
        {
            "nummeraanduiding_id": bezoekadres_nummeraanduiding_id,
            "adresregel_1": bezoekadres_adresregel1,
            "adresregel_2": bezoekadres_adresregel2,
            "adresregel_3": bezoekadres_adresregel3,
            "land": bezoekadres_land,
        },
        optional=(
            "nummeraanduiding_id",
            "adresregel_1",
            "adresregel_2",
            "adresregel_3",
            "land",
        ),
    )

    class Meta:
        abstract = True


class CorrespondentieadresMixin(models.Model):
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
            "ISO 3166-code die het land (buiten Nederland) aangeeft alwaar de ingeschrevene verblijft."
        ),
        validators=[
            MinLengthValidator(limit_value=2),
            validate_country,
        ],
        max_length=2,
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
        optional=(
            "nummeraanduiding_id",
            "adresregel_1",
            "adresregel_2",
            "adresregel_3",
            "land",
        ),
    )

    class Meta:
        abstract = True


class ContactnaamMixin(models.Model):
    contactnaam_voorletters = models.CharField(
        _("voorletters"),
        help_text=_(
            "Een afkorting van de voornamen. Meestal de beginletter, maar in sommige gevallen "
            "de beginletter gecombineerd met de tweede letter van een voornaam."
        ),
        max_length=10,
        blank=True,
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

    contactnaam = GegevensGroepType(
        {
            "voorletters": contactnaam_voorletters,
            "voornaam": contactnaam_voornaam,
            "voorvoegsel_achternaam": contactnaam_voorvoegsel_achternaam,
            "achternaam": contactnaam_achternaam,
        },
        optional=(
            "voorletters",
            "voornaam",
            "voorvoegsel_achternaam",
            "achternaam",
        ),
    )

    class Meta:
        abstract = True

    def get_full_name(self):
        name_components = [
            self.contactnaam_voornaam,
            self.contactnaam_voorvoegsel_achternaam,
            self.contactnaam_achternaam,
        ]

        return " ".join(component for component in name_components if component)
