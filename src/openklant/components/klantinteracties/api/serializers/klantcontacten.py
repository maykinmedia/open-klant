from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorForeignKeySerializer,
)
from openklant.components.klantinteracties.api.serializers.constants import (
    SERIALIZER_PATH,
)
from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresForeignKeySerializer,
)
from openklant.components.klantinteracties.api.validators import (
    betrokkene_exists,
    bijlage_exists,
    klantcontact_exists,
    onderwerpobject_exists,
)
from openklant.components.klantinteracties.models.actoren import Actor
from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Bijlage,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.klantinteracties.models.partijen import Partij


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
                "view_name": "klantinteracties:betrokkene-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze betrokkene binnen deze API."),
            },
        }


class KlantcontactForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Klantcontact
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [klantcontact_exists]},
            "url": {
                "view_name": "klantinteracties:klantcontact-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van dit klantcontact binnen deze API."),
            },
        }


class OnderwerpobjectForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Onderwerpobject
        fields = (
            "uuid",
            "url",
        )

        extra_kwargs = {
            "uuid": {"required": True, "validators": [onderwerpobject_exists]},
            "url": {
                "view_name": "klantinteracties:onderwerpobject-detail",
                "lookup_field": "uuid",
                "help_text": _(
                    "De unieke URL van dit onderwerp object binnen deze API."
                ),
            },
        }


class BijlageForeignKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bijlage
        fields = (
            "uuid",
            "url",
        )

        extra_kwargs = {
            "uuid": {"required": True, "validators": [bijlage_exists]},
            "url": {
                "view_name": "klantinteracties:bijlage-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze bijlage binnen deze API."),
            },
        }


class BetrokkeneForeignkeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Betrokkene
        fields = (
            "uuid",
            "url",
        )
        extra_kwargs = {
            "uuid": {"required": True, "validators": [betrokkene_exists]},
            "url": {
                "view_name": "klantinteracties:betrokkene-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze betrokkene binnen deze API."),
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
        ref_name = "BetrokkeneCorrespondentieadres"


class ContactnaamSerializer(GegevensGroepSerializer):
    class Meta:
        model = Betrokkene
        gegevensgroep = "contactnaam"


class BetrokkeneSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    from openklant.components.klantinteracties.api.serializers.partijen import (
        PartijForeignKeySerializer,
    )

    was_partij = PartijForeignKeySerializer(
        required=True,
        allow_null=True,
        source="partij",
        help_text=_("Betrokkene bij klantcontact die een partij was."),
    )
    had_klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie die betrokken was bij een klantcontact."),
        source="klantcontact",
    )
    digitale_adressen = DigitaalAdresForeignKeySerializer(
        read_only=True,
        help_text=_("Digitale adressen van de betrokkene bij klantcontact."),
        source="digitaaladres_set",
        many=True,
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
    volledige_naam = serializers.SerializerMethodField(
        help_text="De voledige naam van de betrokkene.",
    )

    class Meta:
        model = Betrokkene
        fields = (
            "uuid",
            "url",
            "was_partij",
            "had_klantcontact",
            "digitale_adressen",
            "bezoekadres",
            "correspondentieadres",
            "contactnaam",
            "volledige_naam",
            "rol",
            "organisatienaam",
            "initiator",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:betrokkene-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van deze betrokkene binnen deze API."),
            },
        }

    def get_volledige_naam(self, obj):
        return obj.get_full_name()

    @transaction.atomic
    def update(self, instance, validated_data):
        if "partij" in validated_data:
            if partij := validated_data.pop("partij", None):
                partij = Partij.objects.get(uuid=str(partij.get("uuid")))

            validated_data["partij"] = partij

        if "klantcontact" in validated_data:
            if klantcontact := validated_data.pop("klantcontact", None):
                validated_data["klantcontact"] = Klantcontact.objects.get(
                    uuid=str(klantcontact.get("uuid"))
                )

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        klantcontact_uuid = str(validated_data.pop("klantcontact").get("uuid"))
        validated_data["klantcontact"] = Klantcontact.objects.get(
            uuid=klantcontact_uuid
        )

        if partij := validated_data.pop("partij", None):
            partij = Partij.objects.get(uuid=str(partij.get("uuid")))

        validated_data["partij"] = partij

        return super().create(validated_data)


class KlantcontactSerializer(serializers.HyperlinkedModelSerializer):
    from openklant.components.klantinteracties.api.serializers.internetaken import (
        InterneTaakForeignKeySerializer,
    )

    had_betrokken_actoren = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Actor die bij een klantcontact betrokken was."),
        many=True,
        source="actoren",
    )
    ging_over_onderwerpobjecten = OnderwerpobjectForeignKeySerializer(
        read_only=True,
        source="onderwerpobject_set",
        help_text=_("Onderwerpobject dat tijdens een klantcontact aan de orde was."),
        many=True,
    )
    omvatte_bijlagen = BijlageForeignKeySerializer(
        read_only=True,
        source="bijlage_set",
        help_text=_(
            "Bijlage die (een deel van) de inhoud van het klantcontact beschrijft."
        ),
        many=True,
    )
    had_betrokkenen = BetrokkeneForeignkeySerializer(
        read_only=True,
        source="betrokkene_set",
        help_text=_("Persoon of organisatie die betrokken was bij een klantcontact."),
        many=True,
    )
    leidde_tot_interne_taken = InterneTaakForeignKeySerializer(
        read_only=True,
        source="internetaak_set",
        help_text=_("Klantcontact dat leidde tot een interne taak."),
        many=True,
    )

    inclusion_serializers = {
        # 1 level
        "had_betrokkenen": f"{SERIALIZER_PATH}.klantcontacten.BetrokkeneSerializer",
        "had_betrokken_actoren": f"{SERIALIZER_PATH}.actoren.ActorSerializer",
        "leidde_tot_interne_taken": f"{SERIALIZER_PATH}.internetaken.InterneTaakSerializer",
        "ging_over_onderwerpobjecten": f"{SERIALIZER_PATH}.klantcontacten.OnderwerpobjectSerializer",
        "omvatte_bijlagen": f"{SERIALIZER_PATH}.klantcontacten.BijlageSerializer",
        # 2 levels
        "had_betrokkenen.was_partij": f"{SERIALIZER_PATH}.partijen.PartijSerializer",
        "had_betrokkenen.digitale_adressen": f"{SERIALIZER_PATH}.digitaal_adres.DigitaalAdresSerializer",
    }

    class Meta:
        model = Klantcontact
        fields = (
            "uuid",
            "url",
            "ging_over_onderwerpobjecten",
            "omvatte_bijlagen",
            "had_betrokkenen",
            "leidde_tot_interne_taken",
            "nummer",
            "kanaal",
            "onderwerp",
            "had_betrokken_actoren",
            "inhoud",
            "indicatie_contact_gelukt",
            "taal",
            "vertrouwelijk",
            "plaatsgevonden_op",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:klantcontact-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van dit klantcontact binnen deze API."),
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "actoren" in validated_data:
            actoren = [
                str(actor.get("uuid")) for actor in validated_data.pop("actoren")
            ]
            validated_data["actoren"] = Actor.objects.filter(uuid__in=actoren)

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        actoren = [str(actor["uuid"]) for actor in validated_data.pop("actoren")]
        validated_data["actoren"] = Actor.objects.filter(uuid__in=actoren)

        return super().create(validated_data)


class OnderwerpobjectObjectidentificatorSerializer(GegevensGroepSerializer):
    class Meta:
        model = Onderwerpobject
        gegevensgroep = "objectidentificator"


class OnderwerpobjectSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_("'Klantcontact' ging over 'Onderwerpobject'"),
    )
    was_klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_("'Onderwerpobject' was 'Klantcontact'"),
    )
    objectidentificator = OnderwerpobjectObjectidentificatorSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Gegevens die een onderwerpobject in een extern register uniek "
            "identificeren."
        ),
    )

    class Meta:
        model = Onderwerpobject
        fields = (
            "uuid",
            "url",
            "klantcontact",
            "was_klantcontact",
            "objectidentificator",
        )

        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:klantcontact-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van dit klantcontact binnen deze API."),
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "klantcontact" in validated_data:
            if klantcontact := validated_data.pop("klantcontact", None):
                klantcontact = Klantcontact.objects.get(
                    uuid=str(klantcontact.get("uuid"))
                )

            validated_data["klantcontact"] = klantcontact

        if "was_klantcontact" in validated_data:
            if was_klantcontact := validated_data.pop("was_klantcontact", None):
                was_klantcontact = Klantcontact.objects.get(
                    uuid=str(was_klantcontact.get("uuid"))
                )

            validated_data["was_klantcontact"] = was_klantcontact

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        if klantcontact := validated_data.pop("klantcontact", None):
            klantcontact = Klantcontact.objects.get(uuid=str(klantcontact.get("uuid")))

        if was_klantcontact := validated_data.pop("was_klantcontact", None):
            was_klantcontact = Klantcontact.objects.get(
                uuid=str(was_klantcontact.get("uuid"))
            )

        validated_data["klantcontact"] = klantcontact
        validated_data["was_klantcontact"] = was_klantcontact

        return super().create(validated_data)


class BijlageObjectidentificatorSerializer(GegevensGroepSerializer):
    class Meta:
        model = Bijlage
        gegevensgroep = "objectidentificator"


class BijlageSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    was_bijlage_van_klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_("'Klantcontact' ging over 'Onderwerpobject'"),
        source="klantcontact",
    )
    objectidentificator = BijlageObjectidentificatorSerializer(
        required=False,
        allow_null=True,
        help_text=_(
            "Gegevens die een inhoudsobject in een extern register "
            "uniek identificeren."
        ),
    )

    class Meta:
        model = Bijlage
        fields = (
            "uuid",
            "url",
            "was_bijlage_van_klantcontact",
            "objectidentificator",
        )

        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:klantcontact-detail",
                "lookup_field": "uuid",
                "help_text": _("De unieke URL van dit klantcontact binnen deze API."),
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "klantcontact" in validated_data:
            if klantcontact := validated_data.pop("klantcontact", None):
                klantcontact = Klantcontact.objects.get(
                    uuid=str(klantcontact.get("uuid"))
                )
            validated_data["klantcontact"] = klantcontact

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        if klantcontact := validated_data.pop("klantcontact", None):
            validated_data["klantcontact"] = Klantcontact.objects.get(
                uuid=str(klantcontact.get("uuid"))
            )

        return super().create(validated_data)
