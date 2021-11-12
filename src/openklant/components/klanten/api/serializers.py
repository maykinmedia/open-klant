import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.polymorphism import Discriminator, PolymorphicSerializer
from vng_api_common.serializers import add_choice_values_help_text
from vng_api_common.validators import IsImmutableValidator, URLValidator

from openklant.components.klanten.datamodel.constants import (
    GeslachtsAanduiding,
    KlantType,
)
from openklant.components.klanten.datamodel.models import (
    Klant,
    KlantAdres,
    NatuurlijkPersoon,
    NietNatuurlijkPersoon,
    SubVerblijfBuitenland,
    VerblijfsAdres,
    Vestiging,
)

logger = logging.getLogger(__name__)


class SubVerblijfBuitenlandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVerblijfBuitenland
        fields = (
            "lnd_landcode",
            "lnd_landnaam",
            "sub_adres_buitenland_1",
            "sub_adres_buitenland_2",
            "sub_adres_buitenland_3",
        )


class VerblijfsAdresSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerblijfsAdres
        fields = (
            "aoa_identificatie",
            "wpl_woonplaats_naam",
            "gor_openbare_ruimte_naam",
            "aoa_postcode",
            "aoa_huisnummer",
            "aoa_huisletter",
            "aoa_huisnummertoevoeging",
            "inp_locatiebeschrijving",
        )
        extra_kwargs = {
            "aoa_postcode": {"source": "postcode"},
            "aoa_huisnummer": {"source": "huisnummer"},
            "aoa_huisletter": {"source": "huisletter"},
            "aoa_huisnummertoevoeging": {"source": "huisnummertoevoeging"},
            "wpl_woonplaats_naam": {"source": "woonplaats_naam"},
        }


class KlantAdresSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlantAdres
        fields = (
            "straatnaam",
            "huisnummer",
            "huisletter",
            "huisnummertoevoeging",
            "postcode",
            "woonplaatsnaam",
            "landcode",
        )
        extra_kwargs = {"woonplaatsnaam": {"source": "woonplaats_naam"}}


class NatuurlijkPersoonSerializer(serializers.ModelSerializer):
    verblijfsadres = VerblijfsAdresSerializer(required=False, allow_null=True)
    sub_verblijf_buitenland = SubVerblijfBuitenlandSerializer(
        required=False, allow_null=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(GeslachtsAanduiding)
        self.fields["geslachtsaanduiding"].help_text += f"\n\n{value_display_mapping}"

    class Meta:
        model = NatuurlijkPersoon
        fields = (
            "inp_bsn",
            "anp_identificatie",
            "inp_a_nummer",
            "geslachtsnaam",
            "voorvoegsel_geslachtsnaam",
            "voorletters",
            "voornamen",
            "geslachtsaanduiding",
            "geboortedatum",
            "verblijfsadres",
            "sub_verblijf_buitenland",
        )

    def create(self, validated_data):
        verblijfsadres_data = validated_data.pop("verblijfsadres", None)
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        natuurlijkpersoon = super().create(validated_data)

        if verblijfsadres_data:
            verblijfsadres_data["natuurlijkpersoon"] = natuurlijkpersoon
            VerblijfsAdresSerializer().create(verblijfsadres_data)

        if sub_verblijf_buitenland_data:
            sub_verblijf_buitenland_data["natuurlijkpersoon"] = natuurlijkpersoon
            SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)

        return natuurlijkpersoon

    def update(self, instance, validated_data):
        verblijfsadres_data = validated_data.pop("verblijfsadres", None)
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        natuurlijkpersoon = super().update(instance, validated_data)

        if verblijfsadres_data:
            if hasattr(natuurlijkpersoon, "verblijfsadres"):
                VerblijfsAdresSerializer().update(
                    natuurlijkpersoon.verblijfsadres, verblijfsadres_data
                )
            else:
                verblijfsadres_data["natuurlijkpersoon"] = natuurlijkpersoon
                VerblijfsAdresSerializer().create(verblijfsadres_data)

        if sub_verblijf_buitenland_data:
            if hasattr(natuurlijkpersoon, "sub_verblijf_buitenland"):
                SubVerblijfBuitenlandSerializer().update(
                    natuurlijkpersoon.sub_verblijf_buitenland,
                    sub_verblijf_buitenland_data,
                )
            else:
                sub_verblijf_buitenland_data["natuurlijkpersoon"] = natuurlijkpersoon
                SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)

        return natuurlijkpersoon


class NietNatuurlijkPersoonSerializer(serializers.ModelSerializer):
    sub_verblijf_buitenland = SubVerblijfBuitenlandSerializer(
        required=False, allow_null=True
    )

    class Meta:
        model = NietNatuurlijkPersoon
        fields = (
            "inn_nnp_id",
            "ann_identificatie",
            "statutaire_naam",
            "inn_rechtsvorm",
            "bezoekadres",
            "sub_verblijf_buitenland",
        )

    def create(self, validated_data):
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        nietnatuurlijkpersoon = super().create(validated_data)

        if sub_verblijf_buitenland_data:
            sub_verblijf_buitenland_data[
                "nietnatuurlijkpersoon"
            ] = nietnatuurlijkpersoon
            SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)
        return nietnatuurlijkpersoon

    def update(self, instance, validated_data):
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        nietnatuurlijkpersoon = super().update(instance, validated_data)

        if sub_verblijf_buitenland_data:
            if hasattr(nietnatuurlijkpersoon, "sub_verblijf_buitenland"):
                SubVerblijfBuitenlandSerializer().update(
                    nietnatuurlijkpersoon.sub_verblijf_buitenland,
                    sub_verblijf_buitenland_data,
                )
            else:
                sub_verblijf_buitenland_data[
                    "nietnatuurlijkpersoon"
                ] = nietnatuurlijkpersoon
                SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)

        return nietnatuurlijkpersoon


class VestigingSerializer(serializers.ModelSerializer):
    verblijfsadres = VerblijfsAdresSerializer(required=False, allow_null=True)
    sub_verblijf_buitenland = SubVerblijfBuitenlandSerializer(
        required=False, allow_null=True
    )

    class Meta:
        model = Vestiging
        fields = (
            "vestigings_nummer",
            "handelsnaam",
            "verblijfsadres",
            "sub_verblijf_buitenland",
        )

    def create(self, validated_data):
        verblijfsadres_data = validated_data.pop("verblijfsadres", None)
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        vestiging = super().create(validated_data)

        if verblijfsadres_data:
            verblijfsadres_data["vestiging"] = vestiging
            VerblijfsAdresSerializer().create(verblijfsadres_data)

        if sub_verblijf_buitenland_data:
            sub_verblijf_buitenland_data["vestiging"] = vestiging
            SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)
        return vestiging

    def update(self, instance, validated_data):
        verblijfsadres_data = validated_data.pop("verblijfsadres", None)
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        vestiging = super().update(instance, validated_data)

        if verblijfsadres_data:
            if hasattr(vestiging, "verblijfsadres"):
                VerblijfsAdresSerializer().update(
                    vestiging.verblijfsadres, verblijfsadres_data
                )
            else:
                verblijfsadres_data["vestiging"] = vestiging
                VerblijfsAdresSerializer().create(verblijfsadres_data)

        if sub_verblijf_buitenland_data:
            if hasattr(vestiging, "sub_verblijf_buitenland"):
                SubVerblijfBuitenlandSerializer().update(
                    vestiging.sub_verblijf_buitenland, sub_verblijf_buitenland_data
                )
            else:
                sub_verblijf_buitenland_data["vestiging"] = vestiging
                SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)

        return vestiging


# main models
class KlantSerializer(PolymorphicSerializer):
    adres = KlantAdresSerializer(
        required=False,
        allow_null=True,
        help_text="Adresgegevens zoals opgegeven door de klant (kan ook een buitenlandsadres zijn)",
    )
    discriminator = Discriminator(
        discriminator_field="subject_type",
        mapping={
            KlantType.natuurlijk_persoon: NatuurlijkPersoonSerializer(),
            KlantType.niet_natuurlijk_persoon: NietNatuurlijkPersoonSerializer(),
            KlantType.vestiging: VestigingSerializer(),
        },
        group_field="subject_identificatie",
        same_model=False,
    )

    class Meta:
        model = Klant
        fields = (
            "url",
            "bronorganisatie",
            "klantnummer",
            "bedrijfsnaam",
            "functie",
            "website_url",
            "voornaam",
            "voorvoegsel_achternaam",
            "achternaam",
            "telefoonnummer",
            "emailadres",
            "adres",
            "subject",
            "subject_type",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "subject": {"required": False, "validators": [URLValidator()]},
            "subject_type": {"validators": [IsImmutableValidator()]},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(KlantType)
        self.fields["subject_type"].help_text += f"\n\n{value_display_mapping}"

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)
        subject = validated_attrs.get("subject", None)
        subject_identificatie = validated_attrs.get("subject_identificatie", None)

        if self.instance:
            subject = subject or self.instance.subject
            subject_identificatie = (
                subject_identificatie or self.instance.subject_identificatie
            )

        if not subject and not subject_identificatie:
            raise serializers.ValidationError(
                _("subject or subjectIdentificatie must be provided"),
                code="invalid-subject",
            )

        return validated_attrs

    def to_internal_value(self, data):
        """rewrite method to support update"""
        if self.discriminator.discriminator_field not in data and self.instance:
            data[self.discriminator.discriminator_field] = getattr(
                self.instance, self.discriminator.discriminator_field
            )

        return super().to_internal_value(data)

    @transaction.atomic
    def create(self, validated_data):
        group_data = validated_data.pop("subject_identificatie", None)
        adres_data = validated_data.pop("adres", None)
        klant = super().create(validated_data)

        if adres_data:
            adres_data["klant"] = klant
            KlantAdresSerializer().create(adres_data)

        if group_data:
            group_serializer = self.discriminator.mapping[
                validated_data["subject_type"]
            ]
            serializer = group_serializer.get_fields()["subject_identificatie"]
            group_data["klant"] = klant
            serializer.create(group_data)

        return klant

    @transaction.atomic
    def update(self, instance, validated_data):
        group_data = validated_data.pop("subject_identificatie", None)
        adres_data = validated_data.pop("adres", None)
        klant = super().update(instance, validated_data)
        subject_type = validated_data.get("subject_type", klant.subject_type)

        if adres_data:
            if hasattr(klant, "adres"):
                KlantAdresSerializer().update(klant.adres, adres_data)
            else:
                adres_data["klant"] = klant
                KlantAdresSerializer().create(adres_data)

        if group_data:
            group_serializer = self.discriminator.mapping[subject_type]
            serializer = group_serializer.get_fields()["subject_identificatie"]
            group_instance = klant.subject_identificatie
            if group_instance:
                serializer.update(group_instance, group_data)
            else:
                group_data["klant"] = klant
                serializer.create(group_data)

        return klant
