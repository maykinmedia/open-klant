from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class GeslachtsAanduiding(DjangoChoices):
    man = ChoiceItem("m", "Man")
    vrouw = ChoiceItem("v", "Vrouw")
    onbekend = ChoiceItem("o", "Onbekend")


class KlantType(DjangoChoices):
    natuurlijk_persoon = ChoiceItem("natuurlijk_persoon", "Natuurlijk persoon")
    niet_natuurlijk_persoon = ChoiceItem(
        "niet_natuurlijk_persoon", "Niet-natuurlijk persoon"
    )
    vestiging = ChoiceItem("vestiging", "Vestiging")


# TODO: Copied from Zaken API, move to common
class SoortRechtsvorm(DjangoChoices):
    besloten_vennootschap = ChoiceItem("besloten_vennootschap", "Besloten Vennootschap")
    cooperatie_europees_economische_samenwerking = ChoiceItem(
        "cooperatie_europees_economische_samenwerking",
        "Cooperatie, Europees Economische Samenwerking",
    )
    europese_cooperatieve_vennootschap = ChoiceItem(
        "europese_cooperatieve_venootschap", "Europese Cooperatieve Venootschap"
    )
    europese_naamloze_vennootschap = ChoiceItem(
        "europese_naamloze_vennootschap", "Europese Naamloze Vennootschap"
    )
    kerkelijke_organisatie = ChoiceItem(
        "kerkelijke_organisatie", "Kerkelijke Organisatie"
    )
    naamloze_vennootschap = ChoiceItem("naamloze_vennootschap", "Naamloze Vennootschap")
    onderlinge_waarborg_maatschappij = ChoiceItem(
        "onderlinge_waarborg_maatschappij", "Onderlinge Waarborg Maatschappij"
    )
    overig_privaatrechtelijke_rechtspersoon = ChoiceItem(
        "overig_privaatrechtelijke_rechtspersoon",
        "Overig privaatrechtelijke rechtspersoon",
    )
    stichting = ChoiceItem("stichting", "Stichting")
    vereniging = ChoiceItem("vereniging", "Vereniging")
    vereniging_van_eigenaars = ChoiceItem(
        "vereniging_van_eigenaars", "Vereniging van Eigenaars"
    )
    publiekrechtelijke_rechtspersoon = ChoiceItem(
        "publiekrechtelijke_rechtspersoon", "Publiekrechtelijke Rechtspersoon"
    )
    vennootschap_onder_firma = ChoiceItem(
        "vennootschap_onder_firma", "Vennootschap onder Firma"
    )
    maatschap = ChoiceItem("maatschap", "Maatschap")
    rederij = ChoiceItem("rederij", "Rederij")
    commanditaire_vennootschap = ChoiceItem(
        "commanditaire_vennootschap", "Commanditaire vennootschap"
    )
    kapitaalvennootschap_binnen_eer = ChoiceItem(
        "kapitaalvennootschap_binnen_eer", "Kapitaalvennootschap binnen EER"
    )
    overige_buitenlandse_rechtspersoon_vennootschap = ChoiceItem(
        "overige_buitenlandse_rechtspersoon_vennootschap",
        "Overige buitenlandse rechtspersoon vennootschap",
    )
    kapitaalvennootschap_buiten_eer = ChoiceItem(
        "kapitaalvennootschap_buiten_eer", "Kapitaalvennootschap buiten EER"
    )
