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


class AdresMixin(models.Model):
    adres_nummeraanduiding_id = models.CharField(
        _("nummeraanduiding ID"),
        help_text=_(
            "Identificatie van het adres bij de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=16,
        validators=[validate_bag_id],
        blank=True,
    )
    adres_straatnaam = models.CharField(
        _("straatnaam"),
        help_text=_("Straatnaam in het Basisregistratie Adressen en Gebouwen."),
        max_length=255,
        blank=True,
        null=True,
    )
    adres_huisnummer = models.IntegerField(
        _("huisnummer"),
        help_text=_("Huisnummer in het Basisregistratie Adressen en Gebouwen."),
        validators=[MinValueValidator(1), MaxValueValidator(99999)],
        blank=True,
        null=True,
    )
    adres_huisnummertoevoeging = models.CharField(
        _("huisnummertoevoeging"),
        help_text=_(
            "Huisnummertoevoeging in het Basisregistratie Adressen en Gebouwen."
        ),
        max_length=20,
        blank=True,
        null=True,
    )
    adres_postcode = models.CharField(
        _("postcode"),
        help_text=_("Postcode in het Basisregistratie Adressen en Gebouwen."),
        validators=[validate_postal_code],
        max_length=6,
        blank=True,
        null=True,
    )
    adres_stad = models.CharField(
        _("stad"),
        help_text=_("Stad in het Basisregistratie Adressen en Gebouwen."),
        max_length=255,
        blank=True,
        null=True,
    )
    adres_adresregel1 = models.CharField(
        _("adresregel 1"),
        help_text=_(
            "Eerste deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    adres_adresregel2 = models.CharField(
        _("adresregel 2"),
        help_text=_(
            "Tweede deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    adres_adresregel3 = models.CharField(
        _("adresregel 3"),
        help_text=_(
            "Derde deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
        ),
        max_length=80,
        blank=True,
    )
    adres_land = models.CharField(
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

    adres = GegevensGroepType(
        {
            "nummeraanduiding_id": adres_nummeraanduiding_id,
            "straatnaam": adres_straatnaam,
            "huisnummer": adres_huisnummer,
            "huisnummertoevoeging": adres_huisnummertoevoeging,
            "postcode": adres_postcode,
            "stad": adres_stad,
            "adresregel_1": adres_adresregel1,
            "adresregel_2": adres_adresregel2,
            "adresregel_3": adres_adresregel3,
            "land": adres_land,
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
