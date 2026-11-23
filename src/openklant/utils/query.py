# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2024 Dimpact
from django.db.models import Model

from django_filters import Filter, FilterSet
from drf_spectacular.contrib.django_filters import DjangoFilterExtension
from drf_spectacular.openapi import AutoSchema
from vng_api_common.utils import underscore_to_camel

from openklant.components.utils.filters import URLViewFilter


class CamelizeFilterExtension(DjangoFilterExtension):
    priority = 1

    def resolve_filter_field(
        self,
        auto_schema: AutoSchema,
        model: type[Model],
        filterset_class: type[FilterSet],
        field_name: str,
        filter_field: Filter,
    ) -> list[dict]:
        results = super().resolve_filter_field(
            auto_schema, model, filterset_class, field_name, filter_field
        )

        for result in results:
            result["name"] = underscore_to_camel(result["name"])

        return results


class UUIDURLFilterExtension(CamelizeFilterExtension):
    priority = 2

    def resolve_filter_field(
        self,
        auto_schema: AutoSchema,
        model: type[Model],
        filterset_class: type[FilterSet],
        field_name: str,
        filter_field: Filter,
    ) -> list[dict]:
        results = super().resolve_filter_field(
            auto_schema, model, filterset_class, field_name, filter_field
        )

        if not isinstance(filter_field, URLViewFilter):
            return results

        for result in results:
            schema = result.setdefault("schema", {})
            schema.update({"type": "string", "format": "uri"})

        return results
