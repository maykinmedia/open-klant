import re
from datetime import datetime
from typing import Optional

from dateutil import parser


def camel_to_snake_converter(value):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", value).lower()


def snake_to_camel_converter(value):
    init, *temp = value.split("_")
    return "".join([init.lower(), *map(str.title, temp)])


def parse_datetime(value: str) -> Optional[datetime]:
    """Parses an ISO 8601 string into a datetime object, or returns None if empty or invalid."""
    if not value:
        return None
    try:
        return parser.isoparse(value)
    except (ValueError, TypeError):
        return None
