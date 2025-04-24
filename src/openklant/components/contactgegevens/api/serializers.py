from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import GegevensGroepSerializer, NestedGegevensGroepMixin

from openklant.components.contactgegevens.models import Organisatie, Persoon


class OrganisatieAdresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Organisatie
        gegevensgroep = "adres"
        extra_kwargs = {
            "huisnummer": {
                "allow_null": True,
            }
        }


class OrganisatieSerializer(
    NestedGegevensGroepMixin,
    serializers.HyperlinkedModelSerializer,
):
    adres = OrganisatieAdresSerializer(
        required=False,
        allow_null=True,
        help_text=_("De adres gegevens van een organisatie."),
    )

    class Meta:
        model = Organisatie
        fields = (
            "uuid",
            "url",
            "handelsnaam",
            "oprichtingsdatum",
            "opheffingsdatum",
            "adres",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "contactgegevens:organisatie-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze actor binnen deze API.",
            },
        }


class PersoonAdresSerializer(GegevensGroepSerializer):
    class Meta:
        model = Persoon
        gegevensgroep = "adres"
        extra_kwargs = {
            "huisnummer": {
                "allow_null": True,
            }
        }


class PersoonSerializer(
    NestedGegevensGroepMixin,
    serializers.HyperlinkedModelSerializer,
):
    adres = PersoonAdresSerializer(
        required=False,
        allow_null=True,
        help_text=_("De adres gegevens van een organisatie."),
    )

    class Meta:
        model = Persoon
        fields = (
            "uuid",
            "url",
            "geboortedatum",
            "overlijdensdatum",
            "geslachtsnaam",
            "geslacht",
            "voorvoegsel",
            "voornamen",
            "adres",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "url": {
                "view_name": "contactgegevens:persoon-detail",
                "lookup_field": "uuid",
                "help_text": "De unieke URL van deze organisatie binnen deze API.",
            },
        }
