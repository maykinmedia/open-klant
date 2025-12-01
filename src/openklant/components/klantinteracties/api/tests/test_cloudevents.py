import uuid
from unittest.mock import patch

from django.test import override_settings

from freezegun.api import freeze_time
from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories import (
    KlantcontactFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase

MOCKED_CLOUDEVENT_ID = "f347fd1f-dac1-4870-9dd0-f6c00edf4bf7"
FROZEN_TIME = "2025-10-10"
FROZEN_TIME_Z = "2025-10-10T00:00:00Z"


@freeze_time("2025-10-10")
@patch("notifications_api_common.tasks.send_cloudevent.delay")
@patch(
    "notifications_api_common.cloudevents.uuid.uuid4",
    lambda: MOCKED_CLOUDEVENT_ID,
)
@override_settings(NOTIFICATIONS_SOURCE="ok-test")
class OnderwerpobjectCloudEventTest(APITestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()

        self.klantcontact = KlantcontactFactory(
            onderwerp="Mijn Klantcontact Onderwerp",
            nummer="99999",
        )

        self.klantcontact_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(self.klantcontact.uuid)},
        )

        self.zaak_uuid = uuid.UUID("a7b3c8d9-e4f5-6a7b-8c9d-e0f1a2b3c4d5")

    def test_onderwerpobject_zaak_gelinkt_cloudevent(self, mock_process_cloudevent):
        url = reverse("klantinteracties:onderwerpobject-list")

        data = {
            "klantcontact": {"uuid": str(self.klantcontact.uuid)},
            "onderwerpobjectidentificator": {
                "codeObjecttype": "zaak",
                "object_id": str(self.zaak_uuid),
                "codeRegister": "open-zaak",
                "codeSoortObjectId": "uuid",
            },
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert mock_process_cloudevent.call_count == 1

    def test_onderwerpobject_non_zaak_no_cloudevent(self, mock_process_cloudevent):
        url = reverse("klantinteracties:onderwerpobject-list")
        data = {
            "klantcontact": {"uuid": str(self.klantcontact.uuid)},
            "onderwerpobjectidentificator": {
                "codeObjecttype": "document",
                "object_id": str(uuid.uuid4()),
                "codeRegister": "some-register",
                "codeSoortObjectId": "uuid",
            },
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED, response.data
        mock_process_cloudevent.assert_not_called()

    def test_onderwerpobject_without_klantcontact_sends_cloudevent(
        self, mock_process_cloudevent
    ):
        url = reverse("klantinteracties:onderwerpobject-list")
        data = {
            "onderwerpobjectidentificator": {
                "codeObjecttype": "zaak",
                "object_id": str(self.zaak_uuid),
                "codeRegister": "open-zaak",
                "codeSoortObjectId": "uuid",
            },
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert mock_process_cloudevent.call_count == 1

    def test_multiple_onderwerpobjects_trigger_cloudevents(
        self, mock_process_cloudevent
    ):
        url = reverse("klantinteracties:onderwerpobject-list")
        for _ in range(3):
            data = {
                "klantcontact": {"uuid": str(self.klantcontact.uuid)},
                "onderwerpobjectidentificator": {
                    "codeObjecttype": "zaak",
                    "object_id": str(uuid.uuid4()),
                    "codeRegister": "open-zaak",
                    "codeSoortObjectId": "uuid",
                },
            }
            with self.captureOnCommitCallbacks(execute=True):
                response = self.client.post(url, data, format="json")
            assert response.status_code == status.HTTP_201_CREATED

        assert mock_process_cloudevent.call_count == 3
