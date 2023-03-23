from unittest.mock import patch

from django.test import override_settings

import requests_mock
from freezegun import freeze_time
from notifications_api_common.models import NotificationsConfig
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from openklant.utils.tests.mixins import JWTAuthTransactionMixin

from ..models.constants import KlantType
from ..models.tests.factories import KlantFactory
from .utils import get_operation_url

SUBJECT = "http://example.com/subject/1"


@freeze_time("2018-09-07T00:00:00Z")
@override_settings(NOTIFICATIONS_DISABLED=False)
class SendNotifTestCase(JWTAuthTransactionMixin, APITransactionTestCase):

    heeft_alle_autorisaties = True

    @patch.object(NotificationsConfig, "get_client")
    @patch("notifications_api_common.viewsets.send_notification.delay")
    def test_send_notif_create_klant(self, mock_task, mock_client):
        """
        Check if notifications will be send when Klant is created
        """
        url = get_operation_url("klant_create")
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Xavier",
            "achternaam": "Jackson",
            "emailadres": "test@gmail.com",
            "subjectType": KlantType.natuurlijk_persoon,
            "subject": SUBJECT,
        }

        with requests_mock.Mocker() as m:
            m.get(SUBJECT, json={})
            response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        data = response.json()
        mock_task.assert_called_once_with(
            {
                "kanaal": "klanten",
                "hoofdObject": data["url"],
                "resource": "klant",
                "resourceUrl": data["url"],
                "actie": "create",
                "aanmaakdatum": "2018-09-07T00:00:00Z",
                "kenmerken": {
                    "subjectType": "natuurlijk_persoon",
                },
            },
        )

    @patch.object(NotificationsConfig, "get_client")
    @patch("notifications_api_common.viewsets.send_notification.delay")
    def test_send_notif_delete_klant(self, mock_task, mock_client):
        """
        Check if notifications will be send when Klant is deleted
        """
        klant = KlantFactory.create(subject_type=KlantType.natuurlijk_persoon)
        klant_url = get_operation_url("klant_delete", uuid=klant.uuid)

        response = self.client.delete(klant_url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data
        )

        mock_task.assert_called_once_with(
            {
                "kanaal": "klanten",
                "hoofdObject": f"http://testserver{klant_url}",
                "resource": "klant",
                "resourceUrl": f"http://testserver{klant_url}",
                "actie": "destroy",
                "aanmaakdatum": "2018-09-07T00:00:00Z",
                "kenmerken": {"subjectType": KlantType.natuurlijk_persoon},
            },
        )
