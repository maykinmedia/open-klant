import logging

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from vng_api_common.serializers import add_choice_values_help_text
from vng_api_common.validators import IsImmutableValidator, URLValidator

from openklant.components.contactmomenten.datamodel.constants import ObjectTypes
from openklant.components.contactmomenten.datamodel.models import (
    ContactMoment,
    KlantContactMoment,
    Medewerker,
    ObjectContactMoment,
)
from openklant.utils.serializers import ExpandSerializer

from .validators import ObjectContactMomentCreateValidator

logger = logging.getLogger(__name__)


class MedewerkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medewerker
        fields = (
            "identificatie",
            "achternaam",
            "voorletters",
            "voorvoegsel_achternaam",
        )


class ObjectContactMomentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ObjectContactMoment
        fields = ("url", "contactmoment", "object", "object_type")
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "contactmoment": {
                "lookup_field": "uuid",
                "validators": [IsImmutableValidator()],
            },
            "object": {
                "validators": [IsImmutableValidator()],
                "min_length": 1,
                "max_length": 1000,
            },
            "object_type": {"validators": [IsImmutableValidator()]},
        }
        validators = [ObjectContactMomentCreateValidator()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(ObjectTypes)
        self.fields["object_type"].help_text += f"\n\n{value_display_mapping}"

        if not hasattr(self, "initial_data"):
            return


class KlantContactMomentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KlantContactMoment
        fields = (
            "url",
            "contactmoment",
            "klant",
            "rol",
            "gelezen",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "contactmoment": {"lookup_field": "uuid"},
            "klant": {"validators": [URLValidator()]},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=KlantContactMoment.objects.all(),
                fields=["contactmoment", "klant", "rol"],
            ),
        ]


class ContactMomentSerializer(serializers.HyperlinkedModelSerializer):
    medewerker_identificatie = MedewerkerSerializer(required=False, allow_null=True)
    klantcontactmomenten = ExpandSerializer(
        name="klantcontactmomenten",
        source="klantcontactmoment_set",
        default_serializer=NestedHyperlinkedRelatedField,
        expanded_serializer=KlantContactMomentSerializer,
        many=True,
        read_only=True,
        common_kwargs={
            "read_only": True,
        },
        default_serializer_kwargs={
            "lookup_field": "uuid",
            "view_name": "klantcontactmoment-detail",
        },
        help_text=_("Lijst met URLs van gerelateerde KLANTCONTACTMOMENTen"),
    )
    objectcontactmomenten = ExpandSerializer(
        name="objectcontactmomenten",
        source="objectcontactmoment_set",
        default_serializer=NestedHyperlinkedRelatedField,
        expanded_serializer=ObjectContactMomentSerializer,
        many=True,
        read_only=True,
        common_kwargs={
            "read_only": True,
        },
        default_serializer_kwargs={
            "lookup_field": "uuid",
            "view_name": "objectcontactmoment-detail",
        },
        help_text=_("Lijst met URLs van gerelateerde OBJECTCONTACTMOMENTen"),
    )

    class Meta:
        model = ContactMoment
        fields = (
            "url",
            "vorig_contactmoment",
            "volgend_contactmoment",
            "bronorganisatie",
            "registratiedatum",
            "kanaal",
            "voorkeurskanaal",
            "voorkeurstaal",
            "tekst",
            "onderwerp_links",
            "initiatiefnemer",
            "medewerker",
            "medewerker_identificatie",
            "klantcontactmomenten",
            "objectcontactmomenten",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "vorig_contactmoment": {"lookup_field": "uuid"},
            "volgend_contactmoment": {
                "lookup_field": "uuid",
                "read_only": True,
                "allow_null": True,
                "help_text": _("URL-referentie naar het volgende CONTACTMOMENT."),
            },
        }
        expandable_fields = ["klantcontactmomenten", "objectcontactmomenten"]

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)

        medewerker = validated_attrs.get("medewerker", None)
        medewerker_identificatie = validated_attrs.get("medewerker_identificatie", None)

        if self.instance:
            medewerker = medewerker or self.instance.medewerker
            medewerker_identificatie = medewerker_identificatie or getattr(
                self.instance, "medewerker_identificatie", None
            )

        if not medewerker and not medewerker_identificatie:
            raise serializers.ValidationError(
                _("medewerker or medewerkerIdentificatie must be provided"),
                code="invalid-medewerker",
            )

        return validated_attrs

    def create(self, validated_data):
        medewerker_identificatie_data = validated_data.pop(
            "medewerker_identificatie", None
        )
        contactmoment = super().create(validated_data)

        if medewerker_identificatie_data:
            medewerker_identificatie_data["contactmoment"] = contactmoment
            MedewerkerSerializer().create(medewerker_identificatie_data)

        return contactmoment

    def update(self, instance, validated_data):
        medewerker_identificatie_data = validated_data.pop(
            "medewerker_identificatie", None
        )
        contactmoment = super().update(instance, validated_data)

        if medewerker_identificatie_data:
            if hasattr(contactmoment, "medewerker_identificatie"):
                MedewerkerSerializer().update(
                    contactmoment.medewerker_identificatie,
                    medewerker_identificatie_data,
                )
            else:
                medewerker_identificatie_data["contactmoment"] = contactmoment
                MedewerkerSerializer().create(medewerker_identificatie_data)

        return contactmoment
