from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from localflavor.generic.countries.iso_3166 import ISO_3166_1_ALPHA2_COUNTRY_CODES


def validate_country(value: str) -> None:
    """
    Validate an ISO 3166-1 alpha-2 country code

    :param value:
    :return: None if validation passed. Otherwise, raises a ``ValidationError`` exception.
    """
    if value not in ISO_3166_1_ALPHA2_COUNTRY_CODES:
        raise ValidationError(
            _("Ongeldige landcode, de code moet behoren tot de ISO 3166-standaard")
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


validate_phone_number = RegexValidator(
    regex=r"^("
    r"0[8-9]00[0-9]{4,8}"  # starting with 08 or 09, followed by 00 and then 4 to 8 digits
    r"|0[1-9][0-9]{8}"  # starting with 0, followed by a digit from 1-9 and then exactly 8 digits
    r"|\+31[0-9]{10}"  # starting with +31 followed by 10 digits (Dutch format)
    r"|\+[0-9]{9,20}"  # starting with + followed by 9 to 20 digits (international numbers)
    r"|00[0-9]{11}"  # starting with 00, followed by 11 digits
    r"|1400"  # specific short number for services
    r"|140[0-9]{2,3}"  # starting with 140 and followed by 2 or 3 digits
    r")$",
    message=_("Het opgegeven telefoonnummer is ongeldig."),
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
    regex="^[1-9][0-9]{3} [A-Z]{2}$", message=_("Ongeldige postcode")
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
