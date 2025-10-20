from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from openklant.components.klantinteracties.api.validators import KanaalValidator


class KanaalValidatorTestCase(TestCase):
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig"
    )
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenClient"
    )
    def test_validator_passes_for_valid_kanaal(
        self, mock_client_class, mock_config_class
    ):
        mock_client = mock_client_class.return_value
        mock_client.get_cached_items_by_tabel_code.return_value = [{"code": "email"}]

        mock_config = MagicMock()
        mock_config.enabled = True
        mock_config.service = "dummy_service"
        mock_config.tabel_code = "kanaal"
        mock_config_class.get_solo.return_value = mock_config

        validator = KanaalValidator()
        validator("email")

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig"
    )
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenClient"
    )
    def test_validator_raises_for_invalid_kanaal(
        self, mock_client_class, mock_config_class
    ):
        mock_client = mock_client_class.return_value
        mock_client.get_cached_items_by_tabel_code.return_value = [{"code": "phone"}]

        mock_config = MagicMock()
        mock_config.enabled = True
        mock_config.service = "dummy_service"
        mock_config.tabel_code = "kanaal"
        mock_config_class.get_solo.return_value = mock_config

        validator = KanaalValidator()
        with self.assertRaises(ValidationError) as cm:
            validator("email")

        self.assertIn("is not a valid kanaal", str(cm.exception))
