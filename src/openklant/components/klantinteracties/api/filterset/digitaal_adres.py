from django_filters.rest_framework import FilterSet

from openklant.components.klantinteracties.api.serializers.digitaal_adres import (
    DigitaalAdresSerializer,
)
from openklant.components.utils.filters import ExpandFilter


class DigitaalAdresExpandFilterSet(FilterSet):
    expand = ExpandFilter(serializer_class=DigitaalAdresSerializer)
