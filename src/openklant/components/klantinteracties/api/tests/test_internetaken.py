from freezegun import freeze_time
from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
)
from openklant.components.klantinteracties.models.tests.factories.internetaken import (
    InterneTaakFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    KlantcontactFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class InterneTaakTests(APITestCase):
    def test_list_internetaak(self):
        list_url = reverse("klantinteracties:internetaak-list")
        InterneTaakFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_internetaak(self):
        internetaak = InterneTaakFactory.create()
        detail_url = reverse(
            "klantinteracties:internetaak-detail",
            kwargs={"uuid": str(internetaak.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2024-01-01T12:00:00Z")
    def test_create_internetaak(self):
        actor = ActorFactory.create()
        klantcontact = KlantcontactFactory.create()

        list_url = reverse("klantinteracties:internetaak-list")
        data = {
            "toegewezenAanActor": {"uuid": str(actor.uuid)},
            "aanleidinggevendKlantcontact": {"uuid": str(klantcontact.uuid)},
            "nummer": "1312312312",
            "gevraagdeHandeling": "gevraagdeHandeling",
            "toelichting": "toelichting",
            "status": "verwerkt",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["toegewezenAanActor"]["uuid"], str(actor.uuid))
        self.assertEqual(
            response_data["aanleidinggevendKlantcontact"]["uuid"],
            str(klantcontact.uuid),
        )
        self.assertEqual(response_data["nummer"], "1312312312")
        self.assertEqual(response_data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(response_data["toelichting"], "toelichting")
        self.assertEqual(response_data["status"], "verwerkt")
        self.assertTrue(
            InterneTaak.objects.filter(afgehandeld_op="2024-01-01T12:00:00Z").exists()
        )

        with self.subTest("auto_generate_max_nummer_plus_one"):
            data["nummer"] = ""
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = response.json()
            self.assertEqual(response_data["nummer"], "1312312313")

        with self.subTest("auto_generate_nummer_unique_validation"):
            data["nummer"] = "1312312313"
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(
                response_data["invalidParams"][0]["reason"],
                "Er bestaat al een interne taak met eenzelfde nummer.",
            )

        with self.subTest("auto_generate_nummer_over_10_characters_error_message"):
            InterneTaakFactory.create(nummer="9999999999")
            data["nummer"] = ""
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
            response_data = response.json()
            self.assertEqual(
                response_data["detail"],
                "Er kon niet automatisch een opvolgend nummer worden gegenereerd. "
                "Het maximaal aantal tekens is bereikt.",
            )

    @freeze_time("2024-01-01T12:00:00Z")
    def test_create_internetaak_with_status_te_verwerken(self):
        actor = ActorFactory.create()
        klantcontact = KlantcontactFactory.create()

        list_url = reverse("klantinteracties:internetaak-list")
        data = {
            "toegewezenAanActor": {"uuid": str(actor.uuid)},
            "aanleidinggevendKlantcontact": {"uuid": str(klantcontact.uuid)},
            "nummer": "1312312312",
            "gevraagdeHandeling": "gevraagdeHandeling",
            "toelichting": "toelichting",
            "status": "te_verwerken",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["toegewezenAanActor"]["uuid"], str(actor.uuid))
        self.assertEqual(
            response_data["aanleidinggevendKlantcontact"]["uuid"],
            str(klantcontact.uuid),
        )
        self.assertEqual(response_data["nummer"], "1312312312")
        self.assertEqual(response_data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(response_data["toelichting"], "toelichting")
        self.assertEqual(response_data["status"], "te_verwerken")
        self.assertFalse(
            InterneTaak.objects.filter(afgehandeld_op="2024-01-01T12:00:00Z").exists()
        )

    @freeze_time("2024-01-01T12:00:00Z")
    def test_update_internetaak(self):
        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        internetaak = InterneTaakFactory.create(
            actor=actor,
            klantcontact=klantcontact,
            nummer="1237713712",
            gevraagde_handeling="gevraagdeHandeling",
            toelichting="toelichting",
            status="te_verwerken",
        )
        detail_url = reverse(
            "klantinteracties:internetaak-detail",
            kwargs={"uuid": str(internetaak.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["toegewezenAanActor"]["uuid"], str(actor.uuid))
        self.assertEqual(
            data["aanleidinggevendKlantcontact"]["uuid"], str(klantcontact.uuid)
        )
        self.assertEqual(data["nummer"], "1237713712")
        self.assertEqual(data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(data["toelichting"], "toelichting")
        self.assertEqual(data["status"], "te_verwerken")

        data = {
            "toegewezenAanActor": {"uuid": str(actor2.uuid)},
            "aanleidinggevendKlantcontact": {"uuid": str(klantcontact2.uuid)},
            "nummer": "9999999999",
            "gevraagdeHandeling": "changed",
            "toelichting": "changed",
            "status": "verwerkt",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["toegewezenAanActor"]["uuid"], str(actor2.uuid))
        self.assertEqual(
            data["aanleidinggevendKlantcontact"]["uuid"], str(klantcontact2.uuid)
        )
        self.assertEqual(data["nummer"], "9999999999")
        self.assertEqual(data["gevraagdeHandeling"], "changed")
        self.assertEqual(data["toelichting"], "changed")
        self.assertEqual(data["status"], "verwerkt")
        self.assertTrue(
            InterneTaak.objects.filter(afgehandeld_op="2024-01-01T12:00:00Z").exists()
        )

        with freeze_time("2024-01-01T12:20:00Z") and self.subTest(
            "updating_on_later_date_does_not_change_afgehandeld_op"
        ):
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertFalse(
                InterneTaak.objects.filter(
                    afgehandeld_op="2024-01-01T12:20:00Z"
                ).exists()
            )

        with self.subTest(
            "changing_status_back_to_te_verwerken_clears_afgehandeld_op_field"
        ):
            data = {
                "toegewezenAanActor": {"uuid": str(actor2.uuid)},
                "aanleidinggevendKlantcontact": {"uuid": str(klantcontact2.uuid)},
                "gevraagdeHandeling": "changed",
                "status": "te_verwerken",
            }
            response = self.client.put(detail_url, data)
            data = response.json()
            self.assertEqual(data["status"], "te_verwerken")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(InterneTaak.objects.count(), 1)
            self.assertIsNone(InterneTaak.objects.first().afgehandeld_op)

    def test_partial_update_internetaak(self):
        actor = ActorFactory.create()
        klantcontact = KlantcontactFactory.create()
        internetaak = InterneTaakFactory.create(
            actor=actor,
            klantcontact=klantcontact,
            nummer="1237713712",
            gevraagde_handeling="gevraagdeHandeling",
            toelichting="toelichting",
            status="verwerkt",
        )
        detail_url = reverse(
            "klantinteracties:internetaak-detail",
            kwargs={"uuid": str(internetaak.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["toegewezenAanActor"]["uuid"], str(actor.uuid))
        self.assertEqual(
            data["aanleidinggevendKlantcontact"]["uuid"], str(klantcontact.uuid)
        )
        self.assertEqual(data["nummer"], "1237713712")
        self.assertEqual(data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(data["toelichting"], "toelichting")
        self.assertEqual(data["status"], "verwerkt")

        data = {"nummer": "0000000000"}

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["toegewezenAanActor"]["uuid"], str(actor.uuid))
        self.assertEqual(
            data["aanleidinggevendKlantcontact"]["uuid"], str(klantcontact.uuid)
        )
        self.assertEqual(data["nummer"], "0000000000")
        self.assertEqual(data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(data["toelichting"], "toelichting")
        self.assertEqual(data["status"], "verwerkt")

    def test_destroy_internetaak(self):
        internetaak = InterneTaakFactory.create()
        detail_url = reverse(
            "klantinteracties:internetaak-detail",
            kwargs={"uuid": str(internetaak.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:internetaak-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
