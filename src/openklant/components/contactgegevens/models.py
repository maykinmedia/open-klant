import uuid

from django.core.validators import MinLengthValidator, validate_integer
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_loose_fk.fields import FkOrURLField
from django_loose_fk.loaders import RequestsLoader

from openklant.components.contactgegevens.constants import GeslachtChoices
from openklant.components.contactgegevens.mixins import AdresMixin
from openklant.components.klantinteracties.models.partijen import PartijIdentificator


class Contactgegevens(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de contact gegevens."),
    )
    _partij_identificator = models.ForeignKey(
        PartijIdentificator,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    _partij_identificator_url = models.URLField(blank=True)
    partij_identificator = FkOrURLField(
        fk_field="_partij_identificator",
        url_field="_partij_identificator_url",
        loader=RequestsLoader(),
    )

    class Meta:
        verbose_name = _("contactgegevens")
        verbose_name_plural = _("contactgegevens")


class Organisatie(AdresMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de organisatie."),
    )
    contactgegevens = models.ForeignKey(
        Contactgegevens,
        verbose_name=_("contactgegevens"),
        help_text=_("De contact gegevens van de huidige organisatie."),
        on_delete=models.CASCADE,
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
    contactgegevens = models.ForeignKey(
        Contactgegevens,
        verbose_name=_("contactgegevens"),
        help_text=_("De contact gegevens van het huidige persoon."),
        on_delete=models.CASCADE,
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

    class Meta:
        verbose_name = _("persoon")
        verbose_name_plural = _("personen")

    def __str__(self):
        return f"{self.voornamen} {self.voorvoegsel} {self.geslachtsnaam}"
