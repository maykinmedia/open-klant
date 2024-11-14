# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2024 Dimpact


import logging
import os
from dataclasses import fields as dataclass_fields
from typing import Any, Tuple
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.management import CommandError
from django.core.management.base import BaseCommand, CommandParser

from rest_framework.fields import URLValidator
from rest_framework.reverse import reverse

from openklant.components.token.models import TokenAuth
from openklant.migration.client import Client
from openklant.migration.v1.client import LegacyOpenKlantClient
from openklant.migration.v1.data import Klant
from openklant.migration.v2.client import OpenKlantClient

logger = logging.getLogger(__name__)


def _retrieve_klanten(url: str, access_token: str) -> Tuple[list[Klant], str | None]:
    klanten_path = "/klanten/api/v1/klanten"

    _url = urlparse(url)
    _params = parse_qs(_url.query)

    client = LegacyOpenKlantClient(f"{_url.scheme}://{_url.netloc}", access_token)
    response_data = client.retrieve(_url.path or klanten_path, params=_params)

    if not isinstance(response_data, dict):
        logger.error(f"Unexpected response data returned: {response_data}")
        return [], None

    items = response_data.get("results", [])
    klant_fields = {field.name: field for field in dataclass_fields(Klant)}
    klanten = []

    generic_client = Client()

    for data in items:
        klant = Klant(
            **{field: value for field, value in data.items() if field in klant_fields}
        )

        if klant.subject and not klant.subject_type:
            subject_data = generic_client.retrieve(klant.subject)

            if not isinstance(subject_data, dict):
                logger.error(
                    "Unexpected response data returned during retrieval of "
                    f"subject: {subject_data}"
                )

                continue

            klant.set_from_external_subject(subject_data)

        klanten.append(klant)

    next_url = response_data.get("next")
    return klanten, next_url


def _save_klanten(url: str, klanten: list[Klant]) -> list[str]:
    if not klanten:
        logger.info("No klanten to save, moving on...")
        return []

    logger.info(f"Trying to create {len(klanten)} klanten through the V2 API")

    digitaal_addressen_path = reverse(
        "klantinteracties:digitaaladres-list",
        kwargs=dict(version=settings.REST_FRAMEWORK["DEFAULT_VERSION"]),
    )

    partijen_path = reverse(
        "klantinteracties:partij-list",
        kwargs=dict(version=settings.REST_FRAMEWORK["DEFAULT_VERSION"]),
    )

    dummy_token = _generate_dummy_token()
    openklant_client = OpenKlantClient(url, dummy_token)
    generic_client = Client()
    created_klanten = []

    for klant in klanten:
        digitaal_adres = klant.to_digitaal_adres()
        digitaal_adres_ref = None

        if digitaal_adres:
            _data = openklant_client.create(
                digitaal_addressen_path, digitaal_adres.dict()
            )

            if not isinstance(_data, dict):
                logger.error(
                    f"Unknown data received creating a digitaal adres: {_data}. "
                    "Skipping klant."
                )
                continue

            digitaal_adres_ref = _data.get("uuid")

        if klant.subject and not klant.subject_identificatie:
            subject_identificatie = generic_client.retrieve(klant.subject)

            if not isinstance(subject_identificatie, dict):
                logger.error(
                    f"Unknown data received receiving a subject: {subject_identificatie}. "
                    "Skipping klant."
                )

            klant.subject_identificatie = subject_identificatie

        partij = klant.to_partij(digitaal_adres=digitaal_adres_ref)

        if not partij:
            logger.error("Unable to create partij, skipping klant..")
            continue

        response_data = openklant_client.create(partijen_path, partij.dict())

        if response_data and "url" in response_data:
            created_klanten.append(response_data["url"])

    return created_klanten


def _generate_dummy_token() -> str:
    token_auth, _ = TokenAuth.objects.get_or_create(application="Migration application")
    return token_auth.token


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
        access_token = os.getenv("ACCESS_TOKEN")
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

        next_url: str | None = ""

        if not access_token:
            raise ImproperlyConfigured("An access token is required to acces V1")

        results = []

        while next_url is not None:
            klanten, next_url = _retrieve_klanten(
                v1_url if next_url == "" else next_url, access_token
            )
            results.extend(_save_klanten(v2_url, klanten))

        return "\n".join(results)
