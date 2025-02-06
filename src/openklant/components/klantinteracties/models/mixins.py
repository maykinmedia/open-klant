from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from openklant.utils.validators import (
    validate_bag_id,
    validate_country,
    validate_postal_code,
)


class BezoekadresMixin(models.Model):
    bezoekadres_nummeraanduiding_id = models.CharField(
        _("nummeraanduiding ID"),
        help_text=_(
            "Identificatie van het adres bij de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=16,
        validators=[validate_bag_id],
        blank=True,
    )
    bezoekadres_straatnaam = models.CharField(
        _("straatnaam"),
        help_text=_(
            "Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    bezoekadres_huisnummer = models.IntegerField(
        _("huisnummer"),
        help_text=_(
            "Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        validators=[MinValueValidator(1), MaxValueValidator(99999)],
        blank=True,
        null=True,
    )
    bezoekadres_huisnummertoevoeging = models.CharField(
        _("huisnummertoevoeging"),
        help_text=_(
            "Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        max_length=20,
        blank=True,
        null=True,
    )
    bezoekadres_postcode = models.CharField(
        _("postcode"),
        help_text=_(
            "Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        validators=[validate_postal_code],
        max_length=6,
        blank=True,
        null=True,
    )
    bezoekadres_stad = models.CharField(
        _("stad"),
        help_text=_(
            "Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        max_length=255,
        blank=True,
        null=True,
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
            "straatnaam": bezoekadres_straatnaam,
            "huisnummer": bezoekadres_huisnummer,
            "huisnummertoevoeging": bezoekadres_huisnummertoevoeging,
            "postcode": bezoekadres_postcode,
            "stad": bezoekadres_stad,
            "adresregel_1": bezoekadres_adresregel1,
            "adresregel_2": bezoekadres_adresregel2,
            "adresregel_3": bezoekadres_adresregel3,
            "land": bezoekadres_land,
        },
        optional=(
            "nummeraanduiding_id",
            "straatnaam",
            "huisnummer",
            "huisnummertoevoeging",
            "postcode",
            "stad",
            "adresregel_1",
            "adresregel_2",
            "adresregel_3",
            "land",
        ),
    )

    class Meta:
        abstract = True


class CorrespondentieadresMixin(models.Model):
    correspondentieadres_nummeraanduiding_id = models.CharField(
        _("nummeraanduiding ID"),
        help_text=_(
            "Identificatie van het adres bij de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=16,
        validators=[validate_bag_id],
        blank=True,
    )
    correspondentieadres_straatnaam = models.CharField(
        _("straatnaam"),
        help_text=_(
            "Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    correspondentieadres_huisnummer = models.IntegerField(
        _("huisnummer"),
        help_text=_(
            "Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        validators=[MinValueValidator(1), MaxValueValidator(99999)],
        blank=True,
        null=True,
    )
    correspondentieadres_huisnummertoevoeging = models.CharField(
        _("huisnummertoevoeging"),
        help_text=_(
            "Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        max_length=20,
        blank=True,
        null=True,
    )
    correspondentieadres_postcode = models.CharField(
        _("postcode"),
        help_text=_(
            "Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        validators=[validate_postal_code],
        max_length=6,
        blank=True,
        null=True,
    )
    correspondentieadres_stad = models.CharField(
        _("stad"),
        help_text=_(
            "Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
        ),
        max_length=255,
        blank=True,
        null=True,
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
            "straatnaam": correspondentieadres_straatnaam,
            "huisnummer": correspondentieadres_huisnummer,
            "huisnummertoevoeging": correspondentieadres_huisnummertoevoeging,
            "postcode": correspondentieadres_postcode,
            "stad": correspondentieadres_stad,
            "adresregel_1": correspondentieadres_adresregel1,
            "adresregel_2": correspondentieadres_adresregel2,
            "adresregel_3": correspondentieadres_adresregel3,
            "land": correspondentieadres_land,
        },
        optional=(
            "nummeraanduiding_id",
            "straatnaam",
            "huisnummer",
            "huisnummertoevoeging",
            "postcode",
            "stad",
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
