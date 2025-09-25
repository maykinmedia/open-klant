import time

import jwt
import structlog

from openklant.components.token.models import TokenAuth

MIGRATION_TOKEN_IDENTIFIER = "Migration application"
logger = structlog.stdlib.get_logger(__name__)


# Can be used to easily generate a encoded JWT token given the client_id and secret
def generate_jwt_token(
    client_id: str, secret: str, user_representation: str = ""
) -> str:
    payload = {
        # standard claims
        "iss": "testsuite",
        "iat": int(time.time()),
        # custom
        "client_id": client_id,
        "user_id": client_id,
        "user_representation": user_representation,
    }

    encoded = jwt.encode(payload, secret, algorithm="HS256")
    return str(encoded)


def _generate_dummy_token() -> str:
    try:
        token_auth, _ = TokenAuth.objects.get_or_create(
            application=MIGRATION_TOKEN_IDENTIFIER
        )
    except TokenAuth.MultipleObjectsReturned:
        dummy_tokens = TokenAuth.objects.get_or_create(
            application=MIGRATION_TOKEN_IDENTIFIER
        )

        token_auth = dummy_tokens.first()
        deletion_tokens = dummy_tokens.exclude(pk=token_auth.pk)
        deleted_token_ids = list(deletion_tokens.values_list("id", flat=True))
        deletion_tokens.delete()

        logger.warning("removed_migration_dummy_tokens", tokens=deleted_token_ids)
    return token_auth.token
