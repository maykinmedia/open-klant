from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import override_settings
from notifications_api_common.kanalen import KANAAL_REGISTRY, Kanaal
from notifications_api_common.models import NotificationsConfig

from rest_framework.test import APITestCase
from zgw_consumers.models import Service

from openklant.components.contactmomenten.models.contactmomenten import ContactMoment


@override_settings(IS_HTTPS=True)
class CreateNotifKanaalTestCase(APITestCase):
    @patch.object(NotificationsConfig, 'get_client')
    @patch("notifications_api_common.models.NotificationsConfig.get_solo")
    def test_kanaal_create_with_name(self, mock_config, mock_client):
        """
        Test is request to create kanaal is send with specified kanaal name
        """
        mock_config.return_value = NotificationsConfig(notifications_api_service=Service(api_root="http://example.com/"))
        client = mock_client.return_value
        client.list.return_value = []

        # ensure this is added to the registry
        Kanaal(label="kanaal_test", main_resource=ContactMoment)

        stdout = StringIO()
        call_command(
            "register_kanalen",
            kanalen=["kanaal_test"],
            stdout=stdout,
        )

        client.create.assert_called_once_with(
            "kanaal",
            {
                "naam": "kanaal_test",
                "documentatieLink": "https://example.com/ref/kanalen/#kanaal_test",
                "filters": [],
            },
        )

    @patch.object(NotificationsConfig, 'get_client')
    @patch("notifications_api_common.models.NotificationsConfig.get_solo")
    @override_settings(NOTIFICATIONS_KANAAL="dummy-kanaal")
    def test_kanaal_create_without_name(self, mock_config, mock_client):
        """
        Test is request to create kanaal is send with default kanaal name
        """
        mock_config.return_value = NotificationsConfig(notifications_api_service=Service(api_root="http://example.com/"))
        client = mock_client.return_value
        client.list.return_value = []

        # clear the registry
        KANAAL_REGISTRY.clear()

        # ensure this is added to the registry
        Kanaal(label="dummy-kanaal", main_resource=ContactMoment)

        stdout = StringIO()
        call_command(
            "register_kanalen",
            stdout=stdout,
        )

        client.create.assert_called_once_with(
            "kanaal",
            {
                "naam": "dummy-kanaal",
                "documentatieLink": "https://example.com/ref/kanalen/#dummy-kanaal",
                "filters": [],
            },
        )
