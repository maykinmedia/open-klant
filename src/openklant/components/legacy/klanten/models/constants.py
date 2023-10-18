from django.utils.translation import gettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class GeslachtsAanduiding(DjangoChoices):
    man = ChoiceItem("m", _("Man"))
    vrouw = ChoiceItem("v", _("Vrouw"))
    onbekend = ChoiceItem("o", _("Onbekend"))


class KlantType(DjangoChoices):
    natuurlijk_persoon = ChoiceItem("natuurlijk_persoon", _("Natuurlijk persoon"))
    niet_natuurlijk_persoon = ChoiceItem(
        "niet_natuurlijk_persoon", _("Niet-natuurlijk persoon")
    )
    vestiging = ChoiceItem("vestiging", _("Vestiging"))


# TODO: Copied from Zaken API, move to common
class SoortRechtsvorm(DjangoChoices):
    besloten_vennootschap = ChoiceItem(
        "besloten_vennootschap", _("Besloten Vennootschap")
    )
    cooperatie_europees_economische_samenwerking = ChoiceItem(
        "cooperatie_europees_economische_samenwerking",
        _("Cooperatie, Europees Economische Samenwerking"),
    )
    europese_cooperatieve_vennootschap = ChoiceItem(
        "europese_cooperatieve_venootschap", _("Europese Cooperatieve Venootschap")
    )
    europese_naamloze_vennootschap = ChoiceItem(
        "europese_naamloze_vennootschap", _("Europese Naamloze Vennootschap")
    )
    kerkelijke_organisatie = ChoiceItem(
        "kerkelijke_organisatie", _("Kerkelijke Organisatie")
    )
    naamloze_vennootschap = ChoiceItem(
        "naamloze_vennootschap", _("Naamloze Vennootschap")
    )
    onderlinge_waarborg_maatschappij = ChoiceItem(
        "onderlinge_waarborg_maatschappij", _("Onderlinge Waarborg Maatschappij")
    )
    overig_privaatrechtelijke_rechtspersoon = ChoiceItem(
        "overig_privaatrechtelijke_rechtspersoon",
        _("Overig privaatrechtelijke rechtspersoon"),
    )
    stichting = ChoiceItem("stichting", _("Stichting"))
    vereniging = ChoiceItem("vereniging", _("Vereniging"))
    vereniging_van_eigenaars = ChoiceItem(
        "vereniging_van_eigenaars", _("Vereniging van Eigenaars")
    )
    publiekrechtelijke_rechtspersoon = ChoiceItem(
        "publiekrechtelijke_rechtspersoon", _("Publiekrechtelijke Rechtspersoon")
    )
    vennootschap_onder_firma = ChoiceItem(
        "vennootschap_onder_firma", _("Vennootschap onder Firma")
    )
    maatschap = ChoiceItem("maatschap", _("Maatschap"))
    rederij = ChoiceItem("rederij", _("Rederij"))
    commanditaire_vennootschap = ChoiceItem(
        "commanditaire_vennootschap", _("Commanditaire vennootschap")
    )
    kapitaalvennootschap_binnen_eer = ChoiceItem(
        "kapitaalvennootschap_binnen_eer", _("Kapitaalvennootschap binnen EER")
    )
    overige_buitenlandse_rechtspersoon_vennootschap = ChoiceItem(
        "overige_buitenlandse_rechtspersoon_vennootschap",
        _("Overige buitenlandse rechtspersoon vennootschap"),
    )
    kapitaalvennootschap_buiten_eer = ChoiceItem(
        "kapitaalvennootschap_buiten_eer", _("Kapitaalvennootschap buiten EER")
    )
