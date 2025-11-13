from django.core.cache import caches


class ClearCachesMixin:
    def setUp(self):
        super().setUp()
        self._clear_caches()
        self.addCleanup(self._clear_caches)

    def _clear_caches(self):
        for cache in caches.all():
            cache.clear()
