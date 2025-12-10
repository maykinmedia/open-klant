from typing import Any

from django.core.cache import cache

import requests
from zgw_consumers.client import build_client
from zgw_consumers.models import Service
from zgw_consumers.nlx import NLXClient
from zgw_consumers.service import pagination_helper

REFERENTIELIJST_CLIENT_CACHE_PREFIX = "referentielijst_items_"


class NoServiceConfigured(RuntimeError):
    pass


class ReferentielijstenClient(NLXClient):
    def _get_paginated(
        self,
        endpoint: str,
        query_params: dict[Any, Any] | None = None,
    ):
        query_params = query_params or {}
        response = self.get(endpoint, params=query_params)
        response.raise_for_status()
        data = response.json()
        all_results = list(pagination_helper(self, data))
        return all_results

    @property
    def can_connect(self) -> bool:
        try:
            response = self.get("")
            response.raise_for_status()
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_items_by_tabel_code(self, tabel_code: str) -> list[dict[str, Any]]:
        return self._get_paginated("items", query_params={"tabel__code": tabel_code})

    def get_cached_items_by_tabel_code(
        self, tabel_code: str, cache_timeout: int = 300
    ) -> list[dict[str, Any]]:
        cache_key = f"{REFERENTIELIJST_CLIENT_CACHE_PREFIX}{tabel_code}"
        items = cache.get(cache_key)
        if items is None:
            items = self.get_items_by_tabel_code(tabel_code)
            cache.set(cache_key, items, cache_timeout)
        return items


def get_referentielijsten_client(service: Service) -> ReferentielijstenClient:
    if not service:
        raise NoServiceConfigured("No Referentielijsten API service configured!")

    return build_client(service, client_factory=ReferentielijstenClient)
