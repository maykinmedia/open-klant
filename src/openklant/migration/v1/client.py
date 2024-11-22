from openklant.migration.client import BaseOpenKlantClient


class LegacyOpenKlantClient(BaseOpenKlantClient):
    token_prefix = "Bearer"
