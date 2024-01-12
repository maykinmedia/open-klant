from django.contrib.auth.models import AnonymousUser

from rest_framework import authentication


# Fake authentication class to display security schema for spectacular
# Real JWT authentication will get performed by `vng_api_common.middleware.AuthMiddleware`
class JWTDummyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        return (AnonymousUser(), True)
