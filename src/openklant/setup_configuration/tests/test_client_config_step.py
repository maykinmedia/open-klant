from pathlib import Path

from django.test import TestCase

from django_setup_configuration.exceptions import ConfigurationRunFailed
from django_setup_configuration.test_utils import execute_single_step
from zgw_consumers.test.factories import ServiceFactory

from openklant.config.models import ReferentielijstenConfig
from openklant.setup_configuration.steps import (
    ReferentielijstenConfigurationStep,
)

TEST_FILES = (Path(__file__).parent / "files").resolve()


class ReferentielijstenConfigurationStepTests(TestCase):
    def setUp(self):
        ReferentielijstenConfig.objects.all().delete()

    def test_happy_flow(self):
        service = ServiceFactory(
            slug="referentielijsten-api-test", api_root="http://test.nl/api/v1"
        )

        test_file_path = str(TEST_FILES / "referentielijsten_happy_flow.yaml")

        execute_single_step(
            ReferentielijstenConfigurationStep, yaml_source=test_file_path
        )

        config = ReferentielijstenConfig.get_solo()

        self.assertTrue(config.enabled)
        self.assertEqual(config.service, service)
        self.assertEqual(config.kanalen_tabel_code, "KANAAL")

    def test_error_flow_missing_service(self):
        config = ReferentielijstenConfig.get_solo()
        config.service = None
        config.save()

        test_file_path = str(TEST_FILES / "referentielijsten_missing_service.yaml")

        with self.assertRaises(ConfigurationRunFailed) as cm:
            execute_single_step(
                ReferentielijstenConfigurationStep, yaml_source=test_file_path
            )

        self.assertIn(
            "Could not find Service with identifier 'non-existent-api'",
            str(cm.exception),
        )

        config = ReferentielijstenConfig.get_solo()
        self.assertFalse(config.enabled)
        self.assertIsNone(config.service)

    def test_idempotency(self):
        service = ServiceFactory(
            slug="idempotent-service", api_root="http://idempotent.nl/api/v1"
        )

        test_file_path = str(TEST_FILES / "referentielijsten_idempotent.yaml")

        execute_single_step(
            ReferentielijstenConfigurationStep, yaml_source=test_file_path
        )
        config = ReferentielijstenConfig.get_solo()
        self.assertTrue(config.enabled)
        self.assertEqual(config.service, service)
        self.assertEqual(config.kanalen_tabel_code, "TABEL_IDEMPOTENT")
        execute_single_step(
            ReferentielijstenConfigurationStep, yaml_source=test_file_path
        )

        config = ReferentielijstenConfig.get_solo()
        self.assertTrue(config.enabled)
        self.assertEqual(config.service, service)
        self.assertEqual(config.kanalen_tabel_code, "TABEL_IDEMPOTENT")

    def test_disabled_flow(self):
        service = ServiceFactory(
            slug="referentielijsten-api-disabled", api_root="http://disabled.nl/api/v1"
        )

        test_file_path = str(TEST_FILES / "referentielijsten_disabled_flow.yaml")

        execute_single_step(
            ReferentielijstenConfigurationStep, yaml_source=test_file_path
        )

        config = ReferentielijstenConfig.get_solo()

        self.assertFalse(config.enabled)
        self.assertEqual(config.service, service)
        self.assertEqual(config.kanalen_tabel_code, "KANAAL_DISABLED")
