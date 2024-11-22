from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


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
    regex="(0[8-9]00[0-9]{4,7})|(0[1-9][0-9]{8})|(\\+[0-9]{9,20}|1400|140[0-9]{2,3})",
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
    regex="^[1-9][0-9]{3} ?[a-zA-Z]{2}$", message=_("Ongeldige postcode")
)

# Doesn't truely validate if IBAN is valid but validated the basic pattern.
validate_iban = CustomRegexValidator(
    regex="^[A-Za-z]{2}[0-9]{2}[A-Za-z0-9]{1,30}$", message=_("Ongeldige IBAN")
)

validate_no_space = CustomRegexValidator(
    regex="^[\S]+$", message=_("Geen spaties toegestaan")  # noqa
)
