from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.klantinteracties.models.actoren import Actor
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Klantcontact,
)
from openklant.components.klantinteracties.models.partijen import Organisatie, Partij


def actor_exists(value):
    try:
        Actor.objects.get(uuid=str(value))
    except Actor.DoesNotExist:
        raise serializers.ValidationError(_("Actor object doesn't exist."))


def betrokkene_exists(value):
    try:
        Betrokkene.objects.get(uuid=str(value))
    except Betrokkene.DoesNotExist:
        raise serializers.ValidationError(_("Betrokkene object doesn't exist."))


def digitaal_adres_exists(value):
    try:
        DigitaalAdres.objects.get(uuid=str(value))
    except DigitaalAdres.DoesNotExist:
        raise serializers.ValidationError(_("DigitaalAdres object doesn't exist."))


def klantcontact_exists(value):
    try:
        Klantcontact.objects.get(uuid=str(value))
    except Klantcontact.DoesNotExist:
        raise serializers.ValidationError(_("Klantcontact object doesn't exist."))


def organisatie_exists(value):
    try:
        Organisatie.objects.get(id=str(value))
    except Organisatie.DoesNotExist:
        raise serializers.ValidationError(_("Organisatie object doesn't exist."))


def partij_exists(value):
    try:
        Partij.objects.get(uuid=str(value))
    except Partij.DoesNotExist:
        raise serializers.ValidationError(_("Partij object doesn't exist."))
