from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

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
    partij_exists,
    partij_identificator_exists,
    partij_is_organisatie,
)
from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.partijen import (
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
    Persoon,
)


class PartijForeignkeyBaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Partij
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
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
        required=True,
        allow_null=True,
        help_text=_(
            "Naam die een persoon wil gebruiken tijdens contact met de gemeente. "
            "Deze mag afwijken van de eventueel in de Basisregistratie Personen "
            "(BRP) bekende naam van de persoon."
        ),
    )

    class Meta:
        model = Persoon
        fields = ("contactnaam",)


class ContactpersoonSerializer(NestedGegevensGroepMixin, serializers.ModelSerializer):
    werkte_voor_partij = PartijPolymorphicSerializer(
        required=True,
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

    class Meta:
        model = Contactpersoon
        fields = (
            "uuid",
            "werkte_voor_partij",
            "contactnaam",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        if "werkte_voor_partij" in validated_data:
            if partij := validated_data.pop("werkte_voor_partij", None):
                partij = Partij.objects.get(uuid=str(partij.get("uuid")))

            validated_data["werkte_voor_partij"] = partij

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        if partij := validated_data.pop("werkte_voor_partij"):
            partij = Partij.objects.get(uuid=str(partij.get("uuid")))

        validated_data["werkte_voor_partij"] = partij

        return super().create(validated_data)


class PartijIdentificatorGroepTypeSerializer(GegevensGroepSerializer):
    class Meta:
        model = PartijIdentificator
        gegevensgroep = "partij_identificator"


class PartijIdentificatorSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    identificeerde_partij = PartijForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_("Partij-identificator die hoorde bij een partij."),
        source="partij",
    )
    partij_identificator = PartijIdentificatorGroepTypeSerializer(
        required=True,
        allow_null=True,
        help_text=_(
            "Gegevens die een partij in een basisregistratie "
            "of ander extern register uniek identificeren."
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
        )

        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:partijidentificator-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze partij indentificator binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "partij" in validated_data:
            if partij := validated_data.pop("partij", None):
                validated_data["partij"] = Partij.objects.get(
                    uuid=str(partij.get("uuid"))
                )

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        partij_uuid = str(validated_data.pop("partij").get("uuid"))
        validated_data["partij"] = Partij.objects.get(uuid=partij_uuid)

        return super().create(validated_data)


class PartijSerializer(NestedGegevensGroepMixin, PolymorphicSerializer):
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
    digitale_adressen = DigitaalAdresForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_(
            "Digitaal adres dat een partij verstrekte voor gebruik bij "
            "toekomstig contact met de gemeente."
        ),
        source="digitaaladres_set",
        many=True,
    )
    voorkeurs_digitaal_adres = DigitaalAdresForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_(
            "Digitaal adres waarop een partij bij voorkeur door de gemeente benaderd wordt."
        ),
    )
    vertegenwoordigde = PartijForeignKeySerializer(
        required=True,
        allow_null=True,
        many=True,
        help_text=_("Partij die een andere partij vertegenwoordigde."),
    )
    partij_identificatoren = PartijIdentificatorForeignkeySerializer(
        read_only=True,
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
        # 2 levels
        "betrokkenen.had_klantcontact": f"{SERIALIZER_PATH}.klantcontacten.KlantcontactSerializer",
        # 3 levels
        "betrokkenen.had_klantcontact.had_betrokken_actoren": f"{SERIALIZER_PATH}.actoren.ActorSerializer",
    }

    class Meta:
        model = Partij
        fields = (
            "uuid",
            "url",
            "nummer",
            "interne_notitie",
            "betrokkenen",
            "digitale_adressen",
            "voorkeurs_digitaal_adres",
            "vertegenwoordigde",
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

    @transaction.atomic
    def update(self, instance, validated_data):
        method = self.context.get("request").method
        partij_identificatie = validated_data.pop("partij_identificatie", None)

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

        return partij

    @transaction.atomic
    def create(self, validated_data):
        partij_identificatie = validated_data.pop("partij_identificatie")
        digitale_adressen = validated_data.pop("digitaaladres_set")

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

        if vertegenwoordigde := validated_data.pop("vertegenwoordigde", None):
            partijen = [str(partij["uuid"]) for partij in vertegenwoordigde]
            validated_data["vertegenwoordigde"] = Partij.objects.filter(
                uuid__in=partijen
            )

        validated_data["voorkeurs_digitaal_adres"] = voorkeurs_digitaal_adres

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

        return partij
