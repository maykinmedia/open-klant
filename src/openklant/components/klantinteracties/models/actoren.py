import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import SoortActor
from .mixins import ActorIdentifcatorMixin


class Actor(ActorIdentifcatorMixin):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de actor."),
    )
    # TODO: add FK to Interne Taak
    naam = models.CharField(
        _("Naam"),
        help_text=_("Naam van de actor."),
        max_length=200,
    )
    soort_actor = models.CharField(
        _("Soort actor"),
        help_text=_("Geeft aan van welke specifieke soort actor sprake is."),
        choices=SoortActor.choices,
        max_length=24,
    )
    indicatie_actief = models.BooleanField(
        _("Indicatie actief"),
        help_text=_(
            "Geeft aan of aan de actor nog betrokken mag worden bij nieuwe klantcontacten. "
            "Voor niet-actieve is dit niet toegestaan."
        ),
        blank=False,
    )

    class Meta:
        verbose_name = _("actor")
        verbose_name_plural = _("actoren")

        def __str__(self):
            return self.naam


class GeautomatiseerdeActor(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        verbose_name=_("Actor"),
        related_name="geautomatiseerde_actor",
        help_text=_("'GeautomatiseerdeActor' was 'Actor'"),
        null=False,
    )
    functie = models.CharField(
        _("Functie"),
        help_text=_(
            "Functie van de geautomatiseerde actor of beschrijving van de werkzaamheden die deze uitvoert."
        ),
        max_length=40,
    )
    omschrijving = models.CharField(
        _("Omschrijving"),
        help_text=_("Omschrijving van de geautomatiseerde actor."),
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = _("geautomatiseerde actor")
        verbose_name_plural = _("geautomatiseerde actoren")

        def __str__(self):
            return self.functie


class Medewerker(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        verbose_name=_("Actor"),
        related_name="medewerker",
        help_text=_("'GeautomatiseerdeActor' was 'Actor'"),
        null=False,
    )
    functie = models.CharField(
        _("Functie"),
        help_text=_(
            "Functie van de geautomatiseerde actor of beschrijving van de werkzaamheden die deze uitvoert."
        ),
        max_length=40,
    )
    email = models.EmailField(
        _("email address"),
        help_text=_(
            "Elektronisch postadres waaronder de MEDEWERKER in de regel bereikbaar is."
        ),
        blank=True,
    )
    telefoonnummer = models.CharField(
        _("Telefoonnummer"),
        help_text=_(
            "Telefoonnummer waaronder de MEDEWERKER in de regel bereikbaar is."
        ),
        max_length=20,
    )

    class Meta:
        verbose_name = _("medewerker")
        verbose_name_plural = _("Mederwerkers")

        def __str__(self):
            return self.functie


class OrganisatorischeEenheid(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        verbose_name=_("Actor"),
        related_name="organisatorische_eenheid",
        help_text=_("'GeautomatiseerdeActor' was 'Actor'"),
        null=False,
    )
    omschrijving = models.CharField(
        _("Omschrijving"),
        help_text=_("Omschrijving van de geautomatiseerde actor."),
        max_length=200,
        blank=True,
    )
    email = models.EmailField(
        _("email address"),
        help_text=_(
            "Elektronisch postadres waaronder de MEDEWERKER in de regel bereikbaar is."
        ),
        blank=True,
    )
    faxnummer = models.CharField(
        _("Faxnummer"),
        help_text=_(
            "Faxnummer waaronder de organisatorische eenheid in de regel bereikbaar is."
        ),
        max_length=20,
    )
    telefoonnummer = models.CharField(
        _("Telefoonnummer"),
        help_text=_(
            "Telefoonnummer waaronder de MEDEWERKER in de regel bereikbaar is."
        ),
        max_length=20,
    )

    class Meta:
        verbose_name = _("organisatorische eenheid")

        def __str__(self):
            return self.omschrijving
