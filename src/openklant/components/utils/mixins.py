from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    validate_integer,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType

from openklant.utils.validators import (
    validate_bag_id,
    validate_country,
    validate_postal_code,
)

from .expansion import ExpandJSONRenderer


class APIMixin:
    """
    Determine the absolute URL of a resource in the API.

    Model mixin that reverses the URL-path in the API based on the
    ``uuid``-field of a model instance.
    """

    def get_absolute_api_url(self, request=None, **kwargs) -> str:
        from rest_framework.reverse import reverse

        """
        Build the absolute URL of the object in the API.
        """
        # build the URL of the informatieobject
        resource_name = self._meta.model_name
        app_name = request.resolver_match.app_name

        reverse_kwargs = {"uuid": self.uuid}
        reverse_kwargs.update(**kwargs)

        url = reverse(
            f"{app_name}:{resource_name}-detail",
            kwargs=reverse_kwargs,
            request=request,
        )

        return url


class ExpandMixin:
    renderer_classes = (ExpandJSONRenderer,)
    expand_param = "expand"

    def include_allowed(self):
        return self.action in ["list", "retrieve"]

    def get_requested_inclusions(self, request):
        # Pull expand parameter from request body in case of _zoek operation
        if request.method == "POST":
            return ",".join(request.data.get(self.expand_param, []))
        return request.GET.get(self.expand_param)


def create_prefixed_mixin(prefix: str):
    """Dynamically mreate a Mixin with a prefix for Adres fields"""

    base_fields = {
        "nummeraanduiding_id": models.CharField(
            _("nummeraanduiding ID"),
            help_text=_(
                "Identificatie van het adres bij de Basisregistratie Adressen en Gebouwen."
            ),
            max_length=16,
            validators=[validate_bag_id],
            blank=True,
        ),
        "straatnaam": models.CharField(
            _("straatnaam"),
            help_text=_(
                "Straatnaam van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
            ),
            max_length=255,
            blank=True,
        ),
        "huisnummer": models.CharField(
            _("huisnummer"),
            help_text=_(
                "Huisnummer van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
            ),
            validators=[
                validate_integer,
            ],
            max_length=5,
            blank=True,
        ),
        "huisnummertoevoeging": models.CharField(
            _("huisnummertoevoeging"),
            help_text=_(
                "Huisnummertoevoeging van het adres (indien het een Nederlands adres betreft zonder BAG-id).",
            ),
            max_length=20,
            blank=True,
        ),
        "postcode": models.CharField(
            _("postcode"),
            help_text=_(
                "Postcode van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
            ),
            validators=[validate_postal_code],
            max_length=6,
            blank=True,
        ),
        "stad": models.CharField(
            _("stad"),
            help_text=_(
                "Stad van het adres (indien het een Nederlands adres betreft zonder BAG-id)."
            ),
            max_length=255,
            blank=True,
        ),
        "adresregel1": models.CharField(
            _("adresregel 1"),
            help_text=_(
                "Eerste deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
            ),
            max_length=80,
            blank=True,
        ),
        "adresregel2": models.CharField(
            _("adresregel 2"),
            help_text=_(
                "Tweede deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
            ),
            max_length=80,
            blank=True,
        ),
        "adresregel3": models.CharField(
            _("adresregel 3"),
            help_text=_(
                "Derde deel van het adres dat niet voorkomt in de Basisregistratie Adressen en Gebouwen."
            ),
            max_length=80,
            blank=True,
        ),
        "land": models.CharField(
            _("land"),
            help_text=_(
                "ISO 3166-code die het land (buiten Nederland) aangeeft alwaar de ingeschrevene verblijft."
            ),
            validators=[
                MinLengthValidator(limit_value=2),
                validate_country,
            ],
            max_length=2,
            blank=True,
        ),
    }

    prefixed_fields = {f"{prefix}_{name}": field for name, field in base_fields.items()}

    class Meta:
        abstract = True

    mixin_class = type(
        f"{prefix.capitalize()}Mixin",
        (models.Model,),
        {**prefixed_fields, "__module__": __name__, "Meta": Meta},
    )

    setattr(
        mixin_class,
        prefix,
        GegevensGroepType(
            {
                "nummeraanduiding_id": base_fields["nummeraanduiding_id"],
                "straatnaam": base_fields["straatnaam"],
                "huisnummer": base_fields["huisnummer"],
                "huisnummertoevoeging": base_fields["huisnummertoevoeging"],
                "postcode": base_fields["postcode"],
                "stad": base_fields["stad"],
                "adresregel_1": base_fields["adresregel1"],
                "adresregel_2": base_fields["adresregel2"],
                "adresregel_3": base_fields["adresregel3"],
                "land": base_fields["land"],
            },
            optional=(
                "nummeraanduiding_id",
                "straatnaam",
                "huisnummer",
                "huisnummertoevoeging",
                "postcode",
                "stad",
                "adresregel_1",
                "adresregel_2",
                "adresregel_3",
                "land",
            ),
        ),
    )

    return mixin_class
