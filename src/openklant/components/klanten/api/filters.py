from django.utils.translation import gettext_lazy as _

from django_filters import filters
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_help_text

from openklant.utils.api_spec import mark_oas_difference

from ..datamodel.models import Klant


class KlantFilter(FilterSet):
    subject_natuurlijk_persoon__inp_bsn = filters.CharFilter(
        field_name="natuurlijk_persoon__inp_bsn",
        help_text=get_help_text("klanten.NatuurlijkPersoon", "inp_bsn"),
    )
    subject_natuurlijk_persoon__anp_identificatie = filters.CharFilter(
        field_name="natuurlijk_persoon__anp_identificatie",
        help_text=get_help_text("klanten.NatuurlijkPersoon", "anp_identificatie"),
    )
    subject_natuurlijk_persoon__inp_a_nummer = filters.CharFilter(
        field_name="natuurlijk_persoon__inp_a_nummer",
        help_text=get_help_text("klanten.NatuurlijkPersoon", "inp_a_nummer"),
    )
    subject_natuurlijk_persoon__geboortedatum = filters.CharFilter(
        field_name="natuurlijk_persoon__geboortedatum",
        help_text=mark_oas_difference(_("Geboortedatum van de persoon")),
        lookup_expr="exact",
    )
    subject_natuurlijk_persoon__geboortedatum__gt = filters.CharFilter(
        field_name="natuurlijk_persoon__geboortedatum",
        help_text=mark_oas_difference(_("Geboortedatum van de persoon")),
        lookup_expr="gt",
    )
    subject_natuurlijk_persoon__geboortedatum__gte = filters.CharFilter(
        field_name="natuurlijk_persoon__geboortedatum",
        help_text=mark_oas_difference(_("Geboortedatum van de persoon")),
        lookup_expr="gte",
    )
    subject_natuurlijk_persoon__geboortedatum__lt = filters.CharFilter(
        field_name="natuurlijk_persoon__geboortedatum",
        help_text=mark_oas_difference(_("Geboortedatum van de persoon")),
        lookup_expr="lt",
    )
    subject_natuurlijk_persoon__geboortedatum__lte = filters.CharFilter(
        field_name="natuurlijk_persoon__geboortedatum",
        help_text=mark_oas_difference(_("Geboortedatum van de persoon")),
        lookup_expr="lte",
    )
    subject_niet_natuurlijk_persoon__inn_nnp_id = filters.CharFilter(
        field_name="niet_natuurlijk_persoon__inn_nnp_id",
        help_text=get_help_text("klanten.NietNatuurlijkPersoon", "inn_nnp_id"),
    )
    subject_niet_natuurlijk_persoon__ann_identificatie = filters.CharFilter(
        field_name="niet_natuurlijk_persoon__ann_identificatie",
        help_text=get_help_text("klanten.NietNatuurlijkPersoon", "ann_identificatie"),
    )
    subject_vestiging__vestigings_nummer = filters.CharFilter(
        field_name="vestiging__vestigings_nummer",
        help_text=get_help_text("klanten.Vestiging", "vestigings_nummer"),
    )

    class Meta:
        model = Klant
        fields = {
            "bronorganisatie": ["exact"],
            "klantnummer": ["exact"],
            "bedrijfsnaam": ["exact"],
            "functie": ["exact"],
            "achternaam": ["exact"],
            "telefoonnummer": ["exact"],
            "emailadres": ["exact"],
            "adres__straatnaam": ["exact"],
            "adres__postcode": ["exact"],
            "adres__woonplaats_naam": ["exact"],
            "adres__landcode": ["exact"],
            "subject": ["exact"],
            "subject_type": ["exact"],
        }
