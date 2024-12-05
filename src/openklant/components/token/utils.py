import secrets
from typing import Iterable


def _generate_token() -> str:
    return secrets.token_hex(20)


def get_token(existing_tokens: Iterable[str]) -> str:
    token = _generate_token()

    while token in existing_tokens:
        token = _generate_token()

    return token
