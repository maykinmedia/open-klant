from django.utils.translation import gettext_lazy as _

from .abc import AbstractIndicatieActiefModel
from .extern_register import ExternRegister
from .land import Land

__all__ = [
    "ExternRegister",
    "Kanaal",
    "Land",
    "SoortDigitaalAdres",
    "SoortObject",
    "SoortObjectid",
    "Taal",
]


class Kanaal(AbstractIndicatieActiefModel):
    """Kanalen die personen en organisaties kunnen gebruiken
    voor contact met de gemeente en vice versa."""

    class Meta(AbstractIndicatieActiefModel.Meta):
        verbose_name = _("kanaal")
        verbose_name_plural = _("kanalen")


class SoortDigitaalAdres(AbstractIndicatieActiefModel):
    """Soorten digitale adressen die personen en organisaties kunnen gebruiken
    voor contact met de gemeente en vice versa."""

    class Meta(AbstractIndicatieActiefModel.Meta):
        verbose_name = _("soort digitaal adres")
        verbose_name_plural = _("soorten digitaal adres")


class SoortObject(AbstractIndicatieActiefModel):
    """Typen objecten waarnaar vanuit het klantinteractiesregister
    relaties kunnen worden gelegd."""

    class Meta(AbstractIndicatieActiefModel.Meta):
        verbose_name = _("soort object")
        verbose_name_plural = _("soorten object")


class SoortObjectid(AbstractIndicatieActiefModel):
    """Identificatiesystemen en de registers waarin volgens deze systemen
    te identificeren objecten gevonden kunnen worden."""

    class Meta(AbstractIndicatieActiefModel.Meta):
        verbose_name = _("soort objectid")
        verbose_name_plural = _("soorten objectid")


class Taal(AbstractIndicatieActiefModel):
    """Talen die personen en organisaties kunnen gebruiken
    bij contact met de gemeente en vice versa."""

    class Meta(AbstractIndicatieActiefModel.Meta):
        verbose_name = _("taal")
        verbose_name_plural = _("talen")
