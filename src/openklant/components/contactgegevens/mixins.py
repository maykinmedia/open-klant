from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from openklant.utils.validators import validate_bag_id, validate_country


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
            "adresregel_1": adres_adresregel1,
            "adresregel_2": adres_adresregel2,
            "adresregel_3": adres_adresregel3,
            "land": adres_land,
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
