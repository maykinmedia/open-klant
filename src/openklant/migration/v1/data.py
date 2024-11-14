import logging
from dataclasses import dataclass
from typing import Optional

from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.migration.v1.enum import KlantType
from openklant.migration.v2.data import DigitaalAdres, Partij

logger = logging.getLogger(__name__)


class Subject:
    @property
    def nummer(self) -> str:
        raise NotImplementedError

    def migrate(self) -> dict:
        raise NotImplementedError


@dataclass
class NatuurlijkPersoon(Subject):  # SoortPartij.persoon
    voorletters: Optional[str]
    voornaam: Optional[str]
    achternaam: Optional[str]
    voorvoegsel_achternaam: Optional[str]

    inp_bsn: Optional[str]

    @property
    def nummer(self) -> str:
        return self.inp_bsn or ""

    def migrate(self) -> dict:
        return dict(
            contactnaam=dict(
                voorletters=self.voorletters,
                voornaam=self.voornaam,
                voorvoegsel_achternaam=self.voorvoegsel_achternaam,
                achternaam=self.achternaam,
            )
        )


@dataclass
class NietNatuurlijkPersoon(Subject):  # SoortPartij.organisatie
    inn_nnp_id: Optional[str]
    statutaire_naam: Optional[str]

    @property
    def nummer(self) -> str:
        return self.inn_nnp_id or ""

    def migrate(self) -> dict:
        return dict(naam=self.statutaire_naam)


@dataclass
class Vestiging(Subject):  # SoortPartij.organisatie
    bedrijfsnaam: Optional[str]
    vestigings_nummer: Optional[str]

    @property
    def nummer(self) -> str:
        return self.vestigings_nummer or ""

    def migrate(self) -> dict:
        return dict(naam=self.bedrijfsnaam)


@dataclass
class Klant:
    subject: Optional[str] = None
    subject_identificatie: Optional[dict] = None
    subject_type: Optional[str] = None
    emailadres: Optional[str] = None

    voornaam: Optional[str] = None
    achternaam: Optional[str] = None
    voorvoegsel_achternaam: Optional[str] = None

    bedrijfsnaam: Optional[str] = None

    def _get_subject(
        self,
    ) -> NatuurlijkPersoon | NietNatuurlijkPersoon | Vestiging | None:
        subject_mapping = {
            KlantType.natuurlijk_persoon: NatuurlijkPersoon,
            KlantType.niet_natuurlijk_persoon: NietNatuurlijkPersoon,
            KlantType.vestiging: Vestiging,
        }

        if not self.subject_type:
            return

        subject_class = subject_mapping.get(self.subject_type)

        if not subject_class:
            raise ValueError("No known subjectType found")

        subject_data = self.subject_identificatie

        if not isinstance(subject_data, dict) and subject_data is not None:
            raise ValueError("Invalid subjectIdentificatie data received")

        if not subject_data:
            return

        if subject_class == NatuurlijkPersoon:
            return NatuurlijkPersoon(
                voorletters=subject_data.get("voorletters", ""),
                voornaam=self.voornaam,
                achternaam=self.achternaam,
                voorvoegsel_achternaam=self.voorvoegsel_achternaam,
                inp_bsn=subject_data.get("inp_bsn", ""),
            )
        elif subject_class == NietNatuurlijkPersoon:
            return NietNatuurlijkPersoon(
                inn_nnp_id=subject_data.get("inn_nnp_id", ""),
                statutaire_naam=subject_data.get("statutaire_naam", ""),
            )
        elif subject_class == Vestiging:
            return Vestiging(
                bedrijfsnaam=self.bedrijfsnaam,
                vestigings_nummer=subject_data.get("vestigings_nummer", ""),
            )

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
            nummer=subject.nummer if subject else "",
            partij_identificatie=subject.migrate() if subject else None,
        )

        if digitaal_adres:
            data["digitale_adressen"] = [dict(uuid=digitaal_adres)]
            data["voorkeurs_digitaal_adres"] = dict(uuid=digitaal_adres)

        return Partij(**data)
