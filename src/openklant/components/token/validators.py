import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


# includes tabs, carriage returns, newlines, form-feeds and vertical whitespace characters
ALL_WHITESPACE_PATTERN = re.compile(r"^\s*$")


def validate_non_empty_chars(value: str) -> None:
    if not value:
        raise ValidationError(
            code="invalid",
            message=_("Blank values are not allowed")
        )

    if ALL_WHITESPACE_PATTERN.match(value):
        raise ValidationError(
            code="all-whitespace",
            message=_(
                "Tokens cannot consistent exclusively out of whitespace-like characters"
            )
        )
