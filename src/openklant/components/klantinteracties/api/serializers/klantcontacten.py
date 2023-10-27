from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer

from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorForeignKeySerializer,
)
from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresForeignKeySerializer,
)
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Klantcontact,
)


class KlantcontactForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Klantcontact
        fields = (
            "uuid",
            "url",
            "nummer",
            "kanaal",
            "onderwerp",
        )
        read_only_fields = (
            "nummer",
            "kanaal",
            "onderwerp",
        )
        extra_kwargs = {
            "uuid": {"required": True},
            "url": {
                "view_name": "klantcontact-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van dit klantcontact binnen deze API.",
            },
        }


class KlantcontactSerializer(serializers.HyperlinkedModelSerializer):
    actoren = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Actor die bij een klantcontact betrokken was."),
    )

    class Meta:
        model = Klantcontact
        fields = (
            "uuid",
            "url",
            "nummer",
            "kanaal",
            "onderwerp",
            "actoren",
            "inhoud",
            "indicatie_contact_gelukt",
            "taal",
            "vertrouwelijk",
            "plaatsgevonden_op",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantcontact-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van dit klantcontact binnen deze API.",
            },
        }


class BetrokkeneForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Betrokkene
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True},
            "url": {
                "view_name": "betrokkene-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze betrokkene binnen deze API.",
            },
        }


class BezoekadresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Betrokkene
        gegevensgroep = "bezoekadres"


class CorrespondentieadresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Betrokkene
        gegevensgroep = "correspondentieadres"
        ref_name = "betrokkene correspondentieadres"


class ContactnaamSerializer(GegevensGroepSerializer):
    class Meta:
        model = Betrokkene
        gegevensgroep = "contactnaam"


class BetrokkeneSerializer(serializers.HyperlinkedModelSerializer):
    klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie die betrokken was bij een klantcontact."),
    )
    digitaal_adres = DigitaalAdresForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Digitaal adres dat een betrokkene bij klantcontact verstrekte "
            "voor gebruik bij opvolging van een klantcontact."
        ),
    )

    bezoekadres = BezoekadresSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Adres waarop de betrokkene bij klantcontact in naar aanleiding "
            "van dat contact af te leggen bezoeken wil ontvangen. Dit mag "
            "afwijken van voor de verstrekker eventueel in een basisregistratie bekende adressen."
        ),
    )
    correspondentieadres = CorrespondentieadresSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Adres waarop de betrokkene bij klantcontact naar aanleiding van "
            "dat contact te versturen post wil ontvangen. Dit mag afwijken van "
            "voor de verstrekker eventueel in een basisregistratie bekende adressen."
        ),
    )
    contactnaam = ContactnaamSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Naam die de betrokkene bij klantcontact tijdens vervolghandelingen naar "
            "aanleiding van dat contact wil gebruiken. Deze mag afwijken van eventueel "
            "in de Basisregistratie Personen (BRP) bekende naam van de betrokkene."
        ),
    )

    class Meta:
        model = Betrokkene
        fields = (
            "uuid",
            "url",
            "klantcontact",
            "digitaal_adres",
            "bezoekadres",
            "correspondentieadres",
            "contactnaam",
            "rol",
            "organisatienaam",
            "initiator",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "betrokkene-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze betrokkene binnen deze API.",
            },
        }
