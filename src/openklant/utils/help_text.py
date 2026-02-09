from django.utils.translation import gettext_lazy as _


def mark_experimental(text):
    return _("**EXPERIMENTEEL** {}").format(text)


def mark_deprecated(text):
    return _("**DEPRECATED** {}").format(text)
