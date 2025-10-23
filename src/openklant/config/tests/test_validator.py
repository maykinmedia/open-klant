from unittest import mock
from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from openklant.components.klantinteracties.api.validators import KanaalValidator


class KanaalValidatorTestCase(TestCase):
    @patch("openklant.components.klantinteracties.api.validators.build_client")
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig"
    )
    def test_validator_passes_for_valid_kanaal(
        self, mock_config_class, mock_build_client
    ):
        mock_client = MagicMock()
        mock_client.get_cached_items_by_tabel_code.return_value = [{"code": "email"}]
        mock_build_client.return_value = mock_client

        mock_config = MagicMock()
        mock_config.enabled = True
        mock_config.service = MagicMock()
        mock_config.tabel_code = "kanaal"
        mock_config_class.get_solo.return_value = mock_config

        validator = KanaalValidator()
        validator("email")

        mock_client.get_cached_items_by_tabel_code.assert_called_once_with("kanaal")

    @patch("openklant.components.klantinteracties.api.validators.build_client")
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig"
    )
    def test_validator_raises_for_invalid_kanaal(
        self, mock_config_class, mock_build_client
    ):
        mock_client = MagicMock()
        mock_client.get_cached_items_by_tabel_code.return_value = [{"code": "phone"}]
        mock_build_client.return_value = mock_client

        # Mock the config
        mock_config = MagicMock()
        mock_config.enabled = True
        mock_config.service = MagicMock()
        mock_config.tabel_code = "kanaal"
        mock_config_class.get_solo.return_value = mock_config

        validator = KanaalValidator()

        with self.assertRaises(ValidationError) as cm:
            validator("email")

        self.assertIn("is not a valid kanaal", str(cm.exception))

        mock_build_client.assert_called_once_with(
            service=mock_config.service,
            client_factory=mock.ANY,
        )
        mock_client.get_cached_items_by_tabel_code.assert_called_once_with("kanaal")
