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
from openklant.components.klantinteracties.models.internetaken import InterneTaak
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
                "help_text": "De unieke URL van deze betrokkene binnen deze API.",
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
                "help_text": "De unieke URL van dit klantcontact binnen deze API.",
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
                "view_name": "klantinteracties:bijlage-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze bijlage binnen deze API.",
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
            "was_partij",
            "had_klantcontact",
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
                "view_name": "klantinteracties:betrokkene-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze betrokkene binnen deze API.",
            },
        }

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

        if "partij_set" in validated_data:
            existing_partijen = instance.partij_set.all()
            partij_uuids = [
                partij["uuid"] for partij in validated_data.pop("partij_set")
            ]

            # unset relation of partij that weren't given with the update
            for partij in existing_partijen:
                if partij.uuid not in partij_uuids:
                    partij.betrokkene = None
                    partij.save()

            # create relation between partij and betrokkene of new entries
            for partij_uuid in partij_uuids:
                if partij_uuid not in existing_partijen.values_list("uuid", flat=True):
                    partij = Partij.objects.get(uuid=partij_uuid)
                    partij.betrokkene = instance
                    partij.save()

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
    had_betrokkenen = BetrokkeneForeignkeySerializer(
        required=True,
        allow_null=True,
        source="betrokkene_set",
        help_text=_("Persoon of organisatie die betrokken was bij een klantcontact."),
        many=True,
    )
    leidde_tot_interne_taken = InterneTaakForeignKeySerializer(
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
                "help_text": "De unieke URL van dit klantcontact binnen deze API.",
            },
        }

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

        if "betrokkene_set" in validated_data:
            existing_betrokkene = instance.betrokkene_set.all()
            betrokkene_uuids = [
                betrokkene["uuid"]
                for betrokkene in validated_data.pop("betrokkene_set")
            ]

            # delete relation of betrokkene that weren't given with the update
            for betrokkene in existing_betrokkene:
                if betrokkene.uuid not in betrokkene_uuids:
                    betrokkene.delete()

            # create relation between betrokkene and klantcontact of new entries
            for betrokkene_uuid in betrokkene_uuids:
                if betrokkene_uuid not in existing_betrokkene.values_list(
                    "uuid", flat=True
                ):
                    betrokkene = Betrokkene.objects.get(uuid=betrokkene_uuid)
                    betrokkene.klantcontact = instance
                    betrokkene.save()

        if "internetaak_set" in validated_data:
            existing_internetaken = instance.internetaak_set.all()
            internetaak_uuids = [
                internetaak["uuid"]
                for internetaak in validated_data.pop("internetaak_set")
            ]

            # delete relation of internetaak that weren't given with the update
            for internetaak in existing_internetaken:
                if internetaak.uuid not in internetaak_uuids:
                    internetaak.delete()

            # create relation between internetaak and klantcontact of new entries
            for internetaak_uuid in internetaak_uuids:
                if internetaak_uuid not in existing_internetaken.values_list(
                    "uuid", flat=True
                ):
                    internetaak = InterneTaak.objects.get(uuid=internetaak_uuid)
                    internetaak.klantcontact = instance
                    internetaak.save()

        return super().update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        betrokkenen = validated_data.pop("betrokkene_set")
        internetaken = validated_data.pop("internetaak_set")
        bijlagen = validated_data.pop("bijlage_set")
        onderwerpobjecten = validated_data.pop("onderwerpobject_set")

        actoren = [str(actor["uuid"]) for actor in validated_data.pop("actoren")]
        validated_data["actoren"] = Actor.objects.filter(uuid__in=actoren)

        klantcontact = super().create(validated_data)

        if onderwerpobjecten:
            for index, onderwerpobject in enumerate(onderwerpobjecten):
                onderwerpobject = Onderwerpobject.objects.get(
                    uuid=str(onderwerpobject["uuid"])
                )
                if onderwerpobject.klantcontact:
                    raise serializers.ValidationError(
                        {
                            f"gingOverOnderwerpobjecten.{index}.uuid": _(
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

        if betrokkenen:
            for betrokkene in betrokkenen:
                betrokkene = Betrokkene.objects.get(uuid=str(betrokkene["uuid"]))
                betrokkene.klantcontact = klantcontact
                betrokkene.save()

        if internetaken:
            for internetaak in internetaken:
                internetaak = InterneTaak.objects.get(uuid=str(internetaak["uuid"]))
                internetaak.klantcontact = klantcontact
                internetaak.save()

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
                "view_name": "klantinteracties:klantcontact-detail",
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
