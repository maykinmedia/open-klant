from typing import TYPE_CHECKING
from unittest import TestCase

from django.core.cache import caches

if TYPE_CHECKING:
    _TestCaseBase = TestCase
else:
    _TestCaseBase = object


class ClearCachesMixin(_TestCaseBase):
    def setUp(self):
        super().setUp()
        self._clear_caches()
        self.addCleanup(self._clear_caches)

    def _clear_caches(self):
        for cache in caches.all():
            cache.clear()
