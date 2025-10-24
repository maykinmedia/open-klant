from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from drf_spectacular.openapi import (
    AutoSchema as _AutoSchema,
    ResolvedComponent,
    append_meta,
    build_array_type,
    build_object_type,
    is_list_serializer,
)
from drf_spectacular.utils import OpenApiParameter
from vng_api_common.constants import VERSION_HEADER

from .expansion import EXPAND_KEY
from .mixins import ExpandMixin


class AutoSchema(_AutoSchema):
    def _get_response_for_code(
        self, serializer, status_code, media_types=None, direction="response"
    ):
        response = super()._get_response_for_code(
            serializer, status_code, media_types, direction
        )

        if 200 <= int(status_code) < 300 and isinstance(self.view, ExpandMixin):
            response = self.get_expand_response(serializer, response, direction)

        return response

    def get_expand_response(self, serializer, base_response, direction):
        """
        add '_expand' into response schema
        """

        include_allowed = getattr(self.view, "include_allowed", lambda: False)()
        base_serializer = (
            serializer.child if is_list_serializer(serializer) else serializer
        )
        inclusion_serializers = getattr(base_serializer, "inclusion_serializers", {})

        if not include_allowed or not inclusion_serializers:
            return base_response

        response = base_response.copy()
        # rewrite schema from response
        expand_properties = {}
        for name, serializer_class in inclusion_serializers.items():
            # create schema for top-level inclusions for now
            if "." in name:
                continue

            inclusion_field = base_serializer.fields[name]
            meta = self._get_serializer_field_meta(inclusion_field, direction)
            inclusion_serializer = import_string(serializer_class)

            inclusion_ref = self.resolve_serializer(inclusion_serializer, direction).ref

            many = hasattr(inclusion_field, "child_relation") or hasattr(
                inclusion_field, "many"
            )

            if many:
                inclusion_schema = append_meta(build_array_type(inclusion_ref), meta)
            else:
                inclusion_schema = append_meta(inclusion_ref, meta)

            expand_properties[name] = inclusion_schema

        inclusions_schema = build_object_type(
            properties=expand_properties,
            description=_(
                "Display details of the linked resources requested in the `expand` parameter"
            ),
        )
        base_component = self.resolve_serializer(base_serializer, direction)
        expand_component_name = f"Expand{base_component.name}"
        expand_component = ResolvedComponent(
            name=expand_component_name,
            type=ResolvedComponent.SCHEMA,
            object=expand_component_name,
            schema={
                "allOf": [
                    base_component.ref,
                    build_object_type(properties={EXPAND_KEY: inclusions_schema}),
                ]
            },
        )
        self.registry.register_on_missing(expand_component)
        expand_schema = expand_component.ref

        # paginate if needed
        if self._is_list_view(serializer):
            expand_schema = build_array_type(expand_schema)

            paginator = self._get_paginator()
            if paginator:
                paginated_name = self.get_paginated_name(expand_component_name)
                paginated_component = ResolvedComponent(
                    name=paginated_name,
                    type=ResolvedComponent.SCHEMA,
                    schema=paginator.get_paginated_response_schema(expand_schema),
                    object=paginated_name,
                )
                self.registry.register_on_missing(paginated_component)
                expand_schema = paginated_component.ref

        response["content"]["application/json"]["schema"] = expand_schema

        return response

    def get_filter_backends(self):
        """support expand for detail views"""
        include_allowed = getattr(self.view, "include_allowed", lambda: False)()
        if self.method == "GET" and include_allowed:
            return getattr(self.view, "filter_backends", [])

        return super().get_filter_backends()

    def get_response_serializers(
        self,
    ):
        if self.method == "DELETE":
            return {204: None}

        return super().get_response_serializers()

    def get_override_parameters(self):
        """Add request GEO headers"""
        params = super().get_override_parameters()
        version_headers = self.get_version_headers()

        return params + version_headers

    def get_version_headers(self) -> list[OpenApiParameter]:
        return [
            OpenApiParameter(
                name=VERSION_HEADER,
                type=str,
                location=OpenApiParameter.HEADER,
                description=_(
                    "Geeft een specifieke API-versie aan in de context van "
                    "een specifieke aanroep. Voorbeeld: 1.2.1."
                ),
                response=True,
            )
        ]
