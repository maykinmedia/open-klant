from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class GeslachtsAanduiding(TextChoices):
    man = "m", _("Man")
    vrouw = "v", _("Vrouw")
    onbekend = "o", _("Onbekend")


class KlantType(TextChoices):
    natuurlijk_persoon = "natuurlijk_persoon", _("Natuurlijk persoon")
    niet_natuurlijk_persoon = "niet_natuurlijk_persoon", _("Niet-natuurlijk persoon")
    vestiging = "vestiging", _("Vestiging")


# TODO: Copied from Zaken API, move to common
class SoortRechtsvorm(TextChoices):
    besloten_vennootschap = "besloten_vennootschap", _("Besloten Vennootschap")
    cooperatie_europees_economische_samenwerking = (
        "cooperatie_europees_economische_samenwerking",
        _("Cooperatie, Europees Economische Samenwerking"),
    )
    europese_cooperatieve_vennootschap = "europese_cooperatieve_venootschap", _(
        "Europese Cooperatieve Venootschap"
    )
    europese_naamloze_vennootschap = "europese_naamloze_vennootschap", _(
        "Europese Naamloze Vennootschap"
    )
    kerkelijke_organisatie = "kerkelijke_organisatie", _("Kerkelijke Organisatie")
    naamloze_vennootschap = "naamloze_vennootschap", _("Naamloze Vennootschap")
    onderlinge_waarborg_maatschappij = "onderlinge_waarborg_maatschappij", _(
        "Onderlinge Waarborg Maatschappij"
    )
    overig_privaatrechtelijke_rechtspersoon = (
        "overig_privaatrechtelijke_rechtspersoon",
        _("Overig privaatrechtelijke rechtspersoon"),
    )
    stichting = "stichting", _("Stichting")
    vereniging = "vereniging", _("Vereniging")
    vereniging_van_eigenaars = "vereniging_van_eigenaars", _("Vereniging van Eigenaars")
    publiekrechtelijke_rechtspersoon = "publiekrechtelijke_rechtspersoon", _(
        "Publiekrechtelijke Rechtspersoon"
    )
    vennootschap_onder_firma = "vennootschap_onder_firma", _("Vennootschap onder Firma")
    maatschap = "maatschap", _("Maatschap")
    rederij = "rederij", _("Rederij")
    commanditaire_vennootschap = "commanditaire_vennootschap", _(
        "Commanditaire vennootschap"
    )
    kapitaalvennootschap_binnen_eer = "kapitaalvennootschap_binnen_eer", _(
        "Kapitaalvennootschap binnen EER"
    )
    overige_buitenlandse_rechtspersoon_vennootschap = (
        "overige_buitenlandse_rechtspersoon_vennootschap",
        _("Overige buitenlandse rechtspersoon vennootschap"),
    )
    kapitaalvennootschap_buiten_eer = "kapitaalvennootschap_buiten_eer", _(
        "Kapitaalvennootschap buiten EER"
    )
