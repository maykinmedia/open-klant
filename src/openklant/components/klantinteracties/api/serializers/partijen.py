from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer

from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresForeignKeySerializer,
)
from openklant.components.klantinteracties.api.serializers.klantcontacten import (
    BetrokkeneForeignKeySerializer,
)

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
            "uuid": {"required": True},
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


class PartijSerializer(serializers.HyperlinkedModelSerializer):
    betrokkene = BetrokkeneForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Betrokkene bij klantcontact die een partij was."),
    )
    digitaal_adres = DigitaalAdresForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_(
            "Digitaal adres dat een partij verstrekte voor gebruik bij "
            "toekomstig contact met de gemeente."
        ),
    )
    voorkeurs_digitaal_adres = DigitaalAdresForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_(
            "Digitaal adres waarop een partij bij voorkeur door de gemeente benaderd wordt."
        ),
    )
    vertegenwoordigde = PartijForeignKeySerializer(
        required=True,
        allow_null=False,
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

    class Meta(serializers.HyperlinkedModelSerializer):
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


class OrganisatieForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisatie
        fields = (
            "id",
            "url",
            "naam",
        )
        extra_kwargs = {
            "id": {"required": True},
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


class PersoonContactSerializer(GegevensGroepSerializer):
    class Meta:
        model = Persoon
        gegevensgroep = "contactnaam"


class PersoonSerializer(serializers.HyperlinkedModelSerializer):
    partij = PartijForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie waarmee de gemeente een relatie heeft."),
    )
    contact = PersoonContactSerializer(
        required=False,
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
            "contact",
        )

    extra_kwargs = {
        "id": {"read_only": True},
        "url": {
            "view_name": "persoon-detail",
            "lookup_field": "id",
            "help_text": "De unieke URL van dit persoon binnen deze API.",
        },
    }


class ContactpersoonPersoonSerializer(GegevensGroepSerializer):
    class Meta:
        model = Contactpersoon
        gegevensgroep = "contactnaam"


class ContactpersoonSerializer(serializers.HyperlinkedModelSerializer):
    partij = PartijForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie waarmee de gemeente een relatie heeft."),
    )
    organisatie = OrganisatieForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Organisatie waarvoor een contactpersoon werkte."),
    )
    contact = ContactpersoonPersoonSerializer(
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
            "contact",
        )

    extra_kwargs = {
        "id": {"read_only": True},
        "url": {
            "view_name": "contactpersoon-detail",
            "lookup_field": "id",
            "help_text": "De unieke URL van dit contact persoon binnen deze API.",
        },
    }


class PartijIdentificatorGroepTypeSerializer(GegevensGroepSerializer):
    class Meta:
        model = PartijIdentificator
        gegevensgroep = "partij_identificator"


class PartijIdentificatorSerializer(serializers.HyperlinkedModelSerializer):
    partij = PartijForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Partij-identificator die hoorde bij een partij."),
    )
    partij_identificator = PartijIdentificatorGroepTypeSerializer(
        required=False,
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
