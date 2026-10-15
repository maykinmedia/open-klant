import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

APP_LABEL = "klantinteracties"
MODELS = ("Klantcontact", "Partij", "InterneTaak")
NUMMER_LENGTH = 12
MAX_NUMMER = 10**NUMMER_LENGTH - 1  # 999999999999
BATCH_SIZE = 1000

REGEX_NUMMER = re.compile(r"^[0-9]{1,12}$")


def validate_nummer(model, nummer: str | None, instance=None) -> str | None:
    """
    Zero pad a new or changed ``nummer`` and check it isn't used by another
    ``model`` object.
    """
    if not nummer:
        return nummer

    # unchanged nummer of an existing object: keep it as it is
    if instance is not None and instance.pk:
        stored = (
            model.objects.filter(pk=instance.pk)
            .values_list("nummer", flat=True)
            .first()
        )
        if nummer == stored:
            return nummer

    nummer = pad_nummer(nummer)

    qs = model.objects.filter(nummer=nummer)
    if instance is not None and instance.pk:
        qs = qs.exclude(pk=instance.pk)

    if qs.exists():
        raise ValidationError(
            _("Er bestaat al een %(model)s met nummer %(nummer)s."),
            code="unique",
            params={"model": model._meta.verbose_name, "nummer": nummer},
        )
    return nummer


def pad_nummer(value: str | None) -> str | None:
    """
    Zero pad a numeric ``nummer`` to ``NUMMER_LENGTH`` digits.
    """
    if value and REGEX_NUMMER.match(value):
        return value.zfill(NUMMER_LENGTH)
    return value
