from unittest.mock import patch

from django.test import override_settings

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin

from openklant.components.contactmomenten.datamodel.constants import InitiatiefNemer
from openklant.components.contactmomenten.datamodel.tests.factories import (
    ContactMomentFactory,
)

from .utils import get_operation_url

KLANT = "http://some.klanten.nl/api/v1/klanten/951e4660-3835-4643-8f9c-e523e364a30f"
MEDEWERKER = (
    "http://some.medewerkers.nl/api/v1/medewerkers/ffb1a466-fdad-4898-87fa-dae026df38c0"
)


@freeze_time("2018-09-07T00:00:00Z")
@override_settings(NOTIFICATIONS_DISABLED=False)
class SendNotifTestCase(JWTAuthMixin, APITestCase):

    heeft_alle_autorisaties = True

    @patch("zds_client.Client.from_url")
    def test_send_notif_create_contactmoment(self, mock_client):
        """
        Check if notifications will be send when ContactMoment is created
        """
        client = mock_client.return_value
        url = get_operation_url("contactmoment_create")
        data = {
            "bronorganisatie": "423182687",
            "klant": KLANT,
            "kanaal": "telephone",
            "tekst": "some text",
            "onderwerpLinks": [],
            "initiatiefnemer": InitiatiefNemer.gemeente,
            "medewerker": MEDEWERKER,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        data = response.json()
        client.create.assert_called_once_with(
            "notificaties",
            {
                "kanaal": "contactmomenten",
                "hoofdObject": data["url"],
                "resource": "contactmoment",
                "resourceUrl": data["url"],
                "actie": "create",
                "aanmaakdatum": "2018-09-07T00:00:00Z",
                "kenmerken": {"bronorganisatie": "423182687", "kanaal": "telephone"},
            },
        )

    @patch("zds_client.Client.from_url")
    def test_send_notif_delete_contactmoment(self, mock_client):
        """
        Check if notifications will be send when ContactMoment is deleted
        """
        client = mock_client.return_value
        contactmoment = ContactMomentFactory.create(
            bronorganisatie=423182687, kanaal="telephone"
        )
        contactmoment_url = get_operation_url(
            "contactmoment_delete", uuid=contactmoment.uuid
        )

        response = self.client.delete(contactmoment_url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data
        )

        client.create.assert_called_once_with(
            "notificaties",
            {
                "kanaal": "contactmomenten",
                "hoofdObject": f"http://testserver{contactmoment_url}",
                "resource": "contactmoment",
                "resourceUrl": f"http://testserver{contactmoment_url}",
                "actie": "destroy",
                "aanmaakdatum": "2018-09-07T00:00:00Z",
                "kenmerken": {"bronorganisatie": "423182687", "kanaal": "telephone"},
            },
        )
