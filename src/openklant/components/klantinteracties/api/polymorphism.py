from collections import OrderedDict
from copy import copy
from typing import Union

from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils.translation import gettext_lazy as _

import structlog
from rest_framework import serializers
from rest_framework.fields import empty
from vng_api_common.polymorphism import (
    Discriminator as VngDiscriminator,
    PolymorphicSerializer as VngPolymorphicSerializer,
    PolymorphicSerializerMetaclass as VngPolymorphicSerializerMetaclass,
)

logger = structlog.stdlib.get_logger(__name__)


class Discriminator(VngDiscriminator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = kwargs.get("required", False)

    def to_internal_value(self, data) -> OrderedDict:
        # CUSTOM CODE: try catch to support patch call functionalities
        if self.required and self.discriminator_field not in data:
            raise serializers.ValidationError(
                {f"{self.discriminator_field}": _("Dit veld is vereist.")}
            )

        value = data.get(self.discriminator_field)
        if value is None:
            return None

        serializer = self.mapping.get(value)
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

    def to_representation(self, instance) -> OrderedDict:
        discriminator_value = getattr(instance, self.discriminator_field)
        serializer = self.mapping.get(discriminator_value)
        if serializer is None:
            return None

        # CUSTOM CODE: added context to the serializer root
        serializer.root._context = self.context

        representation = serializer.to_representation(instance)
        return representation


class PolyMorphicSerializerMetaclass(VngPolymorphicSerializerMetaclass):
    @classmethod
    def _sanitize_discriminator(cls, name, attrs) -> Union[Discriminator, None]:
        discriminator = attrs["discriminator"]
        if discriminator is None:
            return None

        model = attrs["Meta"].model

        try:
            field = model._meta.get_field(discriminator.discriminator_field)
        except FieldDoesNotExist as exc:
            raise FieldDoesNotExist(
                f"The discriminator field '{discriminator.discriminator_field}' "
                f"does not exist on the model '{model._meta.label}'"
            ) from exc

        values_seen = set()

        for value, fields in discriminator.mapping.items():
            # construct a serializer instance if a tuple/list of fields is passed
            if isinstance(fields, (tuple, list)):
                name = f"{value}{model._meta.object_name}Serializer"

                Meta = type("Meta", (), {"model": model, "fields": tuple(fields)})

                serializer_class = type(
                    name, (serializers.ModelSerializer,), {"Meta": Meta}
                )

                discriminator.mapping[value] = serializer_class()

            values_seen.add(value)

            serializer = discriminator.mapping[value]

            if serializer is None:
                continue

            # rewrite it to nested serializer
            if discriminator.group_field:
                group_name = (
                    f"{discriminator.group_field}_{serializer.__class__.__name__}"
                )
                group_meta = type(
                    "Meta", (), {"model": model, "fields": (discriminator.group_field,)}
                )

                # find source field for nested serializer
                source = None
                related_fields = model._meta.fields_map
                for field_name, field_type in related_fields.items():
                    # CUSTOM CODE: Updated if statement to only use OneToOne fields as the source
                    # TODO: change Discriminator to have mapping to dict with serializer and model field name
                    if field_type.related_model == serializer.Meta.model and isinstance(
                        field_type, OneToOneRel
                    ):
                        source = field_name

                group_field = serializer.__class__(
                    source=source, required=False, label=discriminator.group_field
                )

                group_serializer_class = type(
                    group_name,
                    (serializers.ModelSerializer,),
                    {"Meta": group_meta, discriminator.group_field: group_field},
                )
                discriminator.mapping[value] = group_serializer_class()

        if field.choices:
            values = {choice[0] for choice in field.choices}
            difference = values - values_seen
            if difference:
                logger.warning(
                    "not_all_values_have_serializers",
                    name=name,
                    missing_values=difference,
                )

        return discriminator


class PolymorphicSerializer(
    VngPolymorphicSerializer, metaclass=PolyMorphicSerializerMetaclass
):
    discriminator: Discriminator = None

    def __init__(self, instance=None, data=empty, **kwargs):
        self.discriminator = copy(self.discriminator)
        super().__init__(instance, data, **kwargs)

    def to_representation(self, instance):
        self.discriminator.context = self.context
        return super().to_representation(instance)
