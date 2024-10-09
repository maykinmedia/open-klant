from django.core.management.base import BaseCommand

from vng_api_common.tests.auth import JWTAuthMixin, generate_jwt_auth


class Command(JWTAuthMixin, BaseCommand):
    def handle(self, *args, **options):
        applicatie, autorisatie = self._create_credentials(
            self.client_id,
            self.secret,
            heeft_alle_autorisaties=True,
            max_vertrouwelijkheidaanduiding=self.max_vertrouwelijkheidaanduiding
        )

        return generate_jwt_auth(
            client_id=self.client_id,
            secret=self.secret,
            user_id=self.user_id,
            user_representation=self.user_representation,
        )
