from dataclasses import asdict, dataclass, fields as dataclass_fields
from typing import Iterable, Optional


class APIClass:
    @property
    def required_fields(self) -> Iterable:
        raise NotImplementedError

    def dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if k in self.required_fields or v}


@dataclass
class DigitaalAdres(APIClass):
    adres: str
    soort_digitaal_adres: str = "email"
    omschrijving: str = "Emailadres"
    verstrekt_door_betrokkene: Optional[dict] = None
    verstrekt_door_partij: Optional[dict] = None

    @property
    def required_fields(self):
        return {field.name: field for field in dataclass_fields(self)}


@dataclass
class Partij(APIClass):
    nummer: str

    partij_identificatie: dict
    soort_partij: str

    indicatie_actief: bool = True
    indicatie_geheimhouding: bool = False
    rekeningnummers: Optional[list] = None
    voorkeurs_rekeningnummer: Optional[dict] = None
    digitale_adressen: Optional[list] = None
    voorkeurs_digitaal_adres: Optional[dict] = None

    @property
    def required_fields(self):
        return (
            "digitale_adressen",
            "voorkeurs_digitaal_adres",
            "rekeningnummers",
            "voorkeurs_rekeningnummer",
            "soort_partij",
            "indicatie_actief",
        )
