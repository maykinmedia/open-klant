from unittest.mock import patch

from django.test import override_settings

import yaml
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

EXPECTED_VERSIONS = (
    ("klantinteracties", "1.0.0"),
    ("contactgegevens", "1.0.0"),
)


class APIVersioningTests(APITestCase):
    def test_api_19_documentation_version_json(self):
        for component, version in EXPECTED_VERSIONS:
            with self.subTest(component=component):
                url = reverse(f"{component}:schema-json-{component}")

                response = self.client.get(url)

                self.assertIn(
                    response["Content-Type"],
                    ["application/json", "application/vnd.oai.openapi+json"],
                )
                doc = response.json()
                self.assertGreaterEqual(doc["openapi"], "3.0.0")
                self.assertEqual(
                    doc["info"]["version"],
                    f"{version} ({api_settings.DEFAULT_VERSION})",
                )

    def test_api_19_documentation_version_yaml(self):
        for component, version in EXPECTED_VERSIONS:
            with self.subTest(component=component):
                url = reverse(f"{component}:schema-yaml-{component}")

                response = self.client.get(url)

                self.assertIn(
                    response["Content-Type"],
                    ["application/yaml", "application/vnd.oai.openapi; charset=utf-8"],
                )
                doc = yaml.safe_load(response.content)
                self.assertGreaterEqual(doc["openapi"], "3.0.0")
                self.assertEqual(
                    doc["info"]["version"],
                    f"{version} ({api_settings.DEFAULT_VERSION})",
                )

    @patch(
        "openklant.utils.middleware.get_version_mapping", return_value={"/": "1.0.0"}
    )
    @override_settings(ROOT_URLCONF="openklant.tests.api_strategy.urls")
    def test_api_24_version_header(self, m):
        response = self.client.get("/test-view")

        self.assertEqual(response["API-version"], "1.0.0")
