import datetime
from collections import Counter

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema_field
from glom import PathAccessError, glom
from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin
from vng_api_common.utils import get_help_text

from openklant.components.klantinteracties.api.polymorphism import (
    Discriminator,
    PolymorphicSerializer,
)
from openklant.components.klantinteracties.api.serializers.constants import (
    SERIALIZER_PATH,
)
from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresForeignKeySerializer,
)
from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    BetrokkeneForeignKeySerializer,
)
from openklant.components.klantinteracties.api.validators import (
    FKUniqueTogetherValidator,
    categorie_exists,
    categorie_relatie_exists,
    partij_exists,
    partij_identificator_exists,
    partij_is_organisatie,
)
from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.partijen import (
    Categorie,
    CategorieRelatie,
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
    Persoon,
    Vertegenwoordigden,
)
from openklant.components.klantinteracties.models.rekeningnummers import Rekeningnummer
from openklant.components.klantinteracties.models.validators import (
    PartijIdentificatorTypesValidator,
    PartijIdentificatorUniquenessValidator,
)
from openklant.utils.decorators import handle_db_exceptions
from openklant.utils.serializers import get_field_instance_by_uuid, get_field_value


class PartijForeignkeyBaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Partij
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [partij_exists]},
            "url": {
                "view_name": "klantinteracties:partij-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze partij binnen deze API."),
            },
        }


class PartijForeignKeySerializer(PartijForeignkeyBaseSerializer):
    class Meta(PartijForeignkeyBaseSerializer.Meta):
        extra_kwargs = {
            **PartijForeignkeyBaseSerializer.Meta.extra_kwargs,
            "uuid": {"required": True, "validators": [partij_exists]},
        }


class CategorieForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    """Let op: Dit attribuut is EXPERIMENTEEL."""

    class Meta:
        model = Categorie
        fields = (
            "uuid",
            "url",
            "naam",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [categorie_exists]},
            "url": {
                "view_name": "klantinteracties:categorie-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze categorie binnen deze API."),
            },
            "naam": {"read_only": True},
        }


class CategorieRelatieForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    """Let op: Dit attribuut is EXPERIMENTEEL."""

    categorie_naam = serializers.SerializerMethodField(
        help_text=_("De naam van de gelinkte categorie.")
    )

    class Meta:
        model = CategorieRelatie
        fields = (
            "uuid",
            "url",
            "categorie_naam",
            "begin_datum",
            "eind_datum",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [categorie_relatie_exists]},
            "url": {
                "view_name": "klantinteracties:categorierelatie-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze categorie binnen deze API."),
            },
        }

    def get_categorie_naam(self, obj) -> str | None:
        if obj.categorie:
            return obj.categorie.naam


class PartijIdentificatorForeignkeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PartijIdentificator
        fields = (
            "uuid",
            "url",
        )

        extra_kwargs = {
            "uuid": {"required": True, "validators": [partij_identificator_exists]},
            "url": {
                "view_name": "klantinteracties:partijidentificator-detail",
                "lookup_field": "uuid",
                "help_text": _(
                    "De unieke URL van deze partij indentificator binnen deze API."
                ),
            },
        }


class PartijPolymorphicSerializer(PartijForeignkeyBaseSerializer):
    class Meta(PartijForeignkeyBaseSerializer.Meta):
        extra_kwargs = {
            **PartijForeignkeyBaseSerializer.Meta.extra_kwargs,
            "uuid": {
                "required": True,
                "validators": [partij_is_organisatie],
            },
        }


class ContactpersoonPersoonSerializer(GegevensGroepSerializer):
    class Meta:
        model = Contactpersoon
        gegevensgroep = "contactnaam"


class PartijBezoekadresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Partij
        gegevensgroep = "bezoekadres"


class CorrespondentieadresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Partij
        gegevensgroep = "correspondentieadres"
        ref_name = "PartijCorrespondentieadres"


class CategorieSerializer(serializers.HyperlinkedModelSerializer):
    """Let op: Dit endpoint is EXPERIMENTEEL."""

    class Meta:
        model = Categorie
        fields = (
            "uuid",
            "url",
            "naam",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:categorie-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze categorie binnen deze API."),
            },
        }


class CategorieRelatieSerializer(serializers.HyperlinkedModelSerializer):
    """Let op: Dit endpoint is EXPERIMENTEEL."""

    partij = PartijForeignkeyBaseSerializer(
        required=False,
        allow_null=True,
        help_text=_("De partij waar de categorie relatie aan gelinkt is."),
    )
    categorie = CategorieForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "De categorie waar de categorie relatie aan gelinkt is: Let op: Dit attribuut is EXPERIMENTEEL."
        ),
    )
    begin_datum = serializers.DateField(
        required=False,
        allow_null=True,
        help_text=_(
            "Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. "
            "Een datum wordt genoteerd van het meest naar het minst "
            "significante onderdeel. Een voorbeeld: 2022-02-21"
        ),
    )

    class Meta:
        model = CategorieRelatie
        fields = (
            "uuid",
            "url",
            "partij",
            "categorie",
            "begin_datum",
            "eind_datum",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:categorierelatie-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze categorie binnen deze API."),
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "partij" in validated_data:
            if partij := validated_data.pop("partij", None):
                partij = Partij.objects.get(uuid=str(partij.get("uuid")))

            validated_data["partij"] = partij

        if "categorie" in validated_data:
            if categorie := validated_data.pop("categorie", None):
                categorie = Categorie.objects.get(uuid=str(categorie.get("uuid")))

            validated_data["categorie"] = categorie

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        if not validated_data.get("begin_datum", None):
            validated_data["begin_datum"] = datetime.datetime.today().strftime(
                "%Y-%m-%d"
            )
        if partij := validated_data.pop("partij", None):
            partij = Partij.objects.get(uuid=str(partij.get("uuid")))

        if categorie := validated_data.pop("categorie", None):
            categorie = Categorie.objects.get(uuid=str(categorie.get("uuid")))

        validated_data["partij"] = partij
        validated_data["categorie"] = categorie

        return super().create(validated_data)


class OrganisatieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisatie
        fields = ("naam",)


class PersoonContactSerializer(GegevensGroepSerializer):
    class Meta:
        model = Persoon
        gegevensgroep = "contactnaam"


class PersoonSerializer(NestedGegevensGroepMixin, serializers.ModelSerializer):
    contactnaam = PersoonContactSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Naam die een persoon wil gebruiken tijdens contact met de gemeente. "
            "Deze mag afwijken van de eventueel in de Basisregistratie Personen "
            "(BRP) bekende naam van de persoon."
        ),
    )
    volledige_naam = serializers.SerializerMethodField(
        help_text="De voledige naam van het persoon.",
    )

    class Meta:
        model = Persoon
        fields = (
            "contactnaam",
            "volledige_naam",
        )

    def get_volledige_naam(self, obj) -> str:
        return obj.get_full_name()


class ContactpersoonSerializer(NestedGegevensGroepMixin, serializers.ModelSerializer):
    werkte_voor_partij = PartijPolymorphicSerializer(
        required=False,
        allow_null=True,
        help_text=_("Organisatie waarvoor een contactpersoon werkte."),
    )
    contactnaam = ContactpersoonPersoonSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Naam die een contactpersoon wil gebruiken tijdens contact met de gemeente. "
            "Deze mag afwijken van de eventueel in de Basisregistratie Personen "
            "(BRP) bekende naam van de contactpersoon."
        ),
    )
    volledige_naam = serializers.SerializerMethodField(
        help_text="De voledige naam van het constact persoon.",
    )

    class Meta:
        model = Contactpersoon
        fields = (
            "uuid",
            "werkte_voor_partij",
            "contactnaam",
            "volledige_naam",
        )

    def get_volledige_naam(self, obj) -> str:
        return obj.get_full_name()

    @transaction.atomic
    def update(self, instance, validated_data):
        if "werkte_voor_partij" in validated_data:
            if partij := validated_data.pop("werkte_voor_partij", None):
                partij = Partij.objects.get(uuid=str(partij.get("uuid")))

            validated_data["werkte_voor_partij"] = partij

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        if partij := validated_data.pop("werkte_voor_partij", None):
            partij = Partij.objects.get(uuid=str(partij.get("uuid")))

        validated_data["werkte_voor_partij"] = partij

        return super().create(validated_data)


class PartijIdentificatorGroepTypeSerializer(GegevensGroepSerializer):
    class Meta:
        model = PartijIdentificator
        gegevensgroep = "partij_identificator"
        extra_kwargs = {
            "code_register": {"required": True},
            "code_objecttype": {"required": True},
            "code_soort_object_id": {"required": True},
            "object_id": {"required": True},
        }
        validators = []


class PartijIdentificatorSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    identificeerde_partij = PartijForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_("Partij-identificator die hoorde bij een partij."),
        source="partij",
    )
    partij_identificator = PartijIdentificatorGroepTypeSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Gegevens die een partij in een basisregistratie "
            "of ander extern register uniek identificeren."
        ),
    )
    sub_identificator_van = PartijIdentificatorForeignkeySerializer(
        required=False,
        allow_null=True,
        help_text=get_help_text(
            "klantinteracties.PartijIdentificator", "sub_identificator_van"
        ),
    )

    class Meta:
        model = PartijIdentificator
        fields = (
            "uuid",
            "url",
            "identificeerde_partij",
            "andere_partij_identificator",
            "partij_identificator",
            "sub_identificator_van",
        )
        extra_kwargs = {
            "uuid": {"required": False, "validators": [partij_identificator_exists]},
            "url": {
                "view_name": "klantinteracties:partijidentificator-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze partij indentificator binnen deze API.",
            },
        }

    def validate(self, attrs):
        partij_identificator = get_field_value(self, attrs, "partij_identificator")
        sub_identificator_van = get_field_instance_by_uuid(
            self, attrs, "sub_identificator_van", PartijIdentificator
        )
        partij = get_field_instance_by_uuid(self, attrs, "partij", Partij)
        if partij_identificator:
            PartijIdentificatorTypesValidator()(
                code_objecttype=partij_identificator["code_objecttype"],
                code_soort_object_id=partij_identificator["code_soort_object_id"],
                object_id=partij_identificator["object_id"],
                code_register=partij_identificator["code_register"],
            )
            PartijIdentificatorUniquenessValidator(
                code_soort_object_id=partij_identificator["code_soort_object_id"],
                instance=self.instance if self.instance else None,
                sub_identificator_van=sub_identificator_van,
            )()

        attrs["sub_identificator_van"] = sub_identificator_van
        attrs["partij"] = partij

        return super().validate(attrs)

    @handle_db_exceptions
    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    @handle_db_exceptions
    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)


class PartijSerializer(NestedGegevensGroepMixin, PolymorphicSerializer):
    from openklant.components.klantinteracties.api.serializers.rekeningnummers import (
        RekeningnummerForeignKeySerializer,
    )

    discriminator = Discriminator(
        discriminator_field="soort_partij",
        mapping={
            SoortPartij.contactpersoon: ContactpersoonSerializer(),
            SoortPartij.persoon: PersoonSerializer(),
            SoortPartij.organisatie: OrganisatieSerializer(),
        },
        same_model=False,
        group_field="partij_identificatie",
    )
    betrokkenen = BetrokkeneForeignKeySerializer(
        read_only=True,
        help_text=_("Betrokkene bij klantcontact die een partij was."),
        many=True,
        source="betrokkene_set",
    )
    categorie_relaties = CategorieRelatieForeignKeySerializer(
        read_only=True,
        help_text=_(
            "De Categorie relaties van een partij: Let op: Dit attribuut is EXPERIMENTEEL."
        ),
        many=True,
        source="categorierelatie_set",
    )
    digitale_adressen = DigitaalAdresForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Digitaal adresen dat een partij verstrekte voor gebruik bij "
            "toekomstig contact met de gemeente."
        ),
        source="digitaaladres_set",
        many=True,
    )
    voorkeurs_digitaal_adres = DigitaalAdresForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Digitaal adres waarop een partij bij voorkeur door de gemeente benaderd wordt."
        ),
    )
    rekeningnummers = RekeningnummerForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_("Rekeningnummers van een partij"),
        source="rekeningnummer_set",
        many=True,
    )
    voorkeurs_rekeningnummer = RekeningnummerForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_("Rekeningsnummer die een partij bij voorkeur gebruikt."),
    )
    vertegenwoordigden = serializers.SerializerMethodField(
        help_text=_("Partijen die een andere partijen vertegenwoordigden."),
    )
    partij_identificatoren = PartijIdentificatorSerializer(
        required=False,
        allow_null=True,
        many=True,
        source="partijidentificator_set",
        help_text=_("Partij-identificatoren die hoorde bij deze partij."),
    )
    bezoekadres = PartijBezoekadresSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Adres waarop de partij door gemeente bezocht wil worden. "
            "Dit mag afwijken van voor de verstrekker eventueel in een "
            "basisregistratie bekende adressen."
        ),
    )
    correspondentieadres = CorrespondentieadresSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Adres waarop de partij post van de gemeente wil ontvangen. "
            "Dit mag afwijken van voor de verstrekker eventueel in een "
            "basisregistratie bekende adressen."
        ),
    )

    inclusion_serializers = {
        # 1 level
        "digitale_adressen": f"{SERIALIZER_PATH}.digitaal_adres.DigitaalAdresSerializer",
        "betrokkenen": f"{SERIALIZER_PATH}.klantcontacten.BetrokkeneSerializer",
        "categorie_relaties": f"{SERIALIZER_PATH}.partijen.CategorieRelatieSerializer",
        # 2 levels
        "betrokkenen.had_klantcontact": f"{SERIALIZER_PATH}.klantcontacten.KlantcontactSerializer",
    }

    class Meta:
        model = Partij
        fields = (
            "uuid",
            "url",
            "nummer",
            "interne_notitie",
            "betrokkenen",
            "categorie_relaties",
            "digitale_adressen",
            "voorkeurs_digitaal_adres",
            "vertegenwoordigden",
            "rekeningnummers",
            "voorkeurs_rekeningnummer",
            "partij_identificatoren",
            "soort_partij",
            "indicatie_geheimhouding",
            "voorkeurstaal",
            "indicatie_actief",
            "bezoekadres",
            "correspondentieadres",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:partij-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze partij binnen deze API."),
            },
        }

    @extend_schema_field(PartijForeignKeySerializer(many=True))
    def get_vertegenwoordigden(self, obj):
        return [
            PartijForeignKeySerializer(
                vertegenwoordigende.vertegenwoordigde_partij, context=self.context
            ).data
            for vertegenwoordigende in obj.vertegenwoordigende.all()
            if vertegenwoordigende
        ]

    def check_identificeerde_partij(self, attrs):
        if any(item["partij"] is not None for item in attrs):
            raise serializers.ValidationError(
                {
                    "identificeerdePartij": _(
                        "Het veld `identificeerde_partij` wordt automatisch ingesteld en"
                        " dient niet te worden opgegeven."
                    )
                },
                code="invalid",
            )

    def check_duplicated_uuid(self, attrs):
        uuid_list = [item["uuid"] for item in attrs if "uuid" in item]
        if uuid_list and max(Counter(uuid_list).values()) > 1:
            raise serializers.ValidationError(
                {
                    "identificeerdePartij": _(
                        "Duplicaat uuid kan niet worden ingevoerd voor `partij_identificatoren`."
                    )
                },
                code="duplicated",
            )

    def validate_partij_identificatoren(self, attrs):
        if attrs:
            self.check_duplicated_uuid(attrs)
            if "request" in self.context and self.context["request"].method == "POST":
                self.check_identificeerde_partij(attrs)

        return attrs

    def update_or_create_partij_identificator(self, partij_identificator):
        sub_identificator_van = partij_identificator["sub_identificator_van"]
        if isinstance(sub_identificator_van, PartijIdentificator):
            partij_identificator["sub_identificator_van"] = {
                "uuid": sub_identificator_van.uuid
            }
        partij_identificator_serializer = PartijIdentificatorSerializer(
            data=partij_identificator
        )
        partij_identificator_serializer.is_valid(raise_exception=True)
        if "uuid" in partij_identificator:
            instance = PartijIdentificator.objects.get(
                uuid=partij_identificator["uuid"]
            )
            partij_identificator_serializer.update(
                instance, partij_identificator_serializer.validated_data
            )
        else:
            partij_identificator_serializer.create(
                partij_identificator_serializer.validated_data
            )

    @handle_db_exceptions
    @transaction.atomic
    def update(self, instance, validated_data):
        method = self.context.get("request").method
        partij_identificatie = validated_data.pop("partij_identificatie", None)
        partij_identificatoren = validated_data.pop("partijidentificator_set", None)
        if "digitaaladres_set" in validated_data:
            existing_digitale_adressen = instance.digitaaladres_set.all()
            digitaal_adres_uuids = [
                digitaal_adres["uuid"]
                for digitaal_adres in validated_data.pop("digitaaladres_set")
            ]

            # unset relation of digitaal adres that weren't given with the update
            for digitaal_adres in existing_digitale_adressen:
                if digitaal_adres.uuid not in digitaal_adres_uuids:
                    digitaal_adres.partij = None
                    digitaal_adres.save()

            # create relation between digitaal adres and partij of new entries
            for digitaal_adres_uuid in digitaal_adres_uuids:
                if digitaal_adres_uuid not in existing_digitale_adressen.values_list(
                    "uuid", flat=True
                ):
                    digitaal_adres = DigitaalAdres.objects.get(uuid=digitaal_adres_uuid)
                    digitaal_adres.partij = instance
                    digitaal_adres.save()

        if "voorkeurs_digitaal_adres" in validated_data:
            if voorkeurs_digitaal_adres := validated_data.pop(
                "voorkeurs_digitaal_adres", None
            ):
                voorkeurs_digitaal_adres_uuid = voorkeurs_digitaal_adres.get("uuid")
                match (method):
                    case "PUT":
                        if len(digitaal_adres_uuids) == 0:
                            raise serializers.ValidationError(
                                {
                                    "voorkeurs_digitaal_adres": _(
                                        "voorkeursDigitaalAdres mag niet meegegeven worden "
                                        "als digitaleAdressen leeg is."
                                    )
                                }
                            )
                        if voorkeurs_digitaal_adres_uuid not in digitaal_adres_uuids:
                            raise serializers.ValidationError(
                                {
                                    "voorkeurs_digitaal_adres": _(
                                        "Het voorkeurs adres moet een gelinkte digitaal adres zijn."
                                    )
                                }
                            )
                    case "PATCH":
                        if (
                            voorkeurs_digitaal_adres_uuid
                            not in instance.digitaaladres_set.all().values_list(
                                "uuid", flat=True
                            )
                        ):
                            raise serializers.ValidationError(
                                {
                                    "voorkeurs_digitaal_adres": _(
                                        "Het voorkeurs adres moet een gelinkte digitaal adres zijn."
                                    )
                                }
                            )

                voorkeurs_digitaal_adres = DigitaalAdres.objects.get(
                    uuid=str(voorkeurs_digitaal_adres_uuid)
                )

            validated_data["voorkeurs_digitaal_adres"] = voorkeurs_digitaal_adres

        if "rekeningnummer_set" in validated_data:
            existing_rekeningnummers = instance.rekeningnummer_set.all()
            rekeningnummers_uuids = [
                rekeningnummer["uuid"]
                for rekeningnummer in validated_data.pop("rekeningnummer_set")
            ]

            # unset relation of rekeningnummer that weren't given with the update
            for rekeningnummer in existing_rekeningnummers:
                if rekeningnummer.uuid not in rekeningnummers_uuids:
                    rekeningnummer.partij = None
                    rekeningnummer.save()

            # create relation between rekeningnummer and partij of new entries
            for rekeninnummers_uuid in rekeningnummers_uuids:
                if rekeninnummers_uuid not in existing_rekeningnummers.values_list(
                    "uuid", flat=True
                ):
                    rekeningnummer = Rekeningnummer.objects.get(
                        uuid=rekeninnummers_uuid
                    )
                    rekeningnummer.partij = instance
                    rekeningnummer.save()

        if "voorkeurs_rekeningnummer" in validated_data:
            if voorkeurs_rekeningnummer := validated_data.pop(
                "voorkeurs_rekeningnummer", None
            ):
                voorkeurs_rekeningnummer_uuid = voorkeurs_rekeningnummer.get("uuid")
                match (method):
                    case "PUT":
                        if len(rekeningnummers_uuids) == 0:
                            raise serializers.ValidationError(
                                {
                                    "voorkeurs_rekeningnummer": _(
                                        "voorkeursRekeningnummer mag niet meegegeven worden "
                                        "als rekeningnummers leeg is."
                                    )
                                }
                            )
                        if voorkeurs_rekeningnummer_uuid not in rekeningnummers_uuids:
                            raise serializers.ValidationError(
                                {
                                    "voorkeurs_rekeningnummer": _(
                                        "Het voorkeurs rekeningnummer moet een gelinkte rekeningnummer zijn."
                                    )
                                }
                            )
                    case "PATCH":
                        if (
                            voorkeurs_rekeningnummer_uuid
                            not in instance.rekeningnummer_set.all().values_list(
                                "uuid", flat=True
                            )
                        ):
                            raise serializers.ValidationError(
                                {
                                    "voorkeurs_rekeningnummer": _(
                                        "Het voorkeurs rekeningnummer moet een gelinkte rekeningnummer zijn."
                                    )
                                }
                            )

                voorkeurs_rekeningnummer = Rekeningnummer.objects.get(
                    uuid=str(voorkeurs_rekeningnummer_uuid)
                )

            validated_data["voorkeurs_rekeningnummer"] = voorkeurs_rekeningnummer

        if "vertegenwoordigde" in validated_data:
            if vertegenwoordigde := validated_data.pop("vertegenwoordigde", []):
                partijen = [str(partij["uuid"]) for partij in vertegenwoordigde]
                vertegenwoordigde = Partij.objects.filter(uuid__in=partijen)

            instance.vertegenwoordigde.set(vertegenwoordigde)

        partij = super().update(instance, validated_data)

        if partij_identificatie:
            serializer_class = self.discriminator.mapping[
                validated_data.get("soort_partij")
            ]
            serializer = serializer_class.get_fields()["partij_identificatie"]

            # remove the previous data
            model = serializer.Meta.model
            model.objects.filter(partij=partij).delete()

            partij_identificatie["partij"] = partij
            serializer.create(partij_identificatie)

        if partij_identificatoren is not None:
            partij.partijidentificator_set.exclude(
                uuid__in=[pi["uuid"] for pi in partij_identificatoren if "uuid" in pi]
            ).delete()

            for partij_identificator in partij_identificatoren:
                partij_identificator["identificeerde_partij"] = {
                    "uuid": str(partij.uuid)
                }
                self.update_or_create_partij_identificator(partij_identificator)

        return partij

    @handle_db_exceptions
    @transaction.atomic
    def create(self, validated_data):
        partij_identificatie = validated_data.pop("partij_identificatie", None)
        digitale_adressen = validated_data.pop("digitaaladres_set", None)
        rekeningnummers = validated_data.pop("rekeningnummer_set", None)
        partij_identificatoren = validated_data.pop("partijidentificator_set", None)

        if voorkeurs_digitaal_adres := validated_data.pop(
            "voorkeurs_digitaal_adres", None
        ):
            voorkeurs_digitaal_adres_uuid = voorkeurs_digitaal_adres.get("uuid")
            if voorkeurs_digitaal_adres and voorkeurs_digitaal_adres_uuid not in [
                digitaal_adres["uuid"] for digitaal_adres in digitale_adressen
            ]:
                raise serializers.ValidationError(
                    {
                        "voorkeurs_digitaal_adres": _(
                            "Het voorkeurs adres moet een gelinkte digitaal adres zijn."
                        )
                    }
                )
            voorkeurs_digitaal_adres = DigitaalAdres.objects.get(
                uuid=str(voorkeurs_digitaal_adres_uuid)
            )

        if voorkeurs_rekeningnummer := validated_data.pop(
            "voorkeurs_rekeningnummer", None
        ):
            voorkeurs_rekeningnummer_uuid = voorkeurs_rekeningnummer.get("uuid")
            if voorkeurs_rekeningnummer and voorkeurs_rekeningnummer_uuid not in [
                rekeningnummer["uuid"] for rekeningnummer in rekeningnummers
            ]:
                raise serializers.ValidationError(
                    {
                        "voorkeurs_rekeningnummer": _(
                            "Het voorkeurs rekeningnummer moet een gelinkte rekeningnummer zijn."
                        )
                    }
                )
            voorkeurs_rekeningnummer = Rekeningnummer.objects.get(
                uuid=str(voorkeurs_rekeningnummer_uuid)
            )

        if vertegenwoordigde := validated_data.pop("vertegenwoordigde", None):
            partijen = [str(partij["uuid"]) for partij in vertegenwoordigde]
            validated_data["vertegenwoordigde"] = Partij.objects.filter(
                uuid__in=partijen
            )

        validated_data["voorkeurs_digitaal_adres"] = voorkeurs_digitaal_adres
        validated_data["voorkeurs_rekeningnummer"] = voorkeurs_rekeningnummer

        partij = super().create(validated_data)

        if partij_identificatie:
            if "werkte_voor_partij" in partij_identificatie:
                partij_identificatie["werkte_voor_partij"] = partij_identificatie.pop(
                    "werkte_voor_partij"
                )

            serializer_class = self.discriminator.mapping[
                validated_data["soort_partij"]
            ]
            serializer = serializer_class.get_fields()["partij_identificatie"]
            partij_identificatie["partij"] = partij
            serializer.create(partij_identificatie)

        if digitale_adressen:
            for digitaal_adres in digitale_adressen:
                digitaal_adres = DigitaalAdres.objects.get(
                    uuid=str(digitaal_adres["uuid"])
                )
                digitaal_adres.partij = partij
                digitaal_adres.save()

        if rekeningnummers:
            for rekeningnummer in rekeningnummers:
                rekeningnummer = Rekeningnummer.objects.get(
                    uuid=str(rekeningnummer["uuid"])
                )
                rekeningnummer.partij = partij
                rekeningnummer.save()

        if partij_identificatoren:
            for partij_identificator in partij_identificatoren:
                partij_identificator["identificeerde_partij"] = {
                    "uuid": str(partij.uuid)
                }
                self.update_or_create_partij_identificator(partij_identificator)

        return partij


class VertegenwoordigdenSerializer(serializers.HyperlinkedModelSerializer):
    vertegenwoordigende_partij = PartijForeignKeySerializer(
        required=True,
        help_text=_("'Partij' die een andere 'Partij' vertegenwoordigde."),
    )
    vertegenwoordigde_partij = PartijForeignKeySerializer(
        required=True,
        help_text=_("'Partij' vertegenwoordigd wordt door een andere 'Partij'."),
    )

    class Meta:
        model = Vertegenwoordigden
        fields = (
            "uuid",
            "url",
            "vertegenwoordigende_partij",
            "vertegenwoordigde_partij",
        )
        validators = [
            FKUniqueTogetherValidator(
                queryset=Vertegenwoordigden.objects.all(),
                fields=(
                    "vertegenwoordigende_partij",
                    "vertegenwoordigde_partij",
                ),
            )
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:vertegenwoordigden-detail",
                "lookup_field": "uuid",
                "help_text": _(
                    "De unieke URL van deze vertegenwoordigden binnen deze API."
                ),
            },
        }

    def validate(self, attrs):
        vertegenwoordigende_partij = (
            glom(attrs, "vertegenwoordigende_partij.uuid", skip_exc=PathAccessError)
            or self.instance.vertegenwoordigende_partij.uuid
        )

        vertegenwoordigde_partij = (
            glom(attrs, "vertegenwoordigde_partij.uuid", skip_exc=PathAccessError)
            or self.instance.vertegenwoordigde_partij.uuid
        )

        if vertegenwoordigende_partij == vertegenwoordigde_partij:
            raise serializers.ValidationError(
                {
                    "vertegenwoordigde_partij": _(
                        "De partij kan niet zichzelf vertegenwoordigen."
                    )
                }
            )

        return super().validate(attrs)

    @transaction.atomic
    def update(self, instance, validated_data):
        if "vertegenwoordigende_partij" in validated_data:
            if vertegenwoordigende_partij := validated_data.pop(
                "vertegenwoordigende_partij", None
            ):
                validated_data["vertegenwoordigende_partij"] = Partij.objects.get(
                    uuid=str(vertegenwoordigende_partij.get("uuid"))
                )

        if "vertegenwoordigde_partij" in validated_data:
            if vertegenwoordigde_partij := validated_data.pop(
                "vertegenwoordigde_partij", None
            ):
                validated_data["vertegenwoordigde_partij"] = Partij.objects.get(
                    uuid=str(vertegenwoordigde_partij.get("uuid"))
                )

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        vertegenwoordigende_partij_uuid = str(
            validated_data.pop("vertegenwoordigende_partij").get("uuid")
        )
        validated_data["vertegenwoordigende_partij"] = Partij.objects.get(
            uuid=vertegenwoordigende_partij_uuid
        )

        vertegenwoordigde_partij_uuid = str(
            validated_data.pop("vertegenwoordigde_partij").get("uuid")
        )
        validated_data["vertegenwoordigde_partij"] = Partij.objects.get(
            uuid=vertegenwoordigde_partij_uuid
        )

        return super().create(validated_data)
