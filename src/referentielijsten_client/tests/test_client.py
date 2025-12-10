from maykin_common.vcr import VCRTestCase
from zgw_consumers.models import Service
from zgw_consumers.test.factories import ServiceFactory

from openklant.tests.utils.cache import ClearCachesMixin
from referentielijsten_client.client import ReferentielijstenClient


class ReferentielijstenClientTestCase(ClearCachesMixin, VCRTestCase):
    service_slug = "referentielijsten-api"

    def setUp(self):
        super().setUp()
        ServiceFactory(slug=self.service_slug, api_root="http://localhost:8004/api/v1")
        self.service = Service.objects.get(slug=self.service_slug)
        self.client = ReferentielijstenClient(
            service=self.service, base_url=self.service.api_root
        )

    def test_get_items_by_tabel_code(self):
        items = self.client.get_items_by_tabel_code("KANAAL")

        self.assertIsInstance(items, list)
        self.assertTrue(all("code" in item for item in items))
        codes = [item["code"] for item in items]
        self.assertEqual(
            codes,
            [
                "no_dates",
                "no_begin_future_eind",
                "expired_phone",
                "future_email",
                "phone",
                "email",
            ],
        )

    def test_get_cached_items_by_tabel_code(self):
        first = self.client.get_cached_items_by_tabel_code("KANAAL")
        self.assertEqual(len(self.cassette.requests), 1)
        second = self.client.get_cached_items_by_tabel_code("KANAAL")
        self.assertEqual(
            len(self.cassette.requests),
            1,
            "The second call to get_cached_items_by_tabel_code should be cached and not result in a new network request.",
        )

        self.assertEqual(first, second)
        self.assertTrue(all("code" in item for item in first))

    def test_cache_independence_between_tables(self):
        items_test = self.client.get_cached_items_by_tabel_code("KANAAL")
        items_nonexistent = self.client.get_cached_items_by_tabel_code("NONEXISTENT")

        self.assertNotEqual(items_test, items_nonexistent)
        self.assertEqual(items_nonexistent, [])

    def test_item_validity_dates(self):
        items = self.client.get_cached_items_by_tabel_code("KANAAL")
        for item in items:
            self.assertIn("begindatumGeldigheid", item)
            self.assertIn("einddatumGeldigheid", item)
