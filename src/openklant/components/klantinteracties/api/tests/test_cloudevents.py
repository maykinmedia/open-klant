import uuid
from unittest.mock import patch

from django.test import override_settings

from freezegun.api import freeze_time
from rest_framework import status
from vng_api_common.tests import reverse

from openklant.cloud_events.constants import (
    ZAAK_GEKOPPELD,
    ZAAK_ONTKOPPELD,
)
from openklant.components.klantinteracties.models.tests.factories import (
    KlantcontactFactory,
    OnderwerpobjectFactory,
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
@override_settings(
    NOTIFICATIONS_SOURCE="ok-test",
    ENABLE_CLOUD_EVENTS=True,
)
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

    @override_settings(ENABLE_CLOUD_EVENTS=False)
    def test_no_cloudevent_when_disabled(self, mock_process_cloudevent):
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

        assert response.status_code == status.HTTP_201_CREATED
        mock_process_cloudevent.assert_not_called()

    def test_onderwerpobject_zaak_gekoppeld_cloudevent(self, mock_process_cloudevent):
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
        mock_process_cloudevent.assert_called_once()

        created_uuid = response.data["uuid"]

        relative_link_to = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": created_uuid, "version": "1"},
        )
        expected_link_to = f"http://testserver{relative_link_to}"

        payload = mock_process_cloudevent.call_args[0][0]
        assert payload["id"] == MOCKED_CLOUDEVENT_ID
        assert payload["type"] == ZAAK_GEKOPPELD
        assert payload["subject"] == str(self.zaak_uuid)
        assert payload["time"] == FROZEN_TIME_Z
        assert payload["data"]["zaak"] == f"urn:uuid:{self.zaak_uuid}"
        assert payload["data"]["linkTo"] == expected_link_to
        assert payload["data"]["label"] == str(self.klantcontact)
        assert payload["data"]["linkObjectType"] == "Onderwerpobject"

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

        assert response.status_code == status.HTTP_201_CREATED
        mock_process_cloudevent.assert_not_called()

    def test_onderwerpobject_without_klantcontact_does_not_send_cloudevent(
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
        mock_process_cloudevent.assert_not_called()

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

    @override_settings(ENABLE_CLOUD_EVENTS=True)
    def test_onderwerpobject_zaak_ontkoppeld_on_delete(self, mock_process_cloudevent):
        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact,
            onderwerpobjectidentificator_object_id=str(self.zaak_uuid),
            onderwerpobjectidentificator_code_objecttype="zaak",
            onderwerpobjectidentificator_code_register="open-zaak",
            onderwerpobjectidentificator_code_soort_object_id="uuid",
        )

        mock_process_cloudevent.reset_mock()

        delete_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": onderwerpobject.uuid, "version": "1"},
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(delete_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_process_cloudevent.assert_called_once()

        payload = mock_process_cloudevent.call_args[0][0]

        expected_link_to = f"http://testserver{delete_url}"

        assert payload["type"] == ZAAK_ONTKOPPELD
        assert payload["subject"] == str(self.zaak_uuid)
        assert payload["time"] == FROZEN_TIME_Z
        assert payload["data"]["zaak"] == f"urn:uuid:{self.zaak_uuid}"
        assert payload["data"]["linkTo"] == expected_link_to
        assert payload["data"]["label"] == str(self.klantcontact)
        assert payload["data"]["linkObjectType"] == "Onderwerpobject"

    def test_delete_non_zaak_does_not_send_ontkoppeld_event(
        self, mock_process_cloudevent
    ):
        create_url = reverse("klantinteracties:onderwerpobject-list")
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
            response = self.client.post(create_url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        onderwerpobject_uuid = response.data["uuid"]

        mock_process_cloudevent.reset_mock()

        delete_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": onderwerpobject_uuid, "version": "1"},
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(delete_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_process_cloudevent.assert_not_called()

    @override_settings(ENABLE_CLOUD_EVENTS=False)
    def test_delete_does_not_send_ontkoppeld_when_disabled(
        self, mock_process_cloudevent
    ):
        create_url = reverse("klantinteracties:onderwerpobject-list")
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
            response = self.client.post(create_url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        onderwerpobject_uuid = response.data["uuid"]

        delete_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": onderwerpobject_uuid, "version": "1"},
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(delete_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_process_cloudevent.assert_not_called()

    def test_delete_without_klantcontact_does_not_send_ontkoppeld(
        self, mock_process_cloudevent
    ):
        create_url = reverse("klantinteracties:onderwerpobject-list")
        data = {
            "onderwerpobjectidentificator": {
                "codeObjecttype": "zaak",
                "object_id": str(self.zaak_uuid),
                "codeRegister": "open-zaak",
                "codeSoortObjectId": "uuid",
            },
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(create_url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        onderwerpobject_uuid = response.data["uuid"]

        delete_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": onderwerpobject_uuid, "version": "1"},
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(delete_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_process_cloudevent.assert_not_called()

    def test_delete_does_not_send_event_when_codeSoortObjectId_not_uuid(
        self, mock_process_cloudevent
    ):
        create_url = reverse("klantinteracties:onderwerpobject-list")
        data = {
            "klantcontact": {"uuid": str(self.klantcontact.uuid)},
            "onderwerpobjectidentificator": {
                "codeObjecttype": "zaak",
                "object_id": str(self.zaak_uuid),
                "codeRegister": "open-zaak",
                "codeSoortObjectId": "other-id-type",
            },
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(create_url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        onderwerpobject_uuid = response.data["uuid"]

        delete_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": onderwerpobject_uuid, "version": "1"},
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(delete_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_process_cloudevent.assert_not_called()

    def test_onderwerpobject_zaak_ontkoppeld_when_changing_to_non_zaak_on_put(
        self, mock_process_cloudevent
    ):
        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact,
            onderwerpobjectidentificator_object_id=str(self.zaak_uuid),
            onderwerpobjectidentificator_code_objecttype="zaak",
            onderwerpobjectidentificator_code_register="open-zaak",
            onderwerpobjectidentificator_code_soort_object_id="uuid",
        )

        url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": onderwerpobject.uuid, "version": "1"},
        )

        mock_process_cloudevent.reset_mock()

        data = {
            "klantcontact": {"uuid": str(self.klantcontact.uuid)},
            "onderwerpobjectidentificator": {
                "codeObjecttype": "document",
                "object_id": str(uuid.uuid4()),
                "codeRegister": "other-register",
                "codeSoortObjectId": "uuid",
            },
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        mock_process_cloudevent.assert_called_once()

        payload = mock_process_cloudevent.call_args[0][0]
        expected_link_to = f"http://testserver{url}"

        assert payload["type"] == ZAAK_ONTKOPPELD
        assert payload["subject"] == str(self.zaak_uuid)
        assert payload["data"]["zaak"] == f"urn:uuid:{self.zaak_uuid}"
        assert payload["data"]["linkTo"] == expected_link_to

    def test_put_does_not_send_ontkoppeld_when_identificator_unchanged(
        self, mock_process_cloudevent
    ):
        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact,
            onderwerpobjectidentificator_object_id=str(self.zaak_uuid),
            onderwerpobjectidentificator_code_objecttype="zaak",
            onderwerpobjectidentificator_code_register="open-zaak",
            onderwerpobjectidentificator_code_soort_object_id="uuid",
        )

        url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": onderwerpobject.uuid, "version": "1"},
        )

        mock_process_cloudevent.reset_mock()

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
            response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        mock_process_cloudevent.assert_not_called()

    def test_onderwerpobject_zaak_ontkoppeld_on_put_object_changed(
        self, mock_process_cloudevent
    ):
        old_zaak_uuid = self.zaak_uuid
        new_zaak_uuid = uuid.uuid4()

        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact,
            onderwerpobjectidentificator_object_id=str(old_zaak_uuid),
            onderwerpobjectidentificator_code_objecttype="zaak",
            onderwerpobjectidentificator_code_register="open-zaak",
            onderwerpobjectidentificator_code_soort_object_id="uuid",
        )

        url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": onderwerpobject.uuid, "version": "1"},
        )

        mock_process_cloudevent.reset_mock()

        data = {
            "klantcontact": {"uuid": str(self.klantcontact.uuid)},
            "onderwerpobjectidentificator": {
                "codeObjecttype": "zaak",
                "object_id": str(new_zaak_uuid),
                "codeRegister": "open-zaak",
                "codeSoortObjectId": "uuid",
            },
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert mock_process_cloudevent.call_count == 2

        expected_link_to = f"http://testserver{url}"

        first_payload = mock_process_cloudevent.call_args_list[0][0][0]
        second_payload = mock_process_cloudevent.call_args_list[1][0][0]

        assert first_payload["type"] == ZAAK_ONTKOPPELD
        assert first_payload["subject"] == str(old_zaak_uuid)
        assert first_payload["data"]["zaak"] == f"urn:uuid:{old_zaak_uuid}"
        assert first_payload["data"]["linkTo"] == expected_link_to
        assert first_payload["data"]["label"] == str(self.klantcontact)

        assert second_payload["type"] == ZAAK_GEKOPPELD
        assert second_payload["subject"] == str(new_zaak_uuid)
        assert second_payload["data"]["zaak"] == f"urn:uuid:{new_zaak_uuid}"
        assert second_payload["data"]["linkTo"] == expected_link_to
        assert second_payload["data"]["label"] == str(self.klantcontact)
        assert second_payload["data"]["linkObjectType"] == "Onderwerpobject"
