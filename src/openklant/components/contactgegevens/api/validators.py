from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openklant.components.contactgegevens.models import (
    Contactgegevens,
    Organisatie,
    Persoon,
)


def contactgegevens_exists(value):
    try:
        Contactgegevens.objects.get(uuid=str(value))
    except Contactgegevens.DoesNotExist:
        raise serializers.ValidationError(_("Contactgegevens object doesn't exist."))


def organisatie_exists(value):
    try:
        Organisatie.objects.get(uuid=str(value))
    except Organisatie.DoesNotExist:
        raise serializers.ValidationError(_("Organisatie object doesn't exist."))


def persoon_exists(value):
    try:
        Persoon.objects.get(uuid=str(value))
    except Persoon.DoesNotExist:
        raise serializers.ValidationError(_("Persoon object doesn't exist."))
