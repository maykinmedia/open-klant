from django.test import SimpleTestCase

import requests_mock

from openklant.migration.client import Client

URL = "https://example.com/api/v1/partijen"


@requests_mock.Mocker()
class ClientTests(SimpleTestCase):
    def test_retrieve_returns_parsed_json(self, m: requests_mock.Mocker):
        m.get(URL, json={"results": [{"some_field": "value"}]})

        response_data = Client().retrieve(URL)

        self.assertEqual(response_data, {"results": [{"some_field": "value"}]})

    def test_create_returns_created_object(self, m: requests_mock.Mocker):
        m.post(URL, json={"uuid": "123"}, status_code=201)

        response_data = Client().create(URL, data={"nummer": "1"})

        self.assertEqual(response_data, {"uuid": "123"})

    def test_create_returns_none_for_list_response(self, m: requests_mock.Mocker):
        m.post(URL, json=[{"uuid": "123"}], status_code=201)

        response_data = Client().create(URL, data={"nummer": "1"})

        self.assertIsNone(response_data)
