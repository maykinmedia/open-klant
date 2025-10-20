from unittest.mock import Mock, patch

from django.test import TestCase

from zgw_consumers.test.factories import ServiceFactory

from referentielijsten_client.client import ReferentielijstenClient


class ReferentielijstenClientTestCase(TestCase):
    def setUp(self):
        self.service = ServiceFactory(api_root="https://dummy.api/")

    def make_response_mock(self, results):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json = Mock(return_value={"results": results})
        return mock_response

    @patch("referentielijsten_client.client.NLXClient.get")
    def test_get_items_by_tabel_code_calls_correct_url(self, mock_get):
        mock_get.return_value = self.make_response_mock(
            [{"code": "email"}, {"code": "phone"}]
        )
        client = ReferentielijstenClient(
            service=self.service, base_url=self.service.api_root
        )
        result = client.get_items_by_tabel_code("KANAAL")
        mock_get.assert_called_once_with("/items", params={"tabel__code": "KANAAL"})
        self.assertEqual(result, [{"code": "email"}, {"code": "phone"}])

    @patch("referentielijsten_client.client.NLXClient.get")
    def test_get_cached_items_by_tabel_code_caches_result(self, mock_get):
        mock_get.return_value = self.make_response_mock([{"code": "email"}])
        client = ReferentielijstenClient(
            service=self.service, base_url=self.service.api_root
        )
        first = client.get_cached_items_by_tabel_code("KANAAL")
        second = client.get_cached_items_by_tabel_code("KANAAL")
        mock_get.assert_called_once()
        self.assertEqual(first, second)
