from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication as _TokenAuthentication

if TYPE_CHECKING:
    from .models import TokenAuth


class TokenAuthentication(_TokenAuthentication):
    def authenticate_credentials(self, key: str) -> tuple[None, "TokenAuth"]:
        from .models import TokenAuth

        try:
            token = TokenAuth.objects.get(token=key)
        except TokenAuth.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        return (None, token)
