from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from openklant.components.utils.mixins import create_prefixed_mixin

BezoekadresMixin = create_prefixed_mixin("bezoekadres")
CorrespondentieadresMixin = create_prefixed_mixin("correspondentieadres")


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
