from unittest.mock import patch

from django.test import override_settings

import yaml
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

EXPECTED_LEGACY_VERSIONS = (
    ("klanten", "1.0.0"),
    ("contactmomenten", "1.0.0"),
)

EXPECTED_VERSIONS = (
    ("klantinteracties", "1.0.0"),
    ("contactgegevens", "1.0.0"),
)


class APILegacyVersioningTests(APITestCase):
    def test_api_19_documentation_version_json(self):
        for component, _ in EXPECTED_LEGACY_VERSIONS:
            with self.subTest(component=component):
                url = reverse(f"schema-json-{component}")

                response = self.client.get(url)

                self.assertIn(
                    response["Content-Type"],
                    ["application/json", "application/vnd.oai.openapi+json"],
                )
                doc = response.json()
                self.assertGreaterEqual(doc["openapi"], "3.0.0")

    def test_api_19_documentation_version_yaml(self):
        for component, _ in EXPECTED_LEGACY_VERSIONS:
            with self.subTest(component=component):
                url = reverse(f"schema-yaml-{component}")

                response = self.client.get(url)

                self.assertIn(
                    response["Content-Type"],
                    ["application/yaml", "application/vnd.oai.openapi; charset=utf-8"],
                )
                doc = yaml.safe_load(response.content)
                self.assertGreaterEqual(doc["openapi"], "3.0.0")

    @patch(
        "openklant.utils.middleware.get_version_mapping", return_value={"/": "1.0.0"}
    )
    @override_settings(ROOT_URLCONF="openklant.tests.api_strategy.urls")
    def test_api_24_version_header(self, m):
        response = self.client.get("/test-view")

        self.assertEqual(response["API-version"], "1.0.0")


class APIVersioningTests(APITestCase):
    def test_api_19_documentation_version_json(self):
        for component, _ in EXPECTED_VERSIONS:
            with self.subTest(component=component):
                url = reverse(f"{component}:schema-json-{component}")

                response = self.client.get(url)

                self.assertIn(
                    response["Content-Type"],
                    ["application/json", "application/vnd.oai.openapi+json"],
                )
                doc = response.json()
                self.assertGreaterEqual(doc["openapi"], "3.0.0")

    def test_api_19_documentation_version_yaml(self):
        for component, _ in EXPECTED_VERSIONS:
            with self.subTest(component=component):
                url = reverse(f"{component}:schema-yaml-{component}")

                response = self.client.get(url)

                self.assertIn(
                    response["Content-Type"],
                    ["application/yaml", "application/vnd.oai.openapi; charset=utf-8"],
                )
                doc = yaml.safe_load(response.content)
                self.assertGreaterEqual(doc["openapi"], "3.0.0")

    @patch(
        "openklant.utils.middleware.get_version_mapping", return_value={"/": "1.0.0"}
    )
    @override_settings(ROOT_URLCONF="openklant.tests.api_strategy.urls")
    def test_api_24_version_header(self, m):
        response = self.client.get("/test-view")

        self.assertEqual(response["API-version"], "1.0.0")
