from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.utils.functional import _StrOrPromise
else:
    _StrOrPromise = str

type StrOrPromise = _StrOrPromise
"""Either ``str`` or a ``Promise`` object returned by the lazy ``gettext`` functions."""
