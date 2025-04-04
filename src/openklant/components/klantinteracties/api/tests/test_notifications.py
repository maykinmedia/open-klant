from unittest.mock import patch

from django.test import override_settings

from freezegun import freeze_time
from notifications_api_common.models import NotificationsConfig
from rest_framework import status
from vng_api_common.tests import reverse
from zgw_consumers.constants import APITypes
from zgw_consumers.models import Service

from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    DigitaalAdresFactory,
    InterneTaakFactory,
    KlantcontactFactory,
    PartijFactory,
    RekeningnummerFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class NotificationsConfigTestCase:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        service, _ = Service.objects.update_or_create(
            api_root="https://notificaties-api.vng.cloud/api/v1/",
            defaults=dict(
                api_type=APITypes.nrc,
                client_id="test",
                secret="test",
                user_id="test",
                user_representation="Test",
            ),
        )
        config = NotificationsConfig.get_solo()
        config.notifications_api_service = service
        config.save()


@freeze_time("2024-2-2T00:00:00Z")
@patch("notifications_api_common.viewsets.send_notification.delay")
@override_settings(NOTIFICATIONS_DISABLED=False)
class SendNotificationPartijTestCase(NotificationsConfigTestCase, APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.partij = PartijFactory.create(
            nummer="1298329191",
            interne_notitie="interneNotitie",
            soort_partij="organisatie",
            voorkeurstaal="ndl",
            indicatie_actief=True,
        )
        cls.list_url = reverse("klantinteracties:partij-list")
        cls.detail_url = reverse(
            "klantinteracties:partij-detail", kwargs={"uuid": str(cls.partij.uuid)}
        )

        digitaal_adres = DigitaalAdresFactory.create()
        rekeningnummer = RekeningnummerFactory.create()
        cls.data = {
            "nummer": "123456789",
            "interneNotitie": "interneNotitie",
            "digitaleAdressen": [{"uuid": str(digitaal_adres.uuid)}],
            "voorkeursDigitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "rekeningnummers": [{"uuid": str(rekeningnummer.uuid)}],
            "voorkeursRekeningnummer": {"uuid": str(rekeningnummer.uuid)},
            "soortPartij": SoortPartij.organisatie.value,
            "partijIdentificatie": {"naam": "string"},
            "voorkeurstaal": "ndl",
            "indicatie_actief": True,
        }

    def test_send_notification_create_object(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.list_url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        m.assert_called_with(
            {
                "kanaal": "partijen",
                "hoofdObject": data["url"],
                "resource": "partij",
                "resourceUrl": data["url"],
                "actie": "create",
                "aanmaakdatum": "2024-02-02T00:00:00Z",
                "kenmerken": {
                    "nummer": "123456789",
                    "interneNotitie": "interneNotitie",
                    "soortPartij": SoortPartij.organisatie.value,
                },
            }
        )

    def test_send_notification_update_object(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.put(self.detail_url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        m.assert_called_with(
            {
                "kanaal": "partijen",
                "hoofdObject": data["url"],
                "resource": "partij",
                "resourceUrl": data["url"],
                "actie": "update",
                "aanmaakdatum": "2024-02-02T00:00:00Z",
                "kenmerken": {
                    "nummer": "123456789",
                    "interneNotitie": "interneNotitie",
                    "soortPartij": SoortPartij.organisatie.value,
                },
            }
        )

    def test_send_notification_partial_update_object(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.patch(
                self.detail_url, {"soortPartij": SoortPartij.organisatie.value}
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        m.assert_called_with(
            {
                "kanaal": "partijen",
                "hoofdObject": data["url"],
                "resource": "partij",
                "resourceUrl": data["url"],
                "actie": "partial_update",
                "aanmaakdatum": "2024-02-02T00:00:00Z",
                "kenmerken": {
                    "nummer": "1298329191",
                    "interneNotitie": "interneNotitie",
                    "soortPartij": SoortPartij.organisatie.value,
                },
            }
        )

    def test_send_notification_delete_object(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        m.assert_called_with(
            {
                "kanaal": "partijen",
                "hoofdObject": f"http://testserver{self.detail_url}",
                "resource": "partij",
                "resourceUrl": f"http://testserver{self.detail_url}",
                "actie": "destroy",
                "aanmaakdatum": "2024-02-02T00:00:00Z",
                "kenmerken": {
                    "nummer": "1298329191",
                    "interneNotitie": "interneNotitie",
                    "soortPartij": "organisatie",
                },
            }
        )


@freeze_time("2024-2-2T00:00:00Z")
@override_settings(NOTIFICATIONS_DISABLED=False)
@patch("notifications_api_common.viewsets.send_notification.delay")
class SendNotificationInterneTaakTestCase(NotificationsConfigTestCase, APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.actor = ActorFactory.create()
        cls.klantcontact = KlantcontactFactory.create()
        cls.internetaak = InterneTaakFactory.create(
            klantcontact=cls.klantcontact,
            nummer="1298329191",
            gevraagde_handeling="test",
            toelichting="test",
            status="te_verwerken",
        )

        cls.list_url = reverse("klantinteracties:internetaak-list")
        cls.detail_url = reverse(
            "klantinteracties:internetaak-detail",
            kwargs={"uuid": str(cls.internetaak.uuid)},
        )
        cls.data = {
            "toegewezenAanActor": {"uuid": str(cls.actor.uuid)},
            "aanleidinggevendKlantcontact": {"uuid": str(cls.klantcontact.uuid)},
            "nummer": "1312312312",
            "gevraagdeHandeling": "gevraagdeHandeling",
            "toelichting": "toelichting",
            "status": "verwerkt",
        }

    def test_send_notification_create_object(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.list_url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        m.assert_called_with(
            {
                "kanaal": "internetaken",
                "hoofdObject": data["url"],
                "resource": "internetaak",
                "resourceUrl": data["url"],
                "actie": "create",
                "aanmaakdatum": "2024-02-02T00:00:00Z",
                "kenmerken": {
                    "nummer": "1312312312",
                    "gevraagdeHandeling": "gevraagdeHandeling",
                    "toelichting": "toelichting",
                    "status": "verwerkt",
                },
            }
        )

    def test_send_notification_update_object(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.put(self.detail_url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        m.assert_called_with(
            {
                "kanaal": "internetaken",
                "hoofdObject": data["url"],
                "resource": "internetaak",
                "resourceUrl": data["url"],
                "actie": "update",
                "aanmaakdatum": "2024-02-02T00:00:00Z",
                "kenmerken": {
                    "nummer": "1312312312",
                    "gevraagdeHandeling": "gevraagdeHandeling",
                    "toelichting": "toelichting",
                    "status": "verwerkt",
                },
            }
        )

    def test_send_notification_partial_update_object(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.patch(self.detail_url, {"nummer": "123456789"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        m.assert_called_with(
            {
                "kanaal": "internetaken",
                "hoofdObject": data["url"],
                "resource": "internetaak",
                "resourceUrl": data["url"],
                "actie": "partial_update",
                "aanmaakdatum": "2024-02-02T00:00:00Z",
                "kenmerken": {
                    "nummer": "123456789",
                    "gevraagdeHandeling": "test",
                    "toelichting": "test",
                    "status": "te_verwerken",
                },
            }
        )

    def test_send_notification_delete_object(self, m):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        m.assert_called_with(
            {
                "kanaal": "internetaken",
                "hoofdObject": f"http://testserver{self.detail_url}",
                "resource": "internetaak",
                "resourceUrl": f"http://testserver{self.detail_url}",
                "actie": "destroy",
                "aanmaakdatum": "2024-02-02T00:00:00Z",
                "kenmerken": {
                    "nummer": "1298329191",
                    "gevraagdeHandeling": "test",
                    "toelichting": "test",
                    "status": "te_verwerken",
                },
            }
        )
