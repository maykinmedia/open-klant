# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2024 Dimpact


import logging
import os
from dataclasses import asdict, dataclass, fields as dataclass_fields
from io import BytesIO
from typing import Any, Literal, Optional, Tuple

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.management.base import BaseCommand, CommandParser
from django.core.validators import URLValidator
from django.db.models import TextChoices

import requests
from djangorestframework_camel_case.parser import CamelCaseJSONParser, ParseError
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.reverse import reverse

from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.token.models import TokenAuth

logger = logging.getLogger(__name__)


class Client:
    token: str
    token_prefix: str
    base_url: str

    def __init__(self, base_url: str, token: str) -> None:
        self.token = token
        self.base_url = base_url

    def _request(
        self, method: str, url: str, data: dict | None = None
    ) -> list | dict | None:
        logger.debug(f"Retrieving {url}")

        headers = {"Authorization": f"{self.token_prefix} {self.token}"}
        renderer = CamelCaseJSONRenderer()
        _data = renderer.render(data) if data else None

        if method == "POST":
            headers.update({"Content-Type": "application/json"})

        try:
            response = requests.request(
                method,
                url,
                data=_data,
                headers=headers,
            )

            response.raise_for_status()
        except requests.RequestException:
            logger.exception(f"Failed retrieving {url}")
            return

        parser = CamelCaseJSONParser()

        try:
            response_data = parser.parse(
                BytesIO(response.content),
                parser_context=dict(encoding=response.encoding),
            )
        except ParseError:
            logger.exception(f"Unable to parse response content: {response.content}")
            return

        return response_data

    def retrieve(self, path: str) -> list | dict | None:
        url = self.base_url + path
        return self._request("GET", url)

    def create(self, path: str, data: dict) -> dict | None:
        url = self.base_url + path
        return self._request("POST", url, data)


class ClientV1(Client):
    token_prefix = "Bearer"


class ClientV2(Client):
    token_prefix = "Token"


class KlantType(TextChoices):
    natuurlijk_persoon = "natuurlijk_persoon"
    niet_natuurlijk_persoon = "niet_natuurlijk_persoon"
    vestiging = "vestiging"


class Subject:
    @property
    def nummer(self) -> str:
        raise NotImplementedError

    def migrate(self) -> dict:
        raise NotImplementedError


@dataclass
class NatuurlijkPersoon(Subject):  # SoortPartij.persoon
    voornaam: str
    achternaam: str
    voorvoegsel_achternaam: str

    inp_bsn: str

    @property
    def nummer(self) -> str:
        return self.inp_bsn or ""

    def migrate(self) -> dict:
        return dict(
            contactnaam=dict(
                voorletters="",
                voornaam=self.voornaam,
                voorvoegsel_achternaam=self.voorvoegsel_achternaam,
                achternaam=self.achternaam,
            )
        )


@dataclass
class NietNatuurlijkPersoon(Subject):  # SoortPartij.organisatie
    inn_nnp_id: str
    statutaire_naam: str

    @property
    def nummer(self) -> str:
        return self.inn_nnp_id or ""

    def migrate(self) -> dict:
        return dict(naam=self.statutaire_naam)


@dataclass
class Vestiging(Subject):  # SoortPartij.organisatie
    bedrijfsnaam: str
    vestigings_nummer: str

    @property
    def nummer(self) -> str:
        return self.vestigings_nummer or ""

    def migrate(self) -> dict:
        return dict(naam=self.handelsnaam)


@dataclass
class DigitaalAdres:
    adres: str
    soort_digitaal_adres: str = "email"
    omschrijving: str = "Emailadres"
    verstrekt_door_betrokkene: Optional[dict] = None
    verstrekt_door_partij: Optional[dict] = None

    def dict(self):
        return {k: v for k, v in asdict(self).items()}


@dataclass
class Partij:
    nummer: str

    partij_identificatie: dict
    soort_partij: str

    indicatie_actief: bool = True
    indicatie_geheimhouding: bool = False
    rekeningnummers: Optional[list] = None
    voorkeurs_rekeningnummer: Optional[dict] = None
    digitale_adressen: Optional[list] = None
    voorkeurs_digitaal_adres: Optional[dict] = None

    def dict(self):
        return {k: v for k, v in asdict(self).items()}


@dataclass
class Klant:
    subject_identificatie: dict
    subject_type: str
    telefoonnummer: str
    emailadres: str

    voornaam: str
    achternaam: str
    voorvoegsel_achternaam: str

    bedrijfsnaam: str

    def _get_subject(self) -> NatuurlijkPersoon | NietNatuurlijkPersoon | Vestiging:
        subject_mapping = {
            KlantType.natuurlijk_persoon: NatuurlijkPersoon,
            KlantType.niet_natuurlijk_persoon: NietNatuurlijkPersoon,
            KlantType.vestiging: Vestiging,
        }
        subject_class = subject_mapping.get(self.subject_type)

        if not subject_class:
            raise ValueError("No subjectType found")

        subject_data = self.subject_identificatie or {}
        fields = {field.name: field for field in dataclass_fields(subject_class)}

        # TODO: retrieve from subject_data or from Klant
        kwargs = {
            field: value or fields[field].type
            for field, value in subject_data.items()
            if field in fields
        }

        return subject_class(**kwargs)

    def _get_soort_partij(self) -> SoortPartij:
        mapping = {
            KlantType.natuurlijk_persoon: SoortPartij.persoon,
            KlantType.niet_natuurlijk_persoon: SoortPartij.organisatie,
            KlantType.vestiging: SoortPartij.organisatie,
        }

        return mapping[self.subject_type]

    def to_digitaal_adres(self) -> DigitaalAdres | None:
        if not self.emailadres:
            return

        return DigitaalAdres(adres=self.emailadres)

    def to_partij(self, digitaal_adres: str | None = None) -> Partij | None:
        try:
            subject = self._get_subject()
        except (TypeError, ValueError):
            logger.exception("Unable to determine subject from subjectIdentificatie")
            return

        try:
            soort_partij = self._get_soort_partij()
        except KeyError:
            logger.exception("Unable to determine soortPartij from subjectType")
            return

        data = dict(
            indicatie_actief=True,
            indicatie_geheimhouding=False,
            rekeningnummers=[],
            voorkeurs_rekeningnummer=None,
            digitale_adressen=None,
            voorkeurs_digitaal_adres=None,
            soort_partij=soort_partij,
            nummer=subject.nummer,
            partij_identificatie=subject.migrate(),
        )

        if digitaal_adres:
            data["digitale_adressen"] = [dict(uuid=digitaal_adres)]
            data["voorkeurs_digitaal_adres"] = dict(uuid=digitaal_adres)

        return Partij(**data)


def _retrieve_klanten(url: str, access_token: str) -> Tuple[list[Klant], str | None]:
    client = ClientV1(url, access_token)
    response_data = client.retrieve("/klanten/api/v1/klanten")

    if not isinstance(response_data, dict):
        logger.error(f"Unexpected response data returned: {response_data}")
        return [], None

    items = response_data.get("results", [])
    klant_fields = {field.name: field for field in dataclass_fields(Klant)}
    klanten = []

    for data in items:
        klant = Klant(
            **{
                field: value or klant_fields[field].type
                for field, value in data.items()
                if field in klant_fields
            }
        )

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
    client = ClientV2(url, dummy_token)
    created_klanten = []

    for klant in klanten:
        digitaal_adres = klant.to_digitaal_adres()
        digitaal_adres_ref = None

        if digitaal_adres:
            _data = client.create(digitaal_addressen_path, digitaal_adres.dict())

            if not isinstance(_data, dict):
                logger.error(
                    f"Unknown data received creating a digitaal adres: {_data}. "
                    "Skipping klant."
                )
                continue

            digitaal_adres_ref = _data.get("uuid")

        partij = klant.to_partij(digitaal_adres=digitaal_adres_ref)

        if not partij:
            logger.error("Unable to create partij, skipping klant..")
            continue

        response_data = client.create(partijen_path, partij.dict())

        if response_data and "url" in response_data:
            created_klanten.append(response_data["url"])

    return created_klanten


def _generate_dummy_token() -> str:
    token_auth, _ = TokenAuth.objects.get_or_create(application="Migration application")
    return token_auth.token


class Command(BaseCommand):
    # TODO: add cleanup argument to remove (partially) failed klant creation?
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "v1_url",
            type=str,
            metavar="example.openklant.nl",
            help="URL of the Klanten API",
        )

        parser.add_argument(
            "v2_url",
            type=str,
            metavar="example.klantinteracties.nl",
            help="URL of the Klantinteracties API",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        access_token = os.getenv("ACCESS_TOKEN")
        v1_url = options["v1_url"]
        v2_url = options["v2_url"]

        validator = URLValidator()
        for url in (v1_url, v2_url):
            try:
                validator(url)
            except ValidationError as e:
                return str(e)

        next_url: str | None = ""

        if not access_token:
            raise ImproperlyConfigured("An access token is required to acces V1")

        results = []

        while next_url is not None:
            klanten, next_url = _retrieve_klanten(v1_url, access_token)
            results.extend(_save_klanten(v2_url, klanten))

        return "\n".join(results)
