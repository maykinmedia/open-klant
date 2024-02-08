import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from openklant.utils.validators import validate_phone_number

from .constants import SoortActor
from .mixins import ObjectidentificatorMixin


class Actor(ObjectidentificatorMixin):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de actor."),
    )
    naam = models.CharField(
        _("naam"),
        help_text=_("Naam van de actor."),
        max_length=200,
    )
    soort_actor = models.CharField(
        _("soort actor"),
        help_text=_("Geeft aan van welke specifieke soort actor sprake is."),
        choices=SoortActor.choices,
        max_length=24,
    )
    indicatie_actief = models.BooleanField(
        _("indicatie actief"),
        help_text=_(
            "Geeft aan of aan de actor nog betrokken mag worden bij nieuwe klantcontacten. "
            "Voor niet-actieve is dit niet toegestaan."
        ),
        default=True,
    )

    class Meta:
        verbose_name = _("actor")
        verbose_name_plural = _("actoren")

    def __str__(self):
        return self.naam


class ActorKlantcontact(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        help_text=_("Unieke (technische) identificatiecode van de actor klantcontact."),
    )
    actor = models.ForeignKey(
        "klantinteracties.Actor",
        on_delete=models.CASCADE,
        verbose_name=_("actor"),
        help_text=_("De gekoppelde 'Actor'."),
    )
    klantcontact = models.ForeignKey(
        "klantinteracties.Klantcontact",
        on_delete=models.CASCADE,
        verbose_name=_("klantcontact"),
        help_text=_("De gekoppelde 'Klantcontact'."),
    )

    class Meta:
        verbose_name = _("actor klantcontact")
        verbose_name_plural = _("actor klantcontacten")
        unique_together = (
            "actor",
            "klantcontact",
        )

    def __str__(self):
        return f"{self.actor.naam} - {self.klantcontact.nummer}"


class GeautomatiseerdeActor(models.Model):
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,
        verbose_name=_("Actor"),
        help_text=_("'GeautomatiseerdeActor' was 'Actor'"),
    )
    functie = models.CharField(
        _("functie"),
        help_text=_(
            "Functie van de geautomatiseerde actor of beschrijving van de werkzaamheden die deze uitvoert."
        ),
        max_length=40,
    )
    omschrijving = models.CharField(
        _("omschrijving"),
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
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,
        verbose_name=_("actor"),
        help_text=_("'GeautomatiseerdeActor' was 'Actor'"),
    )
    functie = models.CharField(
        _("functie"),
        help_text=_(
            "Functie van de geautomatiseerde actor of beschrijving van de werkzaamheden die deze uitvoert."
        ),
        max_length=40,
    )
    emailadres = models.EmailField(
        _("e-mailadres"),
        help_text=_(
            "Elektronisch postadres waaronder de MEDEWERKER in de regel bereikbaar is."
        ),
        blank=True,
    )
    telefoonnummer = models.CharField(
        _("telefoonnummer"),
        help_text=_(
            "Telefoonnummer waaronder de MEDEWERKER in de regel bereikbaar is."
        ),
        validators=[validate_phone_number],
        max_length=20,
    )

    class Meta:
        verbose_name = _("medewerker")
        verbose_name_plural = _("mederwerkers")

    def __str__(self):
        return self.functie


class OrganisatorischeEenheid(models.Model):
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,
        verbose_name=_("actor"),
        help_text=_("'GeautomatiseerdeActor' was 'Actor'"),
    )
    omschrijving = models.CharField(
        _("omschrijving"),
        help_text=_("Omschrijving van de geautomatiseerde actor."),
        max_length=200,
        blank=True,
    )
    emailadres = models.EmailField(
        _("e-mailadres"),
        help_text=_(
            "Elektronisch postadres waaronder de MEDEWERKER in de regel bereikbaar is."
        ),
        blank=True,
    )
    faxnummer = models.CharField(
        _("faxnummer"),
        help_text=_(
            "Faxnummer waaronder de organisatorische eenheid in de regel bereikbaar is."
        ),
        max_length=20,
    )
    telefoonnummer = models.CharField(
        _("telefoonnummer"),
        help_text=_(
            "Telefoonnummer waaronder de MEDEWERKER in de regel bereikbaar is."
        ),
        validators=[validate_phone_number],
        max_length=20,
    )

    class Meta:
        verbose_name = _("organisatorische eenheid")

    def __str__(self):
        return self.omschrijving
