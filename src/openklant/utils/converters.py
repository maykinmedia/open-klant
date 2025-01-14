import re

from .constants import COUNTRIES_DICT


def camel_to_snake_converter(value):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", value).lower()


def snake_to_camel_converter(value):
    init, *temp = value.split("_")
    return "".join([init.lower(), *map(str.title, temp)])


def nl_code_to_iso_code_country_converter(nl_code: str) -> str:
    for country_data in COUNTRIES_DICT.values():
        if country_data["nl_code"] == nl_code:
            return country_data["iso_code"]
    return ""
