import uuid

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from openklant.components.contactgegevens.constants import GeslachtChoices
from openklant.components.contactgegevens.mixins import AdresMixin
from openklant.utils.validators import validate_country


class Organisatie(AdresMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de organisatie."),
    )
    handelsnaam = models.CharField(
        _("handelsnaam"),
        help_text=_("De naam waaronder een bedrijf of vestiging handelt."),
        max_length=255,
    )
    oprichtingsdatum = models.DateField(
        _("oprichtingsdatum"),
        editable=True,
        null=True,
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst "
            "significante onderdeel. Een voorbeeld: 2022-02-21"
        ),
    )
    opheffingsdatum = models.DateField(
        _("opheffingsdatum"),
        editable=True,
        null=True,
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst "
            "significante onderdeel. Een voorbeeld: 2022-02-21"
        ),
    )
    land = models.CharField(
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

    class Meta:
        verbose_name = _("organisatie")
        verbose_name_plural = _("organisaties")

    def __str__(self):
        return self.handelsnaam


class Persoon(AdresMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van het persoon."),
    )
    geboortedatum = models.DateField(
        _("geboortedatum"),
        editable=True,
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst "
            "significante onderdeel. Een voorbeeld: 2022-02-21"
        ),
    )
    overlijdensdatum = models.DateField(
        _("overlijdensdatum"),
        editable=True,
        null=True,
        blank=True,
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst "
            "significante onderdeel. Een voorbeeld: 2022-02-21"
        ),
    )
    geslachtsnaam = models.CharField(
        _("geslachtsnaam"),
        help_text=_(
            "De (geslachts)naam waarvan de eventueel aanwezige voorvoegsels "
            "zijn afgesplitst. Gebruik van de wildcard is toegestaan bij invoer "
            "van ten minste 3 letters. Zoeken met tekstvelden is case-insensitive."
        ),
        max_length=200,
    )
    geslacht = models.CharField(
        _("geslacht"),
        choices=GeslachtChoices.choices,
        help_text=_(
            "Geeft aan dat de persoon een man of een vrouw is, "
            "of dat het geslacht (nog) onbekend is."
        ),
        max_length=1,
        blank=True,
    )
    voorvoegsel = models.CharField(
        _("voorvoegsel"),
        help_text=_(
            "Deel van de geslachtsnaam dat vooraf gaat aan de rest van de geslachtsnaam. "
            "Zoeken met tekstvelden is case-insensitive."
        ),
        max_length=10,
        blank=True,
    )
    voornamen = models.CharField(
        _("voornamen"),
        help_text=_(
            "De verzameling namen die, gescheiden door spaties, aan de geslachtsnaam "
            "voorafgaat. Gebruik van de wildcard is toegestaan. Zoeken met tekstvelden "
            "is case-insensitive."
        ),
        max_length=200,
        blank=True,
    )
    land = models.CharField(
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

    class Meta:
        verbose_name = _("persoon")
        verbose_name_plural = _("personen")

    def __str__(self):
        return f"{self.voornamen} {self.voorvoegsel} {self.geslachtsnaam}"
