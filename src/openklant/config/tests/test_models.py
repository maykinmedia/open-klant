from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from zgw_consumers.test.factories import ServiceFactory

from openklant.components.klantinteracties.api.validators import KanaalValidator
from openklant.components.klantinteracties.models import Klantcontact
from openklant.config.models import ReferentielijstenConfig


class ReferentielijstenConfigTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = ServiceFactory(
            api_root="https://dummy.api/",
            api_type="nrc",
            client_id="test",
            secret="test",
            user_id="test",
            user_representation="Test",
        )

        ReferentielijstenConfig.objects.create(
            service=cls.service,
            enabled=True,
            tabel_code="KANAAL",
        )

    class ReferentielijstenConfigTestCase(TestCase):
        def test_validation_raises_if_kanaal_missing(self):
            Klantcontact.objects.create(
                nummer="0000000001",
                kanaal="email",
                onderwerp="Test onderwerp",
                inhoud="Test inhoud",
                indicatie_contact_gelukt=True,
                taal="nl",
                vertrouwelijk=False,
                plaatsgevonden_op=timezone.now(),
            )

            with patch(
                "openklant.components.klantinteracties.api.validators.build_client"
            ) as mock_build_client:
                dummy_client = MagicMock()
                dummy_client.get_cached_items_by_tabel_code.return_value = []
                mock_build_client.return_value = dummy_client

                validator = KanaalValidator()
                with self.assertRaises(ValidationError) as cm:
                    validator("email")

                self.assertIn("is not a valid kanaal", str(cm.exception))
                dummy_client.get_cached_items_by_tabel_code.assert_called_once()
