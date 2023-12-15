from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.klantinteracties.models.actoren import Actor
from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Bijlage,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.klantinteracties.models.partijen import (
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
)


def actor_is_valid_instance(value):
    if not isinstance(value, Actor):
        raise serializers.ValidationError(_("Actor object bestaat niet."))


def actor_exists(value):
    try:
        Actor.objects.get(uuid=str(value))
    except Actor.DoesNotExist:
        raise serializers.ValidationError(_("Actor object bestaat niet."))


def betrokkene_exists(value):
    try:
        Betrokkene.objects.get(uuid=str(value))
    except Betrokkene.DoesNotExist:
        raise serializers.ValidationError(_("Betrokkene object bestaat niet."))


def bijlage_exists(value):
    try:
        Bijlage.objects.get(uuid=str(value))
    except Bijlage.DoesNotExist:
        raise serializers.ValidationError(_("Bijlage object bestaat niet."))


def contactpersoon_exists(value):
    try:
        Contactpersoon.objects.get(id=int(value))
    except Contactpersoon.DoesNotExist:
        raise serializers.ValidationError(_("Contactpersoon object bestaat niet."))


def digitaal_adres_exists(value):
    try:
        DigitaalAdres.objects.get(uuid=str(value))
    except DigitaalAdres.DoesNotExist:
        raise serializers.ValidationError(_("DigitaalAdres object bestaat niet."))


def internetaak_exists(value):
    try:
        InterneTaak.objects.get(uuid=str(value))
    except InterneTaak.DoesNotExist:
        raise serializers.ValidationError(_("InterneTaak object bestaat niet."))


def klantcontact_exists(value):
    try:
        Klantcontact.objects.get(uuid=str(value))
    except Klantcontact.DoesNotExist:
        raise serializers.ValidationError(_("Klantcontact object bestaat niet."))


def onderwerpobject_exists(value):
    try:
        Onderwerpobject.objects.get(uuid=(str(value)))
    except Onderwerpobject.DoesNotExist:
        raise serializers.ValidationError(_("Onderwerpobject object bestaat niet."))


def organisatie_exists(value):
    try:
        Organisatie.objects.get(id=int(value))
    except Organisatie.DoesNotExist:
        raise serializers.ValidationError(_("Organisatie object bestaat niet."))


def partij_is_valid_instance(value):
    if not isinstance(value, Partij):
        raise serializers.ValidationError(_("Partij object bestaat niet."))


def partij_is_organisatie(value):
    # Validate if partij intance exists.
    partij_exists(value)

    partij = Partij.objects.get(uuid=str(value))
    if partij.soort_partij != SoortPartij.organisatie:
        raise serializers.ValidationError(
            _("Partij object moet het soort 'organisatie' hebben.")
        )


def partij_exists(value):
    try:
        Partij.objects.get(uuid=str(value))
    except Partij.DoesNotExist:
        raise serializers.ValidationError(_("Partij object bestaat niet."))


def partij_identificator_exists(value):
    try:
        PartijIdentificator.objects.get(uuid=str(value))
    except PartijIdentificator.DoesNotExist:
        raise serializers.ValidationError(_("PartijIdentificator object bestaat niet."))
