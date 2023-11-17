from django.core.validators import MinLengthValidator, validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType


class AdresMixin(models.Model):
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

    adres = GegevensGroepType(
        {
            "adresregel_1": adres_adresregel1,
            "adresregel_2": adres_adresregel2,
            "adresregel_3": adres_adresregel3,
            "land": adres_land,
        },
    )

    class Meta:
        abstract = True


class LandMixin(models.Model):
    land_code = models.CharField(
        _("code"),
        help_text=_("adres code"),
        blank=True,
        max_length=255,
    )

    land = GegevensGroepType(
        {
            "code": land_code,
        },
    )

    class Meta:
        abstract = True
