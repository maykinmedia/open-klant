# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2024 Dimpact


import os
from dataclasses import fields as dataclass_fields
from typing import Any, Tuple
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.management import CommandError
from django.core.management.base import BaseCommand, CommandParser

from rest_framework.fields import URLValidator
from rest_framework.reverse import reverse_lazy

from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models import (
    DigitaalAdres,
    Partij,
)
from openklant.components.token.models import TokenAuth
from openklant.migration.client import Client
from openklant.migration.utils import (
    MIGRATION_TOKEN_IDENTIFIER,
    _generate_dummy_token,
    generate_jwt_token,
    logger,
)
from openklant.migration.v1.client import LegacyOpenKlantClient
from openklant.migration.v1.data import Klant
from openklant.migration.v2.client import OpenKlantClient

KLANT_FIELDS = {field.name: field for field in dataclass_fields(Klant)}

DIGITALE_ADDRESSEN_PATH = reverse_lazy(
    "klantinteracties:digitaaladres-list",
    kwargs=dict(version=settings.REST_FRAMEWORK["DEFAULT_VERSION"]),
)

PARTIJEN_PATH = reverse_lazy(
    "klantinteracties:partij-list",
    kwargs=dict(version=settings.REST_FRAMEWORK["DEFAULT_VERSION"]),
)


def _retrieve_klanten(url: str, access_token: str) -> Tuple[list[Klant], str | None]:
    klanten_path = "/klanten/api/v1/klanten"

    _url = urlparse(url)
    _params = parse_qs(_url.query)

    client = LegacyOpenKlantClient(f"{_url.scheme}://{_url.netloc}", access_token)
    response_data = client.retrieve(_url.path or klanten_path, params=_params)

    if not isinstance(response_data, dict):
        logger.error("unexpected_response_data", response_data=response_data)
        return [], None

    items = response_data.get("results", [])
    klanten = []

    generic_client = Client()

    for data in items:
        klant = Klant(
            **{field: value for field, value in data.items() if field in KLANT_FIELDS}
        )

        if klant.subject and not klant.subject_type:
            subject_data = generic_client.retrieve(klant.subject)

            if not isinstance(subject_data, dict):
                logger.error(
                    "unexpected_response_data",
                    context="subject_retrieval",
                    subject_data=subject_data,
                )

                continue

            klant.set_from_external_subject(subject_data)

        klanten.append(klant)

    next_url = response_data.get("next")
    return klanten, next_url


NUMMER_FIELD_MAPPING = {
    "natuurlijk_persoon": "inp_bsn",
    "niet_natuurlijk_persoon": "inn_nnp_id",
    "vestiging": "vestigings_nummer",
}


def _save_klanten_phonenumbers(
    url: str, token: TokenAuth, klanten: list[Klant]
) -> list[str]:
    if not klanten:
        logger.info("no_klanten_to_save")
        return []

    logger.info("updating_klanten_v2_api", count=len(klanten))

    openklant_client = OpenKlantClient(url, token)
    updated_klanten = []

    partijen_to_use = Partij.objects.exclude(
        digitaaladres__referentie="portaalvoorkeur",
        digitaaladres__soort_digitaal_adres=SoortDigitaalAdres.telefoonnummer,
    )

    for klant in klanten:
        subject_type = getattr(klant, "subject_type", None)
        nummer_field = NUMMER_FIELD_MAPPING.get(subject_type)
        nummer = getattr(klant.subject_identificatie, "get", lambda x: None)(
            nummer_field
        )
        try:
            soort_partij = klant._get_soort_partij()
            partij = partijen_to_use.get(soort_partij=soort_partij, nummer=nummer)
        except Partij.DoesNotExist:
            logger.warning(
                "partij_not_found",
                klant=klant,
                subject_type=subject_type,
                nummer=nummer,
            )
            continue

        digitaal_adres = klant.to_digitaal_adres_phonenumber()
        if digitaal_adres:
            digitaal_adres_data = digitaal_adres.dict()
            digitaal_adres_data["referentie"] = "portaalvoorkeur"

            _data = openklant_client.create(
                DIGITALE_ADDRESSEN_PATH,
                digitaal_adres_data,
            )

            if _data and "url" in _data:
                try:
                    da = DigitaalAdres.objects.get(uuid=_data["uuid"])
                    da.partij = partij
                    da.save(update_fields=["partij"])
                    updated_klanten.append(_data["url"])
                except DigitaalAdres.DoesNotExist:
                    logger.error(
                        "digitaaladres_not_found_after_create", uuid=_data["uuid"]
                    )

    return updated_klanten


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "v1_url",
            type=str,
            metavar="https://example.openklant.nl",
            help="URL of the Klanten API",
        )

        parser.add_argument(
            "v2_url",
            type=str,
            metavar="https://example.klantinteracties.nl",
            help="URL of the Klantinteracties API",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        client_id = os.getenv("CLIENT_ID")
        secret = os.getenv("SECRET")

        v1_url = options["v1_url"]
        v2_url = options["v2_url"]

        url_validator = URLValidator(schemes=["http", "https"])

        for url in (v1_url, v2_url):
            try:
                url_validator(url)
            except ValidationError as e:
                raise CommandError(
                    f"Invalid URL(s) detected: {str(e.message)}. See "
                    "migrate_to_v2 --help for correct usage."
                )

        if client_id and secret:
            access_token = generate_jwt_token(client_id, secret)
        else:
            access_token = os.getenv("ACCESS_TOKEN")

        next_url: str | None = ""

        if not access_token:
            raise ImproperlyConfigured("An access token is required to acces V1")

        dummy_token = _generate_dummy_token()
        results = []

        try:
            while next_url is not None:
                klanten, next_url = _retrieve_klanten(
                    v1_url if next_url == "" else next_url, access_token
                )
                results.extend(_save_klanten_phonenumbers(v2_url, dummy_token, klanten))
        finally:
            dummy_tokens = TokenAuth.objects.filter(
                application=MIGRATION_TOKEN_IDENTIFIER
            )

            dummy_tokens.delete()

        return "\n".join(results)
