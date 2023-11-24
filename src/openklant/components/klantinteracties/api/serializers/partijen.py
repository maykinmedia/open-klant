from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresForeignKeySerializer,
)
from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    BetrokkeneForeignKeySerializer,
)
from openklant.components.klantinteracties.api.validators import (
    contactpersoon_exists,
    organisatie_exists,
    partij_exists,
    partij_identificator_exists,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.klantcontacten import Betrokkene
from openklant.components.klantinteracties.models.partijen import (
    Contactpersoon,
    Organisatie,
    Partij,
    PartijIdentificator,
    Persoon,
)


class PartijForeignKeySerializer(serializers.HyperlinkedModelSerializer):
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
                "help_text": "De unieke URL van deze partij binnen deze API.",
            },
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
                "help_text": "De unieke URL van deze partij indentificator binnen deze API.",
            },
        }


class PartijBezoekadresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Partij
        gegevensgroep = "bezoekadres"


class CorrespondentieadresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Partij
        gegevensgroep = "correspondentieadres"
        ref_name = "partij correspondentieadres serializer"


class PartijSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    betrokkenen = BetrokkeneForeignKeySerializer(
        required=True,
        allow_null=True,
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
        required=True,
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
                "help_text": "De unieke URL van deze partij binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        method = self.context.get("request").method

        if "betrokkene_set" in validated_data:
            existing_betrokkenen = instance.betrokkene_set.all()
            betrokkene_uuids = [
                betrokkene["uuid"]
                for betrokkene in validated_data.pop("betrokkene_set")
            ]

            # unset relation of betrokkenen that weren't given with the update
            for betrokkene in existing_betrokkenen:
                if betrokkene.uuid not in betrokkene_uuids:
                    betrokkene.partij = None
                    betrokkene.save()

            # create relation between betrokkene and partij of new entries
            for betrokkene_uuid in betrokkene_uuids:
                if betrokkene_uuid not in existing_betrokkenen.values_list(
                    "uuid", flat=True
                ):
                    betrokkene = Betrokkene.objects.get(uuid=betrokkene_uuid)
                    betrokkene.partij = instance
                    betrokkene.save()

        if "partijidentificator_set" in validated_data:
            existing_partij_identificatoren = instance.partijidentificator_set.all()
            partij_identificator_uuids = [
                partij_identificator["uuid"]
                for partij_identificator in validated_data.pop(
                    "partijidentificator_set"
                )
            ]

            # delete relation of partij identificator that weren't given with the update
            for partij_identificator in existing_partij_identificatoren:
                if partij_identificator.uuid not in partij_identificator_uuids:
                    partij_identificator.delete()

            # create relation between partij identificator and partij of new entries
            for partij_identificator_uuid in partij_identificator_uuids:
                if (
                    partij_identificator_uuid
                    not in existing_partij_identificatoren.values_list(
                        "uuid", flat=True
                    )
                ):
                    partij_identificator = PartijIdentificator.objects.get(
                        uuid=partij_identificator_uuid
                    )
                    partij_identificator.partij = instance
                    partij_identificator.save()

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

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        digitale_adressen = validated_data.pop("digitaaladres_set")
        partij_identificatoren = validated_data.pop("partijidentificator_set")
        betrokkenen = validated_data.pop("betrokkene_set")

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

        if digitale_adressen:
            for digitaal_adres in digitale_adressen:
                digitaal_adres = DigitaalAdres.objects.get(
                    uuid=str(digitaal_adres["uuid"])
                )
                digitaal_adres.partij = partij
                digitaal_adres.save()

        if partij_identificatoren:
            for partij_identificator in partij_identificatoren:
                partij_identificator = PartijIdentificator.objects.get(
                    uuid=str(partij_identificator["uuid"])
                )
                partij_identificator.partij = partij
                partij_identificator.save()

        if betrokkenen:
            for betrokkene in betrokkenen:
                betrokkene = Betrokkene.objects.get(uuid=str(betrokkene["uuid"]))
                betrokkene.partij = partij
                betrokkene.save()

        return partij


class ContactPersoonForeignkeySerializer(serializers.HyperlinkedModelSerializer):
    partij = PartijForeignKeySerializer(
        read_only=True,
        help_text=_("Persoon of organisatie waarmee de gemeente een relatie heeft."),
    )

    class Meta:
        model = Contactpersoon
        fields = (
            "id",
            "url",
            "partij",
        )
        extra_kwargs = {
            "id": {
                "required": True,
                "read_only": False,
                "validators": [contactpersoon_exists],
            },
            "url": {
                "view_name": "klantinteracties:contactpersoon-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van dit contact persoon binnen deze API.",
            },
        }


class OrganisatieForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisatie
        fields = (
            "id",
            "url",
        )
        extra_kwargs = {
            "id": {
                "required": True,
                "read_only": False,
                "validators": [organisatie_exists],
            },
            "url": {
                "view_name": "klantinteracties:organisatie-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van deze organisatie binnen deze API.",
            },
        }


class OrganisatieSerializer(serializers.HyperlinkedModelSerializer):
    partij = PartijForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie waarmee de gemeente een relatie heeft."),
    )
    contactpersoon = ContactPersoonForeignkeySerializer(
        required=True,
        allow_null=True,
        many=True,
        source="contactpersoon_set",
        help_text=_("Organisatie waarvoor een contactpersoon werkte."),
    )

    class Meta:
        model = Organisatie
        fields = (
            "id",
            "url",
            "naam",
            "partij",
            "contactpersoon",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:organisatie-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van deze organisatie binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "partij" in validated_data:
            if partij := validated_data.pop("partij", None):
                partij_uuid = str(partij.get("uuid"))
                if partij_uuid != str(instance.partij.uuid):
                    if Organisatie.objects.filter(partij__uuid=partij_uuid):
                        raise serializers.ValidationError(
                            {
                                "partij.uuid": _(
                                    "Er bestaat al een organisatie met eenzelfde uuid."
                                )
                            }
                        )

                validated_data["partij"] = Partij.objects.get(
                    uuid=str(partij.get("uuid"))
                )

        if "contactpersoon_set" in validated_data:
            existing_contactpersonen = instance.contactpersoon_set.all()
            contactpersonen_ids = [
                contactpersoon["id"]
                for contactpersoon in validated_data.pop("contactpersoon_set")
            ]

            # unset relation of contactpersoon that weren't given with the update
            for contactpersoon in existing_contactpersonen:
                if contactpersoon.id not in contactpersonen_ids:
                    contactpersoon.organisatie = None
                    contactpersoon.save()

            # create relation between contactpersoon and organisatie of new entries
            for contactpersoon_id in contactpersonen_ids:
                if contactpersoon_id not in existing_contactpersonen.values_list(
                    "id", flat=True
                ):
                    contactpersoon = Contactpersoon.objects.get(id=contactpersoon_id)
                    contactpersoon.organisatie = instance
                    contactpersoon.save()

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        partij_uuid = str(validated_data.pop("partij").get("uuid"))
        if Organisatie.objects.filter(partij__uuid=partij_uuid):
            raise serializers.ValidationError(
                {"partij.uuid": _("Er bestaat al een organisatie met eenzelfde uuid.")}
            )

        contactpersonen = validated_data.pop("contactpersoon_set")

        validated_data["partij"] = Partij.objects.get(uuid=partij_uuid)

        oranisatie = super().create(validated_data)

        if contactpersonen:
            for index, contactpersoon in enumerate(contactpersonen):
                contactpersoon = Contactpersoon.objects.get(
                    id=str(contactpersoon["id"])
                )
                if contactpersoon.organisatie:
                    raise serializers.ValidationError(
                        {
                            f"contactpersoon.{index}.id": _(
                                "Contactpersoon object already is linked to a organisatie object."
                            )
                        }
                    )
                contactpersoon.organisatie = oranisatie
                contactpersoon.save()

        return oranisatie


class PersoonContactSerializer(GegevensGroepSerializer):
    class Meta:
        model = Persoon
        gegevensgroep = "contactnaam"


class PersoonSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    partij = PartijForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie waarmee de gemeente een relatie heeft."),
    )
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
        fields = (
            "id",
            "url",
            "partij",
            "contactnaam",
        )

        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:persoon-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van dit persoon binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "partij" in validated_data:
            if partij := validated_data.pop("partij", None):
                partij_uuid = str(partij.get("uuid"))
                if partij_uuid != str(instance.partij.uuid):
                    if Persoon.objects.filter(partij__uuid=partij_uuid):
                        raise serializers.ValidationError(
                            {
                                "partij.uuid": _(
                                    "Er bestaat al een partij met eenzelfde uuid."
                                )
                            }
                        )

                validated_data["partij"] = Partij.objects.get(
                    uuid=str(partij.get("uuid"))
                )

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        partij_uuid = str(validated_data.pop("partij").get("uuid"))
        if Persoon.objects.filter(partij__uuid=partij_uuid):
            raise serializers.ValidationError(
                {"partij.uuid": _("Er bestaat al een partij met eenzelfde uuid.")}
            )

        validated_data["partij"] = Partij.objects.get(uuid=partij_uuid)

        return super().create(validated_data)


class ContactpersoonPersoonSerializer(GegevensGroepSerializer):
    class Meta:
        model = Contactpersoon
        gegevensgroep = "contactnaam"


class ContactpersoonSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    partij = PartijForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie waarmee de gemeente een relatie heeft."),
    )
    werkte_voor_organisatie = OrganisatieForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_("Organisatie waarvoor een contactpersoon werkte."),
        source="organisatie",
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
            "id",
            "url",
            "partij",
            "werkte_voor_organisatie",
            "contactnaam",
        )

        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:contactpersoon-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van dit contact persoon binnen deze API.",
            },
        }

    def update(self, instance, validated_data):
        if partij := validated_data.pop("partij", None):
            partij_uuid = str(partij.get("uuid"))
            if partij_uuid != str(instance.partij.uuid):
                if Contactpersoon.objects.filter(partij__uuid=partij_uuid):
                    raise serializers.ValidationError(
                        {
                            "partij.uuid": _(
                                "Er bestaat al een partij met eenzelfde uuid."
                            )
                        }
                    )

            validated_data["partij"] = Partij.objects.get(uuid=str(partij.get("uuid")))

        if "organisatie" in validated_data:
            if organisatie := validated_data.pop("organisatie", None):
                organisatie = Organisatie.objects.get(id=organisatie.get("id"))

            validated_data["organisatie"] = organisatie

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        partij_uuid = str(validated_data.pop("partij").get("uuid"))
        if Contactpersoon.objects.filter(partij__uuid=partij_uuid):
            raise serializers.ValidationError(
                {"partij.uuid": _("Er bestaat al een partij met eenzelfde uuid.")}
            )

        validated_data["partij"] = Partij.objects.get(uuid=partij_uuid)

        if organisatie := validated_data.pop("organisatie"):
            organisatie = Organisatie.objects.get(id=organisatie.get("id"))

        validated_data["organisatie"] = organisatie

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
