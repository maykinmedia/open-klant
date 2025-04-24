from django.db import transaction
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorForeignKeySerializer,
    ActorSerializer,
)
from openklant.components.klantinteracties.api.serializers.constants import (
    SERIALIZER_PATH,
)
from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresForeignKeySerializer,
)
from openklant.components.klantinteracties.api.validators import (
    FKUniqueTogetherValidator,
    betrokkene_exists,
    bijlage_exists,
    klantcontact_exists,
    onderwerpobject_exists,
)
from openklant.components.klantinteracties.models.actoren import (
    Actor,
    ActorKlantcontact,
)
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


class BezoekadresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Betrokkene
        gegevensgroep = "bezoekadres"
        extra_kwargs = {
            "huisnummer": {
                "allow_null": True,
            }
        }


class CorrespondentieadresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Betrokkene
        gegevensgroep = "correspondentieadres"
        ref_name = "BetrokkeneCorrespondentieadres"
        extra_kwargs = {
            "huisnummer": {
                "allow_null": True,
            }
        }


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
        required=False,
        allow_null=True,
        source="partij",
        help_text=_("Betrokkene bij klantcontact die een partij was."),
    )
    had_klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_(
            "Het klantcontact waar deze persoon of organisatie bij betrokken was."
        ),
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

    inclusion_serializers = {
        "digitale_adressen": f"{SERIALIZER_PATH}.digitaal_adres.DigitaalAdresSerializer",
    }

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

    def get_volledige_naam(self, obj) -> str:
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

    had_betrokken_actoren = serializers.SerializerMethodField(
        help_text=_("Actor die bij een klantcontact betrokken was."),
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
    had_betrokkenen = BetrokkeneForeignKeySerializer(
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
            "had_betrokken_actoren",
            "omvatte_bijlagen",
            "had_betrokkenen",
            "leidde_tot_interne_taken",
            "nummer",
            "kanaal",
            "onderwerp",
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

    @extend_schema_field(ActorSerializer(many=True))
    def get_had_betrokken_actoren(self, obj):
        return [
            ActorSerializer(actor_klantcontact.actor, context=self.context).data
            for actor_klantcontact in obj.actorklantcontact_set.all()
            if actor_klantcontact
        ]


class OnderwerpobjectidentificatorSerializer(GegevensGroepSerializer):
    class Meta:
        model = Onderwerpobject
        gegevensgroep = "onderwerpobjectidentificator"


class OnderwerpobjectSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    klantcontact = KlantcontactForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_("'Klantcontact' ging over 'Onderwerpobject'"),
    )
    was_klantcontact = KlantcontactForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_("'Onderwerpobject' was 'Klantcontact'"),
    )
    onderwerpobjectidentificator = OnderwerpobjectidentificatorSerializer(
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
            "onderwerpobjectidentificator",
        )

        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:onderwerpobject-detail",
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


class BijlageIdentificatorSerializer(GegevensGroepSerializer):
    class Meta:
        model = Bijlage
        gegevensgroep = "bijlageidentificator"


class BijlageSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    was_bijlage_van_klantcontact = KlantcontactForeignKeySerializer(
        required=False,
        allow_null=True,
        help_text=_("'Klantcontact' ging over 'Onderwerpobject'"),
        source="klantcontact",
    )
    bijlageidentificator = BijlageIdentificatorSerializer(
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
            "bijlageidentificator",
        )

        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:bijlage-detail",
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


class ActorKlantcontactSerializer(serializers.HyperlinkedModelSerializer):
    actor = ActorForeignKeySerializer(
        required=True,
        help_text=_("De gekoppelde 'Actor'."),
    )
    klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        help_text=_("De gekoppelde 'Klantcontact'."),
    )

    class Meta:
        model = ActorKlantcontact
        fields = (
            "uuid",
            "url",
            "actor",
            "klantcontact",
        )
        validators = [
            FKUniqueTogetherValidator(
                queryset=ActorKlantcontact.objects.all(),
                fields=(
                    "actor",
                    "klantcontact",
                ),
            )
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "klantinteracties:actorklantcontact-detail",
                "lookup_field": "uuid",
                "help_text": _(
                    "De unieke URL van deze actor klantcontact binnen deze API."
                ),
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if "actor" in validated_data:
            if actor := validated_data.pop("actor", None):
                actor = Actor.objects.get(uuid=str(actor.get("uuid")))

            validated_data["actor"] = actor

        if "klantcontact" in validated_data:
            if klantcontact := validated_data.pop("klantcontact", None):
                validated_data["klantcontact"] = Klantcontact.objects.get(
                    uuid=str(klantcontact.get("uuid"))
                )

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        actor_uuid = str(validated_data.pop("actor").get("uuid"))
        validated_data["actor"] = Actor.objects.get(uuid=actor_uuid)

        klantcontact_uuid = str(validated_data.pop("klantcontact").get("uuid"))
        validated_data["klantcontact"] = Klantcontact.objects.get(
            uuid=klantcontact_uuid
        )

        return super().create(validated_data)


class BetrokkeneKlantcontactReadOnlySerializer(BetrokkeneSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["had_klantcontact"].read_only = True


class OnderwerpobjectKlantcontactReadOnlySerializer(OnderwerpobjectSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["klantcontact"].read_only = True


class MaakKlantcontactSerializer(serializers.Serializer):
    klantcontact = KlantcontactSerializer()
    betrokkene = BetrokkeneKlantcontactReadOnlySerializer(required=False)
    onderwerpobject = OnderwerpobjectKlantcontactReadOnlySerializer(required=False)

    @transaction.atomic
    def create(self, validated_data):
        """
        Create the objects and use the original serializers to ensure all the correct
        fields show up in the response
        """
        klantcontact_data = validated_data["klantcontact"]
        klantcontact = Klantcontact.objects.create(**klantcontact_data)

        betrokkene = None
        if betrokkene_data := validated_data.pop("betrokkene", None):
            betrokkene_data["had_klantcontact"] = {"uuid": str(klantcontact.uuid)}
            betrokkene_data.setdefault(
                "was_partij", betrokkene_data.get("partij", None)
            )
            betrokkene_serializer = BetrokkeneSerializer(data=betrokkene_data)
            betrokkene_serializer.is_valid()
            betrokkene = betrokkene_serializer.save()

        onderwerpobject = None
        if onderwerpobject_data := validated_data.pop("onderwerpobject", None):
            onderwerpobject_data["klantcontact"] = {"uuid": str(klantcontact.uuid)}
            onderwerpobject_data.setdefault("was_klantcontact", None)
            onderwerpobject_serializer = OnderwerpobjectSerializer(
                data=onderwerpobject_data
            )
            onderwerpobject_serializer.is_valid()
            onderwerpobject = onderwerpobject_serializer.save()

        return {
            "klantcontact": klantcontact,
            "betrokkene": betrokkene,
            "onderwerpobject": onderwerpobject,
        }
