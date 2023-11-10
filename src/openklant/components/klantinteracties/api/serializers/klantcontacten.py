from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorForeignKeySerializer,
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
                "view_name": "klantcontact-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van dit klantcontact binnen deze API.",
            },
        }


class BetrokkeneBaseSerializer(
    NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer
):
    from openklant.components.klantinteracties.api.serializers.partijen import (
        KlantcontactPartijSerializer,
    )

    partij = KlantcontactPartijSerializer(
        required=True,
        allow_null=True,
        source="partij_set",
        help_text=_("Betrokkene bij klantcontact die een partij was."),
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

    class Meta:
        model = Betrokkene
        fields = (
            "uuid",
            "url",
            "partij",
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

    # TODO: remove this code and create update suport for partij
    def get_fields(self, *args, **kwargs):
        fields = super(BetrokkeneBaseSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get("request", None)
        if request and getattr(request, "method", None) in ["PUT", "PATCH"]:
            fields["partij"].required = False
            fields["partij"].read_only = True
        return fields

    @transaction.atomic
    def update(self, instance, validated_data):
        if "klantcontact" in validated_data:
            if klantcontact := validated_data.pop("klantcontact", None):
                validated_data["klantcontact"] = Klantcontact.objects.get(
                    uuid=str(klantcontact.get("uuid"))
                )

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        from openklant.components.klantinteracties.api.serializers.partijen import (
            PartijSerializer,
        )

        klantcontact_uuid = str(validated_data.pop("klantcontact").get("uuid"))
        partijen = validated_data.pop("partij_set")

        validated_data["klantcontact"] = Klantcontact.objects.get(
            uuid=klantcontact_uuid
        )

        betrokkene = super().create(validated_data)

        if partijen:
            linked_parijen = []
            for partij in partijen:
                partij["betrokkene"] = {"uuid": betrokkene.uuid}
                linked_parijen.append(partij)

            serializer = PartijSerializer(
                data=linked_parijen, context=self.context, many=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return betrokkene


class BetrokkeneSerializer(BetrokkeneBaseSerializer):
    klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Persoon of organisatie die betrokken was bij een klantcontact."),
    )

    class Meta(BetrokkeneBaseSerializer.Meta):
        fields = BetrokkeneBaseSerializer.Meta.fields + ("klantcontact",)


class BetrokkeneKlantcontactSerializer(BetrokkeneBaseSerializer):
    klantcontact = KlantcontactForeignKeySerializer(
        read_only=True,
        allow_null=False,
        help_text=_("Persoon of organisatie die betrokken was bij een klantcontact."),
    )

    class Meta(BetrokkeneBaseSerializer.Meta):
        fields = BetrokkeneBaseSerializer.Meta.fields + ("klantcontact",)


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
                "view_name": "onderwerpobject-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van dit onderwerp object binnen deze API.",
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
                "view_name": "bijlage-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze bijlage binnen deze API.",
            },
        }


class KlantcontactSerializer(serializers.HyperlinkedModelSerializer):
    from openklant.components.klantinteracties.api.serializers.internetaken import (
        KlantcontactInterneTaakSerializer,
    )

    actoren = ActorForeignKeySerializer(
        required=True,
        allow_null=False,
        help_text=_("Actor die bij een klantcontact betrokken was."),
        many=True,
    )
    ging_over_onderwerpobject = OnderwerpobjectForeignKeySerializer(
        required=True,
        allow_null=True,
        source="onderwerpobject_set",
        help_text=_("Onderwerpobject dat tijdens een klantcontact aan de orde was."),
        many=True,
    )
    omvatte_bijlagen = BijlageForeignKeySerializer(
        required=True,
        allow_null=True,
        source="bijlage_set",
        help_text=_(
            "Bijlage die (een deel van) de inhoud van het klantcontact beschrijft."
        ),
        many=True,
    )

    # TODO: change to inline resource for update
    had_betrokkene = BetrokkeneKlantcontactSerializer(
        required=True,
        allow_null=True,
        source="betrokkene_set",
        help_text=_("Persoon of organisatie die betrokken was bij een klantcontact."),
        many=True,
    )
    # TODO: change to inline resource for update
    leide_tot_interne_taken = KlantcontactInterneTaakSerializer(
        required=True,
        allow_null=True,
        source="internetaak_set",
        help_text=_("Klantcontact dat leidde tot een interne taak."),
        many=True,
    )

    class Meta:
        model = Klantcontact
        fields = (
            "uuid",
            "url",
            "ging_over_onderwerpobject",
            "omvatte_bijlagen",
            "had_betrokkene",
            "leide_tot_interne_taken",
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

    # TODO: remove this code and create update suport for interne taken
    def get_fields(self, *args, **kwargs):
        fields = super(KlantcontactSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get("request", None)
        if request and getattr(request, "method", None) in ["PUT", "PATCH"]:
            fields["leide_tot_interne_taken"].required = False
            fields["leide_tot_interne_taken"].read_only = True

            fields["had_betrokkene"].required = False
            fields["had_betrokkene"].read_only = True
        return fields

    @transaction.atomic
    def update(self, instance, validated_data):
        if "actoren" in validated_data:
            actoren = [
                str(actor.get("uuid")) for actor in validated_data.pop("actoren")
            ]
            validated_data["actoren"] = Actor.objects.filter(uuid__in=actoren)

        if "bijlage_set" in validated_data:
            existing_bijlagen = instance.bijlage_set.all()
            bijlagen_uuids = [
                bijlage["uuid"] for bijlage in validated_data.pop("bijlage_set")
            ]

            # unset relation of bijlage that weren't given with the update
            for bijlage in existing_bijlagen:
                if bijlage.uuid not in bijlagen_uuids:
                    bijlage.klantcontact = None
                    bijlage.save()

            # create relation between bijlage and klantcontact of new entries
            for bijlage_uuid in bijlagen_uuids:
                if bijlage_uuid not in existing_bijlagen.values_list("uuid", flat=True):
                    bijlage = Bijlage.objects.get(uuid=bijlage_uuid)
                    bijlage.klantcontact = instance
                    bijlage.save()

        if "onderwerpobject_set" in validated_data:
            existing_onderwerpobjecten = instance.onderwerpobject_set.all()
            onderwerpobjecten_uuids = [
                onderwerpobject["uuid"]
                for onderwerpobject in validated_data.pop("onderwerpobject_set")
            ]

            # unset relation of onderwerpobject that weren't given with the update
            for onderwerpobject in existing_onderwerpobjecten:
                if onderwerpobject.uuid not in onderwerpobjecten_uuids:
                    onderwerpobject.klantcontact = None
                    onderwerpobject.save()

            # create relation between onderwerpobject and klantcontact of new entries
            for onderwerpobject_uuid in onderwerpobjecten_uuids:
                if onderwerpobject_uuid not in existing_onderwerpobjecten.values_list(
                    "uuid", flat=True
                ):
                    onderwerpobject = Onderwerpobject.objects.get(
                        uuid=onderwerpobject_uuid
                    )
                    onderwerpobject.klantcontact = instance
                    onderwerpobject.save()

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        from openklant.components.klantinteracties.api.serializers.internetaken import (
            InterneTaakSerializer,
        )

        betrokkenen = validated_data.pop("betrokkene_set")
        internetaken = validated_data.pop("internetaak_set")
        bijlagen = validated_data.pop("bijlage_set")
        onderwerpobjecten = validated_data.pop("onderwerpobject_set")

        actoren = [str(actor["uuid"]) for actor in validated_data.pop("actoren")]
        validated_data["actoren"] = Actor.objects.filter(uuid__in=actoren)

        klantcontact = super().create(validated_data)

        if internetaken:
            linked_internetaken = []
            for internetaak in internetaken:
                internetaak["klantcontact"] = {"uuid": str(klantcontact.uuid)}
                linked_internetaken.append(internetaak)

            serializer = InterneTaakSerializer(
                data=linked_internetaken, context=self.context, many=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        if betrokkenen:
            linked_betrokkene = []
            for betrokkene in betrokkenen:
                betrokkene["partij"] = betrokkene.pop("partij_set", [])
                betrokkene["klantcontact"] = {"uuid": str(klantcontact.uuid)}
                linked_betrokkene.append(betrokkene)

            serializer = BetrokkeneSerializer(
                data=linked_betrokkene, context=self.context, many=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        if onderwerpobjecten:
            for index, onderwerpobject in enumerate(onderwerpobjecten):
                onderwerpobject = Onderwerpobject.objects.get(
                    uuid=str(onderwerpobject["uuid"])
                )
                if onderwerpobject.klantcontact:
                    raise serializers.ValidationError(
                        {
                            f"gingOverOnderwerpobject.{index}.uuid": _(
                                "Onderwerpobject object already is linked to a klantcontact object."
                            )
                        }
                    )
                onderwerpobject.klantcontact = klantcontact
                onderwerpobject.save()

        if bijlagen:
            for index, bijlage in enumerate(bijlagen):
                bijlage = Bijlage.objects.get(uuid=str(bijlage["uuid"]))
                if bijlage.klantcontact:
                    raise serializers.ValidationError(
                        {
                            f"omvatteBijlagen.{index}.uuid": _(
                                "Bijlage object already is linked to a klantcontact object."
                            )
                        }
                    )
                bijlage.klantcontact = klantcontact
                bijlage.save()

        return klantcontact


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
                "view_name": "klantcontact-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van dit klantcontact binnen deze API.",
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
    klantcontact = KlantcontactForeignKeySerializer(
        required=True,
        allow_null=True,
        help_text=_("'Klantcontact' ging over 'Onderwerpobject'"),
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
            "klantcontact",
            "objectidentificator",
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
