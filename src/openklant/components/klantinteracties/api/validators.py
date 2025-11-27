from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

import structlog
from dateutil import parser
from requests import RequestException
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, qs_filter
from zgw_consumers.client import build_client

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
from openklant.config.models import ReferentielijstenConfig
from openklant.utils.validators import validate_phone_number
from referentielijsten_client.client import ReferentielijstenClient

logger = structlog.get_logger(__name__)


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


class SoortDigitaalAdresValidator:
    def __call__(self, soort_digitaal_adres: SoortDigitaalAdres, value: str):
        match soort_digitaal_adres:
            case SoortDigitaalAdres.email:
                EmailValidator()(value)
            case SoortDigitaalAdres.telefoonnummer:
                validate_phone_number(value)
            case _:
                return


class InvalidReferentielijstenConfiguration(Exception):
    pass


class KanaalValidator:
    def is_valid_datetime(self, value):
        return parser.isoparse(value) if value else None

    def __call__(self, value: str):
        config = ReferentielijstenConfig.get_solo()
        if not config.enabled:
            return value

        if not config.service:
            logger.warning("missing_referentielijsten_service")
            raise InvalidReferentielijstenConfiguration(
                "`kanaal` validation using Referentielijsten API is enabled, but no service is configured."
            )

        try:
            client = build_client(
                service=config.service,
                client_factory=ReferentielijstenClient,
            )
            raw_items = client.get_cached_items_by_tabel_code(config.kanalen_tabel_code)

        except (RequestException, Exception):
            logger.error(
                "failed_to_fetch_kanalen_from_referentielijsten",
                exc_info=True,
            )
            raise ValidationError(
                "Failed to retrieve valid channels from the Referentielijsten API to validate `kanaal`."
            )

        if not raw_items:
            logger.warning(
                "no_kanalen_found_in_referentielijsten",
                tabel_code=config.kanalen_tabel_code,
            )
            raise ValidationError(
                "No channels to validate `kanaal` were found for the configured tabel_code in the Referentielijsten API."
            )

        now = datetime.now(timezone.utc)

        kanalen = []

        for item in raw_items:
            begin = item.get("begindatumGeldigheid")
            eind = item.get("einddatumGeldigheid")

            begin_dt = self.is_valid_datetime(begin)
            eind_dt = self.is_valid_datetime(eind)

            if begin_dt and now < begin_dt:
                continue
            if eind_dt and now >= eind_dt:
                continue
            if begin_dt and eind_dt and not (begin_dt <= now < eind_dt):
                continue

            code = item.get("code")
            if code:
                kanalen.append(code)

        if not kanalen:
            raise ValidationError(
                f"'{value}' is not a valid kanaal. Allowed values: {', '.join(kanalen)}"
            )

        if value not in kanalen:
            raise ValidationError(
                f"'{value}' is not a valid kanaal. Allowed values: {', '.join(kanalen)}"
            )

        return value
