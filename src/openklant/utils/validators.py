from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from localflavor.generic.countries.iso_3166 import ISO_3166_1_ALPHA2_COUNTRY_CODES


def validate_country(value: str) -> None:
    """
    Validate an ISO 3166-1 alpha-2 country code

    :param value:
    :return: None if validation passed. Otherwise, raises a ``ValidationError`` exception.
    """
    upper_value = value.upper()
    if upper_value not in ISO_3166_1_ALPHA2_COUNTRY_CODES:
        raise ValidationError(
            _("Ongeldige landcode, de code moet behoren tot de ISO 3166-standaard")
        )
    elif value != upper_value:
        raise ValidationError(
            _(
                "Ongeldige landcode, de code moet behoren tot de ISO 3166-standaard."
                " Bedoelde u {country_upper}?"
            ).format(country_upper=upper_value)
        )


def validate_charfield_entry(value, allow_apostrophe=False):
    """
    Validates a charfield entry according with Belastingdienst requirements.

    :param value: The input value string to be validated.
    :param allow_apostrophe: Boolean to add the apostrophe character to the
    validation. Apostrophes are allowed in input with ``True`` value. Defaults
    to ``False``.
    :return: The input value if validation passed. Otherwise, raises a
    ``ValidationError`` exception.
    """
    invalid_chars = '/"\\,;' if allow_apostrophe else "/\"\\,;'"

    for char in invalid_chars:
        if char in value:
            raise ValidationError(_("Uw invoer bevat een ongeldig teken: %s") % char)
    return value


FORBIDDEN_PREFIXES = (
    "0800",
    "0900",
    "088",
    "1400",
    "140",
)


@deconstructible
class RegexWithDisallowedPrefixesValidator(RegexValidator):
    def __init__(self, *args, **kwargs):
        self.disallowed_prefixes = kwargs.pop("disallowed_prefixes")
        self.message_disallowed_prefix = kwargs.pop("message_disallowed_prefix")

        super().__init__(*args, **kwargs)

    def __call__(self, value):
        for prefix in self.disallowed_prefixes:
            if value.startswith(prefix):
                raise ValidationError(self.message_disallowed_prefix)

        super().__call__(value)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.regex.pattern == other.regex.pattern
            and self.disallowed_prefixes == other.disallowed_prefixes
        )


phonenumber_regex = r"^(0[1-9][0-9]{8}|\+[0-9]{9,15}|00[0-9]{7,13})$"

validate_phone_number = RegexWithDisallowedPrefixesValidator(
    regex=phonenumber_regex,
    disallowed_prefixes=FORBIDDEN_PREFIXES,
    message=_("Het opgegeven telefoonnummer is ongeldig."),
    message_disallowed_prefix=_(
        "Het opgegeven telefoonnummer is ongeldig, telefoonnummers beginnend met 0800, 0900, 088, 1400 of 140xx zijn niet toegestaan."
    ),
)


class CustomRegexValidator(RegexValidator):
    """
    CustomRegexValidator because the validated value is append to the message.
    """

    def __call__(self, value):
        """
        Validates that the input matches the regular expression.
        """
        if not self.regex.search(force_str(value)):
            message = "{0}: {1}".format(self.message, force_str(value))
            raise ValidationError(message, code=self.code)


validate_postal_code = CustomRegexValidator(
    regex="^[1-9][0-9]{3} [A-Z]{2}$",
    message=_("Postcode moet aan het volgende formaat voldoen: `1234 AB` (met spatie)"),
)

# Doesn't truely validate if IBAN is valid but validated the basic pattern.
validate_iban = CustomRegexValidator(
    regex="^[A-Za-z]{2}[0-9]{2}[A-Za-z0-9]{1,30}$", message=_("Ongeldige IBAN")
)

validate_no_space = CustomRegexValidator(
    regex="^[\S]+$", message=_("Geen spaties toegestaan")
)

validate_bag_id = CustomRegexValidator(
    regex="^[0-9]{16}$", message=_("Ongeldige nummeraanduiding BAG-ID")
)
