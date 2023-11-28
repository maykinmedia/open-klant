from collections import OrderedDict

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from vng_api_common.polymorphism import Discriminator as VngDiscriminator


class Discriminator(VngDiscriminator):
    def to_internal_value(self, data) -> OrderedDict:
        # Added custom try catch to support patch call functionalities
        try:
            discriminator_value = data[self.discriminator_field]
        except KeyError:
            raise serializers.ValidationError(
                {f"{self.discriminator_field}": _("Dit veld is vereist.")}
            )
        serializer = self.mapping.get(discriminator_value)
        if serializer is None:
            return None

        internal_value = serializer.to_internal_value(data)
        # if nested serializer was generated in _sanitize_discriminator name if group_field
        # was changed in the internal_value. We need to return it
        if (
            self.group_field
            and self.group_field not in internal_value
            and len(internal_value) == 1
        ):
            key, value = internal_value.popitem()
            internal_value = OrderedDict({self.group_field: value})

        return internal_value
