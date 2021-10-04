from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.encoding import force_text
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
    invalid_chars = '/"\\,;' if allow_apostrophe else '/"\\,;\''

    for char in invalid_chars:
        if char in value:
            raise ValidationError(
                _('Uw invoer bevat een ongeldig teken: %s') % char)
    return value


def validate_phone_number(value):
    try:
        int(value.strip().lstrip('0+').replace('-', '').replace(' ', ''))
    except (ValueError, TypeError):
        raise ValidationError(
            _('Het opgegeven mobiele telefoonnummer is ongeldig.'))

    return value


class CustomRegexValidator(RegexValidator):
    """
    CustomRegexValidator because the validated value is append to the message.
    """

    def __call__(self, value):
        """
        Validates that the input matches the regular expression.
        """
        if not self.regex.search(force_text(value)):
            message = '{0}: {1}'.format(self.message, force_text(value))
            raise ValidationError(message, code=self.code)


validate_postal_code = CustomRegexValidator(
    regex='^[1-9][0-9]{3} ?[a-zA-Z]{2}$',
    message=_('Ongeldige postcode')
)
