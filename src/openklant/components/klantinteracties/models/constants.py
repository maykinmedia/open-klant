from django.utils.translation import gettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class Taakstatus(DjangoChoices):
    te_verwerken = ChoiceItem("te_verwerken", _("Het verzoek is afgehandeld."))
    verwerkt = ChoiceItem("verwerkt", _("Het verzoek ID buiten behandeling gesteld."))


class SoortBezoekadres(DjangoChoices):
    binnenlands_adres = ChoiceItem("binnenlands_adres", _("Binnenlands adres"))
    buitenlands_adres = ChoiceItem("binnenlands_adres", _("Buitenlands adres"))


class AanduidingBijHuisnummer(DjangoChoices):
    bij = ChoiceItem("bij", _("Bij"))
    tegenover = ChoiceItem("tegenover", _("Tegenover"))


class SoortCorrespondentieadres(DjangoChoices):
    postbusnummer = ChoiceItem("postbusnummer", _("Postbusnummer"))
    antwoordnummer = ChoiceItem("antwoordnummer", _("Antwoordnummer"))
    binnenlands_adres = ChoiceItem("binnenlands_adres", _("Binnenlands adres"))
    buitenlands_adres = ChoiceItem("buitenlands_adres", _("Buitenlands adres"))


class SoortActor(DjangoChoices):
    medewerker = ChoiceItem("medewerker", _("Medewerker"))
    geautomatiseerde_actor = ChoiceItem(
        "geautomatiseerde_actor", _("Geautomatiseerde actor")
    )
    organisatorische_eenheid = ChoiceItem(
        "organisatorische_eenheid", _("Organisatorische eenheid")
    )


class SoortInhoudsdeel(DjangoChoices):
    informatieobject = ChoiceItem("informatieobject", _("Informatieobject"))
    overig_object = ChoiceItem("overig_object", _("Overig object"))
    tekst = ChoiceItem("tekst", _("Tekst"))


class SoortPartij(DjangoChoices):
    persoon = ChoiceItem("persoon", _("Persoon"))
    organisatie = ChoiceItem("organisatie", _("Organisatie"))
    contactpersoon = ChoiceItem("contactpersoon", _("Contactpersoon"))


class Klantcontrol(DjangoChoices):
    vertegenwoordiger = ChoiceItem("vertegenwoordiger", _("Vertegenwoordiger"))
    klant = ChoiceItem("klant", _("Klant"))
