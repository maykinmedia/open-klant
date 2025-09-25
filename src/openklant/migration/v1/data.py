from dataclasses import dataclass, fields as dataclass_fields
from typing import Optional

from django.utils.functional import classproperty

import structlog

from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models.constants import (
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
    SoortPartij,
)
from openklant.migration.v1.enum import KlantType
from openklant.migration.v2.data import DigitaalAdres, Partij

logger = structlog.stdlib.get_logger(__name__)


class Subject:
    @property
    def nummer(self) -> str:
        raise NotImplementedError

    @classproperty
    def klant_type(self) -> KlantType:
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
        if self.inp_bsn:
            # Avoid padding incorrect BSNs
            if len(self.inp_bsn) < 8:
                return self.inp_bsn
            return self.inp_bsn.zfill(9)
        return ""

    @classproperty
    def klant_type(self) -> KlantType:
        return KlantType.natuurlijk_persoon

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

    @classproperty
    def klant_type(self) -> KlantType:
        return KlantType.niet_natuurlijk_persoon

    def migrate(self) -> dict:
        return dict(naam=self.statutaire_naam)


@dataclass
class Vestiging(Subject):  # SoortPartij.organisatie
    bedrijfsnaam: Optional[str]
    vestigings_nummer: Optional[str]

    @property
    def nummer(self) -> str:
        return self.vestigings_nummer or ""

    @classproperty
    def klant_type(self) -> KlantType:
        return KlantType.vestiging

    def migrate(self) -> dict:
        return dict(naam=self.bedrijfsnaam)


@dataclass
class Klant:
    subject: Optional[str] = None
    subject_identificatie: Optional[dict] = None
    subject_type: Optional[str] = None
    emailadres: Optional[str] = None
    telefoonnummer: Optional[str] = None

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

    def set_from_external_subject(self, subject_data: dict) -> None:
        self.subject_identificatie = subject_data

        subject_fields = {
            subject_class: [field.name for field in dataclass_fields(subject_class)]
            for subject_class in (NatuurlijkPersoon, NietNatuurlijkPersoon, Vestiging)
        }

        for subject_class, fields in subject_fields.items():
            match = any(field in subject_data for field in fields)

            if match:
                self.subject_type = subject_class.klant_type
                return

    def to_digitaal_adres_email(self) -> DigitaalAdres | None:
        if not self.emailadres:
            return

        return DigitaalAdres(
            adres=self.emailadres,
            soort_digitaal_adres=SoortDigitaalAdres.email,
        )

    def to_digitaal_adres_phonenumber(self) -> DigitaalAdres | None:
        if not self.telefoonnummer:
            return
        return DigitaalAdres(
            adres=self.telefoonnummer,
            soort_digitaal_adres=SoortDigitaalAdres.telefoonnummer,
        )

    def to_partij(self, digitaal_adres: str | None = None) -> Partij | None:
        try:
            subject = self._get_subject()
        except (TypeError, ValueError):
            logger.exception(
                "unable_to_determine_subject",
                reason="subjectIdentificatie_missing_or_invalid",
            )
            return

        try:
            soort_partij = self._get_soort_partij()
        except KeyError:
            logger.exception(
                "unable_to_determine_soortpartij",
                reason="soort_partij_missing_or_invalid",
            )
            return

        partij_identificatoren = []

        if (
            subject
            and subject.nummer
            and self.subject_type
            in {
                KlantType.natuurlijk_persoon,
                KlantType.niet_natuurlijk_persoon,
            }
        ):
            nummer = subject.nummer
            codeSoortObjectId = None
            register = None

            if self.subject_type == KlantType.niet_natuurlijk_persoon:
                if len(nummer) == 8:
                    codeSoortObjectId = PartijIdentificatorCodeSoortObjectId.kvk_nummer
                    register = PartijIdentificatorCodeRegister.hr
                elif len(nummer) == 9:
                    codeSoortObjectId = PartijIdentificatorCodeSoortObjectId.rsin
                    register = PartijIdentificatorCodeRegister.hr
                else:
                    logger.warning(
                        "invalid_nnp_identifier_length",
                        nummer=nummer,
                        reason="Expected 8 or 9 digits",
                    )
            else:
                codeSoortObjectId, register = (
                    PartijIdentificatorCodeSoortObjectId.bsn,
                    PartijIdentificatorCodeRegister.brp,
                )

            if codeSoortObjectId and register:
                partij_identificatoren.append(
                    {
                        "partijIdentificator": {
                            "codeObjecttype": self.subject_type,
                            "codeSoortObjectId": codeSoortObjectId,
                            "objectId": nummer,
                            "codeRegister": register,
                        },
                    }
                )

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
            partij_identificatoren=partij_identificatoren,
        )

        if digitaal_adres:
            data["digitale_adressen"] = [dict(uuid=digitaal_adres)]
            data["voorkeurs_digitaal_adres"] = dict(uuid=digitaal_adres)

        return Partij(**data)
