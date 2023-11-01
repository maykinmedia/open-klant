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
    organisatie_exists,
    partij_exists,
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
            "nummer",
            "interne_notitie",
        )
        read_only_fields = (
            "nummer",
            "interne_notitie",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [partij_exists]},
            "url": {
                "view_name": "partij-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze partij binnen deze API.",
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
    betrokkene = BetrokkeneForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_("Betrokkene bij klantcontact die een partij was."),
    )
    digitaal_adres = DigitaalAdresForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_(
            "Digitaal adres dat een partij verstrekte voor gebruik bij "
            "toekomstig contact met de gemeente."
        ),
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
            "betrokkene",
            "digitaal_adres",
            "voorkeurs_digitaal_adres",
            "vertegenwoordigde",
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
                "view_name": "partij-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze partij binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get("betrokkene"):
            if betrokkene := validated_data.pop("betrokkene", None):
                validated_data["betrokkene"] = Betrokkene.objects.get(
                    uuid=str(betrokkene.get("uuid"))
                )

        if validated_data.get("digitaal_adres"):
            if digitaal_adres := validated_data.pop("digitaal_adres", None):
                validated_data["digitaal_adres"] = DigitaalAdres.objects.get(
                    uuid=str(digitaal_adres.get("uuid"))
                )

        if validated_data.get("voorkeurs_digitaal_adres"):
            if voorkeurs_digitaal_adres := validated_data.pop(
                "voorkeurs_digitaal_adres", None
            ):
                validated_data["voorkeurs_digitaal_adres"] = DigitaalAdres.objects.get(
                    uuid=str(voorkeurs_digitaal_adres.get("uuid"))
                )

        if validated_data.get("vertegenwoordigde"):
            if vertegenwoordigde := validated_data.pop("vertegenwoordigde", []):
                partijen = [str(partij["uuid"]) for partij in vertegenwoordigde]
                instance.vertegenwoordigde.set(Partij.objects.filter(uuid__in=partijen))

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        if betrokkene := validated_data.pop("betrokkene", None):
            validated_data["betrokkene"] = Betrokkene.objects.get(
                uuid=str(betrokkene.get("uuid"))
            )

        if digitaal_adres := validated_data.pop("digitaal_adres", None):
            validated_data["digitaal_adres"] = DigitaalAdres.objects.get(
                uuid=str(digitaal_adres.get("uuid"))
            )

        if voorkeurs_digitaal_adres := validated_data.pop(
            "voorkeurs_digitaal_adres", None
        ):
            validated_data["voorkeurs_digitaal_adres"] = DigitaalAdres.objects.get(
                uuid=str(voorkeurs_digitaal_adres.get("uuid"))
            )

        if vertegenwoordigde := validated_data.pop("vertegenwoordigde", None):
            partijen = [str(partij["uuid"]) for partij in vertegenwoordigde]
            validated_data["vertegenwoordigde"] = Partij.objects.filter(
                uuid__in=partijen
            )

        return super().create(validated_data)


class OrganisatieForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisatie
        fields = (
            "id",
            "url",
            "naam",
        )
        extra_kwargs = {
            "id": {
                "required": True,
                "read_only": False,
                "validators": [organisatie_exists],
            },
            "url": {
                "view_name": "organisatie-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van deze organisatie binnen deze API.",
            },
            "naam": {"read_only": True},
        }


class OrganisatieSerializer(serializers.HyperlinkedModelSerializer):
    partij = PartijForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie waarmee de gemeente een relatie heeft."),
    )

    class Meta:
        model = Organisatie
        fields = (
            "id",
            "url",
            "naam",
            "partij",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "organisatie-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van deze organisatie binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if partij := validated_data.pop("partij", None):
            validated_data["partij"] = Partij.objects.get(uuid=str(partij.get("uuid")))

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        partij_uuid = str(validated_data.pop("partij").get("uuid"))
        validated_data["partij"] = Partij.objects.get(uuid=partij_uuid)

        return super().create(validated_data)


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
                "view_name": "persoon-detail",
                "lookup_field": "id",
                "help_text": "De unieke URL van dit persoon binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
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

            validated_data["partij"] = Partij.objects.get(uuid=str(partij.get("uuid")))

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
    organisatie = OrganisatieForeignKeySerializer(
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
            "id",
            "url",
            "partij",
            "organisatie",
            "contactnaam",
        )

        extra_kwargs = {
            "id": {"read_only": True},
            "url": {
                "view_name": "contactpersoon-detail",
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

        if validated_data.get("organisatie"):
            if organisatie := validated_data.pop("organisatie", None):
                validated_data["organisatie"] = Organisatie.objects.get(
                    id=organisatie.get("id")
                )

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        partij_uuid = str(validated_data.pop("partij").get("uuid"))
        organisatie_id = validated_data.pop("organisatie").get("id")
        if Contactpersoon.objects.filter(partij__uuid=partij_uuid):
            raise serializers.ValidationError(
                {"partij.uuid": _("Er bestaat al een partij met eenzelfde uuid.")}
            )

        validated_data["partij"] = Partij.objects.get(uuid=partij_uuid)
        validated_data["organisatie"] = Organisatie.objects.get(id=organisatie_id)

        return super().create(validated_data)


class PartijIdentificatorGroepTypeSerializer(GegevensGroepSerializer):
    class Meta:
        model = PartijIdentificator
        gegevensgroep = "partij_identificator"


class PartijIdentificatorSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    partij = PartijForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_("Partij-identificator die hoorde bij een partij."),
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
            "partij",
            "andere_partij_identificator",
            "partij_identificator",
        )

        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "partijidentificator-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze partij indentificator binnen deze API.",
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get("partij"):
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
