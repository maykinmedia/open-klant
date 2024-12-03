import binascii
import os

from typing import Iterable


def _generate_token() -> str:
    return binascii.hexlify(os.urandom(20)).decode()


def get_token(existing_tokens: Iterable[str]) -> str:
    token = _generate_token()

    while token in existing_tokens:
        token = _generate_token()

    return token
