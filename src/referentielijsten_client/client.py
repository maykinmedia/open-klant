from typing import Any

from django.core.cache import cache

from zgw_consumers.nlx import NLXClient
from zgw_consumers.service import pagination_helper


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

    def get_items_by_tabel_code(self, tabel_code: str) -> list[dict[str, Any]]:
        return self._get_paginated("items", query_params={"tabel__code": tabel_code})

    def get_cached_items_by_tabel_code(
        self, tabel_code: str, cache_timeout: int = 300
    ) -> list[dict[str, Any]]:
        cache_key = f"referentielijst_items_{tabel_code}"
        items = cache.get(cache_key)
        if items is None:
            items = self.get_items_by_tabel_code(tabel_code)
            cache.set(cache_key, items, cache_timeout)
        return items
