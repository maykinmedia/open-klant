from dataclasses import Field, asdict, dataclass, fields as dataclass_fields
from typing import Iterable

from openklant.components.klantinteracties.constants import SoortDigitaalAdres


@dataclass
class APIClass:
    @property
    def required_fields(self) -> Iterable:
        raise NotImplementedError

    def dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if k in self.required_fields or v}


@dataclass
class DigitaalAdres(APIClass):
    adres: str
    omschrijving: str = ""
    soort_digitaal_adres: SoortDigitaalAdres = SoortDigitaalAdres.email
    verstrekt_door_betrokkene: dict | None = None
    verstrekt_door_partij: dict | None = None

    @property
    def required_fields(self) -> dict[str, Field]:
        return {field.name: field for field in dataclass_fields(self)}


@dataclass
class Partij(APIClass):
    nummer: str

    partij_identificatie: dict | None
    soort_partij: str

    indicatie_actief: bool = True
    indicatie_geheimhouding: bool = False
    rekeningnummers: list | None = None
    voorkeurs_rekeningnummer: dict | None = None
    digitale_adressen: list | None = None
    voorkeurs_digitaal_adres: dict | None = None
    partij_identificatoren: list[dict] | None = None

    @property
    def required_fields(self) -> tuple[str, ...]:
        return (
            "digitale_adressen",
            "voorkeurs_digitaal_adres",
            "rekeningnummers",
            "voorkeurs_rekeningnummer",
            "soort_partij",
            "indicatie_actief",
        )
