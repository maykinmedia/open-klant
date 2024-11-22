# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2024 Dimpact
from drf_spectacular.contrib.django_filters import DjangoFilterExtension
from drf_spectacular.utils import OpenApiParameter
from vng_api_common.utils import underscore_to_camel


class CamelizeFilterExtension(DjangoFilterExtension):
    priority = 1

    def get_schema_operation_parameters(self, auto_schema, *args, **kwargs):
        """
        camelize query parameters
        """
        parameters = super().get_schema_operation_parameters(
            auto_schema, *args, **kwargs
        )

        for parameter in parameters:
            parameter["name"] = underscore_to_camel(parameter["name"])

            # reshape url fields which has incorrect field format
            is_query = parameter["in"] == OpenApiParameter.QUERY
            is_string = parameter["schema"]["type"] == "string"
            is_url_field = parameter["name"].endswith("__url")

            if all((is_query, is_string, is_url_field)):
                parameter["schema"] = {"type": "string", "format": "uri"}

        return parameters
