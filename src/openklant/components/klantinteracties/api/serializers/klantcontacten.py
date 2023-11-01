from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorForeignKeySerializer,
)
from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresForeignKeySerializer,
)
from openklant.components.klantinteracties.api.validators import (
    betrokkene_exists,
    klantcontact_exists,
)
from openklant.components.klantinteracties.models.actoren import Actor
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
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
            "uuid": {"required": True, "validators": [klantcontact_exists]},
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
        many=True,
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

    @transaction.atomic
    def update(self, instance, validated_data):
        actoren = [
            str(actor.get("uuid"))
            for actor in validated_data.pop(
                "actoren", instance.actoren.all().values("uuid")
            )
        ]
        validated_data["actoren"] = Actor.objects.filter(uuid__in=actoren)

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        actoren = [str(actor["uuid"]) for actor in validated_data.pop("actoren")]
        validated_data["actoren"] = Actor.objects.filter(uuid__in=actoren)

        return super().create(validated_data)


class BetrokkeneForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Betrokkene
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [betrokkene_exists]},
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


class BetrokkeneSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie die betrokken was bij een klantcontact."),
    )
    digitaal_adres = DigitaalAdresForeignKeySerializer(
        required=True,
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

    @transaction.atomic
    def update(self, instance, validated_data):
        if klantcontact := validated_data.pop("klantcontact", None):
            validated_data["klantcontact"] = Klantcontact.objects.get(
                uuid=str(klantcontact.get("uuid"))
            )

        if validated_data.get("digitaal_adres"):
            if digitaal_adres := validated_data.pop("digitaal_adres", None):
                validated_data["digitaal_adres"] = DigitaalAdres.objects.get(
                    uuid=str(digitaal_adres.get("uuid"))
                )

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        klantcontact_uuid = str(validated_data.pop("klantcontact").get("uuid"))
        digitaal_adres_uuid = str(validated_data.pop("digitaal_adres").get("uuid"))

        validated_data["klantcontact"] = Klantcontact.objects.get(
            uuid=klantcontact_uuid
        )
        validated_data["digitaal_adres"] = DigitaalAdres.objects.get(
            uuid=digitaal_adres_uuid
        )

        return super().create(validated_data)
