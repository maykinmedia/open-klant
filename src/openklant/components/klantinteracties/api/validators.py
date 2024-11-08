from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, qs_filter

from openklant.components.klantinteracties.constants import SoortDigitaalAdres
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
    Categorie,
    CategorieRelatie,
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
)
from openklant.components.klantinteracties.models.rekeningnummers import Rekeningnummer


class FKUniqueTogetherValidator(UniqueTogetherValidator):
    def filter_queryset(self, attrs, queryset, serializer):
        """
        Filter the queryset to all instances matching the given attributes.
        """
        sources = [serializer.fields[field_name].source for field_name in self.fields]

        if serializer.instance is not None:  # noqa
            for source in sources:
                if source not in attrs:
                    attrs[source] = getattr(serializer.instance, source)

        # changed the way we generate filter_kwargs
        # to either filter on model instance or model_uuid instance
        filter_kwargs = {}
        for source in sources:
            if isinstance(attrs[source], models.Model):
                filter_kwargs[source] = attrs[source]
                continue
            filter_kwargs[source + "__uuid"] = str(attrs[source]["uuid"])

        return qs_filter(queryset, **filter_kwargs)


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


def categorie_relatie_exists(value):
    try:
        CategorieRelatie.objects.get(uuid=str(value))
    except CategorieRelatie.DoesNotExist:
        raise serializers.ValidationError(_("CategorieRelatie object bestaat niet."))


def categorie_exists(value):
    try:
        Categorie.objects.get(uuid=str(value))
    except Categorie.DoesNotExist:
        raise serializers.ValidationError(_("Categorie object bestaat niet."))


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


def Rekeningnummer_exists(value):
    try:
        Rekeningnummer.objects.get(uuid=str(value))
    except Rekeningnummer.DoesNotExist:
        raise serializers.ValidationError(_("Rekeningnummer object bestaat niet."))


class OptionalEmailValidator(EmailValidator):
    """
    EmailValidator for SoortDigitaalAdres that only attempts to validate if
    `SoortDigitaalAdres` is `email`
    """

    def __call__(self, value: str, soort_digitaal_adres: str):
        if soort_digitaal_adres == SoortDigitaalAdres.email:
            super().__call__(value)
