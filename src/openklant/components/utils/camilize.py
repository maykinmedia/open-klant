import re
from collections import OrderedDict

from django.utils.encoding import force_text
from django.utils.functional import Promise

from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import is_iterable, underscore_to_camel
from rest_framework.utils.serializer_helpers import ReturnDict

camelize_re = re.compile(r"[a-z0-9]?_[a-z0-9]")


def camelize(data, **options):
    # Handle lazy translated strings.
    ignore_fields = options.get("ignore_fields") or ()
    ignore_keys = options.get("ignore_keys") or ()

    if isinstance(data, Promise):
        data = force_text(data)
    if isinstance(data, dict):
        if isinstance(data, ReturnDict):
            new_dict = ReturnDict(serializer=data.serializer)
        else:
            new_dict = OrderedDict()
        for key, value in data.items():
            if isinstance(key, Promise):
                key = force_text(key)
            # added ignore_keys validation check
            if key not in ignore_keys and isinstance(key, str) and "_" in key:
                new_key = re.sub(camelize_re, underscore_to_camel, key)
            else:
                new_key = key
            if key not in ignore_fields and new_key not in ignore_fields:
                new_dict[new_key] = camelize(value, **options)
            else:
                new_dict[new_key] = value
        return new_dict
    if is_iterable(data) and not isinstance(data, str):
        return [camelize(item, **options) for item in data]
    return data


class CamelCaseJSONRenderer(api_settings.RENDERER_CLASS):
    def render(self, data, *args, **kwargs):
        return super().render(
            camelize(data, **api_settings.JSON_UNDERSCOREIZE), *args, **kwargs
        )
