import os
from unittest.mock import patch

from freezegun.api import freeze_time
from maykin_common.vcr import VCRTestCase
from requests.exceptions import Timeout
from rest_framework import status
from vng_api_common.tests import get_validation_errors, reverse
from zgw_consumers.test.factories import ServiceFactory

from openklant.components.token.tests.api_testcase import APITestCase
from openklant.config.models import ReferentielijstenConfig
from openklant.tests.utils.cache import ClearCachesMixin


class KanaalValidatorAPITestCase(ClearCachesMixin, APITestCase, VCRTestCase):
    service_slug = "referentielijsten-api"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.service = ServiceFactory(
            slug=cls.service_slug,
            api_root="http://localhost:8004/api/v1",
        )

    def setUp(self):
        super().setUp()
        self.initial_data = {
            "nummer": "9999999999",
            "kanaal": "email",
            "onderwerp": "Initial contact for update tests",
            "inhoud": "Test inhoud",
            "indicatie_contact_gelukt": True,
            "taal": "nl",
            "vertrouwelijk": False,
            "plaatsgevonden_op": "2025-11-06T12:00:00Z",
        }

        self.config = ReferentielijstenConfig(
            service=self.service,
            enabled=True,
            kanalen_tabel_code="KANAAL",
        )

    def _create_initial_contact(self, mock_get_solo):
        create_url = reverse(
            "klantinteracties:klantcontact-list", kwargs={"version": "1"}
        )
        response = self.client.post(create_url, self.initial_data, format="json")

        if response.status_code != status.HTTP_201_CREATED:
            raise AssertionError(
                f"Expected 201 when creating klantcontact, got {response.status_code}: {response.data}"
            )

        uuid = response.json().get("uuid")
        if not uuid:
            raise AssertionError(f"No 'uuid' found in response: {response.json()}")

        self.detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"version": "1", "uuid": uuid},
        )

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_valid_kanaal(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        data["nummer"] = "0000000001"

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_invalid_kanaal(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        data["nummer"] = "0000000002"
        data["kanaal"] = "fax"

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "kanaal")

        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "'fax' is not a valid kanaal. Allowed values: no_dates, no_begin_future_eind, phone, email",
        )

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_referentielijsten_returns_empty_list(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        # Tabel does not exist in Referentielijsten API, so the list of returned
        # items will be empty
        mock_get_solo.return_value.kanalen_tabel_code = "non-existent"
        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        data["nummer"] = "0000000002"
        data["kanaal"] = "fax"

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "kanaal")

        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "No channels to validate `kanaal` were found for the "
                "configured tabel_code in the Referentielijsten API."
            ),
        )

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_referentielijsten_timeout(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        data["nummer"] = "0000000002"
        data["kanaal"] = "fax"

        with self.vcr_raises(Timeout):
            response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "kanaal")

        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "Failed to retrieve valid channels from the "
                "Referentielijsten API to validate `kanaal`."
            ),
        )

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_no_referentielijsten_service_configured(self, mock_get_solo):
        mock_get_solo.return_value = ReferentielijstenConfig(
            enabled=True, service=None, kanalen_tabel_code="KANAAL"
        )

        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        data["nummer"] = "0000000002"
        data["kanaal"] = "fax"

        # Should raise a 500 error
        with patch.dict(os.environ, {"DEBUG": "false"}, clear=False):
            response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 500)

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_patch_with_valid_kanaal(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        self._create_initial_contact(mock_get_solo)
        data = {"kanaal": "phone"}

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["kanaal"], "phone")

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_patch_with_invalid_kanaal(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        self._create_initial_contact(mock_get_solo)
        data = {"kanaal": "telepathy"}

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "kanaal")

        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "'telepathy' is not a valid kanaal. Allowed values: no_dates, no_begin_future_eind, phone, email",
        )

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_put_with_valid_kanaal(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        self._create_initial_contact(mock_get_solo)
        data = self.initial_data.copy()
        data["kanaal"] = "phone"
        data["plaatsgevonden_op"] = "2025-11-06T13:00:00Z"

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["kanaal"], "phone")

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_put_with_invalid_kanaal(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        self._create_initial_contact(mock_get_solo)
        data = self.initial_data.copy()
        data["kanaal"] = "carrier-pigeon"
        data["plaatsgevonden_op"] = "2025-11-06T13:00:00Z"

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "kanaal")

        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "'carrier-pigeon' is not a valid kanaal. Allowed values: no_dates, no_begin_future_eind, phone, email",
        )

    @freeze_time("2025-11-24T12:00:00Z")
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_kanaal_not_yet_valid_due_to_future_begin(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        self._create_initial_contact(mock_get_solo)
        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        data["kanaal"] = "future_email"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "kanaal")
        self.assertEqual(error["code"], "invalid")
        self.assertIn("Allowed values:", error["reason"])

    @freeze_time("2025-11-24T12:00:00Z")
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_kanaal_expired_due_to_past_eind(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        self._create_initial_contact(mock_get_solo)
        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        data["kanaal"] = "expired_phone"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "kanaal")
        self.assertEqual(error["code"], "invalid")
        self.assertIn("Allowed values:", error["reason"])

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_kanaal_valid_open_ended_eind(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_kanaal_valid_within_geldigheid_window(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        url = reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"})
        data = self.initial_data.copy()
        data["kanaal"] = "phone"
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @freeze_time("2025-11-24T12:00:00Z")
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_kanaal_valid_no_begin_with_future_end(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        data = self.initial_data.copy()
        data["kanaal"] = "no_begin_future_eind"
        response = self.client.post(
            reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"}),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @freeze_time("2025-11-24T12:00:00Z")
    @patch(
        "openklant.components.klantinteracties.api.validators.ReferentielijstenConfig.get_solo"
    )
    def test_kanaal_valid_begin_in_past_no_end(self, mock_get_solo):
        mock_get_solo.return_value = self.config
        data = self.initial_data.copy()
        data["kanaal"] = "no_dates"
        response = self.client.post(
            reverse("klantinteracties:klantcontact-list", kwargs={"version": "1"}),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
