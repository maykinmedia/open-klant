from unittest.mock import patch

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

        class DummyClient:
            def get_cached_items_by_tabel_code(self, code):
                return []

        with patch(
            "openklant.components.klantinteracties.api.validators.ReferentielijstenClient",
            lambda service: DummyClient(),
        ):
            validator = KanaalValidator()
            with self.assertRaises(ValidationError) as cm:
                validator("email")
            self.assertIn("is not a valid kanaal", str(cm.exception))
