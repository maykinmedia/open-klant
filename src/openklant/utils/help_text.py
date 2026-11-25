from django.utils.translation import gettext_lazy as _

from openklant.utils.typing import StrOrPromise


def mark_experimental(text: StrOrPromise) -> str:
    return _("**EXPERIMENTEEL** {}").format(text)


def mark_deprecated(text: StrOrPromise) -> str:
    return _("**DEPRECATED** {}").format(text)
