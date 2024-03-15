from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Taakstatus(TextChoices):
    te_verwerken = "te_verwerken", _("Te verwerken.")
    verwerkt = "verwerkt", _("Verwerkt")


class SoortBezoekadres(TextChoices):
    binnenlands_adres = "binnenlands_adres", _("Binnenlands adres")
    buitenlands_adres = "buitenlands_adres", _("Buitenlands adres")


class AanduidingBijHuisnummer(TextChoices):
    bij = "bij", _("Bij")
    tegenover = "tegenover", _("Tegenover")


class SoortCorrespondentieadres(TextChoices):
    postbusnummer = "postbusnummer", _("Postbusnummer")
    antwoordnummer = "antwoordnummer", _("Antwoordnummer")
    binnenlands_adres = "binnenlands_adres", _("Binnenlands adres")
    buitenlands_adres = "buitenlands_adres", _("Buitenlands adres")


class SoortActor(TextChoices):
    medewerker = "medewerker", _("Medewerker")
    geautomatiseerde_actor = "geautomatiseerde_actor", _("Geautomatiseerde actor")
    organisatorische_eenheid = "organisatorische_eenheid", _("Organisatorische eenheid")


class SoortInhoudsdeel(TextChoices):
    informatieobject = "informatieobject", _("Informatieobject")
    overig_object = "overig_object", _("Overig object")
    tekst = "tekst", _("Tekst")


class SoortPartij(TextChoices):
    persoon = "persoon", _("Persoon")
    organisatie = "organisatie", _("Organisatie")
    contactpersoon = "contactpersoon", _("Contactpersoon")


class Klantcontrol(TextChoices):
    vertegenwoordiger = "vertegenwoordiger", _("Vertegenwoordiger")
    klant = "klant", _("Klant")
