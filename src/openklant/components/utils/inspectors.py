from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from drf_yasg import openapi
from drf_yasg.inspectors.base import NotHandled
from drf_yasg.inspectors.field import ReferencingSerializerInspector
from rest_framework.serializers import Serializer

from .expansion import EXPAND_KEY


def get_component_from_serializer(serializer: Serializer) -> str:
    return serializer.Meta.model._meta.app_label


class ExpandSerializerInspector(ReferencingSerializerInspector):
    def field_to_swagger_object(
        self,
        field: Serializer,
        swagger_object_type,
        use_references: bool,
        inside_inclusion: bool = False,
        **kwargs,
    ):
        include_allowed = getattr(self.view, "include_allowed", lambda: False)()
        inclusion_serializers = getattr(field, "inclusion_serializers", {})

        if not include_allowed or not inclusion_serializers or inside_inclusion:
            return NotHandled

        # retrieve base schema
        base_schema_ref = super().field_to_swagger_object(
            field, swagger_object_type, use_references, **kwargs
        )

        # create schema for inclusions
        expand_properties = {}
        for name, serializer_class in inclusion_serializers.items():
            # create schema for top-level inclusions for now
            if "." in name:
                continue

            inclusion_serializer = import_string(serializer_class)()
            if get_component_from_serializer(field) == get_component_from_serializer(
                inclusion_serializer
            ):
                # same component - local ref
                inclusion_ref = self.probe_field_inspectors(
                    inclusion_serializer,
                    openapi.Schema,
                    use_references=True,
                    inside_inclusion=True,
                )

            # define if it is many=True field
            # we can't initialize serializer with many=True, because it will trigger infinite loop
            # therefore we create array manually
            inclusion_field = field.fields[name]
            many = hasattr(inclusion_field, "child_relation")
            inclusion_schema = (
                openapi.Schema(type=openapi.TYPE_ARRAY, items=inclusion_ref)
                if many
                else inclusion_ref
            )
            expand_properties[name] = inclusion_schema

        expand_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=expand_properties,
            description=_(
                "Display details of the linked resources requested in the `expand` parameter"
            ),
        )

        # combine base schema with inclusions
        allof_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            all_of=[
                base_schema_ref,
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={EXPAND_KEY: expand_schema},
                ),
            ],
        )

        return allof_schema
