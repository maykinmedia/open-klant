from freezegun import freeze_time
from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    InterneTaakFactory,
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

    def test_list_pagination_pagesize_param(self):
        list_url = reverse("klantinteracties:internetaak-list")
        InterneTaakFactory.create_batch(10)

        response = self.client.get(list_url, {"pageSize": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 10)
        self.assertEqual(len(data["results"]), 5)
        self.assertEqual(data["next"], f"http://testserver{list_url}?page=2&pageSize=5")

    def test_read_internetaak(self):
        internetaak = InterneTaakFactory.create()
        detail_url = reverse(
            "klantinteracties:internetaak-detail",
            kwargs={"uuid": str(internetaak.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

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
        self.assertEqual(len(response_data["toegewezenAanActoren"]), 1)
        self.assertEqual(
            response_data["toegewezenAanActoren"][0]["uuid"],
            str(actor.uuid),
        )
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
        self.assertEqual(len(response_data["toegewezenAanActoren"]), 1)
        self.assertEqual(
            response_data["toegewezenAanActoren"][0]["uuid"],
            str(actor.uuid),
        )
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

        with self.subTest("validate_afgehandeld_op_error_with_te_verwerken_status"):
            del data["nummer"]
            data["afgehandeldOp"] = "2024-01-01T01:00:00Z"
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(response_data["invalidParams"][0]["name"], "afgehandeldOp")
            self.assertEqual(
                response_data["invalidParams"][0]["reason"],
                "De Internetaak kan geen afgehandeld op datum bevatten als de status niet op 'verwerkt' staat.",
            )

    def test_create_internetaak_with_afgehandeld_op_date(self):
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
            "afgehandeldOp": "2024-01-01T01:00:00Z",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["toegewezenAanActor"]["uuid"], str(actor.uuid))
        self.assertEqual(len(response_data["toegewezenAanActoren"]), 1)
        self.assertEqual(
            response_data["toegewezenAanActoren"][0]["uuid"],
            str(actor.uuid),
        )
        self.assertEqual(
            response_data["toegewezenAanActoren"][0]["uuid"], str(actor.uuid)
        )
        self.assertEqual(
            response_data["aanleidinggevendKlantcontact"]["uuid"],
            str(klantcontact.uuid),
        )
        self.assertEqual(response_data["nummer"], "1312312312")
        self.assertEqual(response_data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(response_data["toelichting"], "toelichting")
        self.assertEqual(response_data["status"], "verwerkt")
        self.assertTrue(
            InterneTaak.objects.filter(afgehandeld_op="2024-01-01T01:00:00Z").exists()
        )

    def test_create_internetaak_with_multiple_actoren(self):
        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact = KlantcontactFactory.create()

        list_url = reverse("klantinteracties:internetaak-list")

        data = {
            "toegewezenAanActoren": [
                {"uuid": str(actor2.uuid)},
                {"uuid": str(actor.uuid)},
            ],
            "aanleidinggevendKlantcontact": {"uuid": str(klantcontact.uuid)},
            "nummer": "1312312312",
            "gevraagdeHandeling": "gevraagdeHandeling",
            "toelichting": "toelichting",
            "status": "verwerkt",
            "afgehandeldOp": "2024-01-01T01:00:00Z",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["toegewezenAanActor"]["uuid"], str(actor2.uuid))
        self.assertEqual(
            response_data["toegewezenAanActoren"][0]["uuid"],
            str(actor2.uuid),
        )
        self.assertEqual(
            response_data["toegewezenAanActoren"][1]["uuid"],
            str(actor.uuid),
        )
        self.assertEqual(
            response_data["aanleidinggevendKlantcontact"]["uuid"],
            str(klantcontact.uuid),
        )
        self.assertEqual(response_data["nummer"], "1312312312")
        self.assertEqual(response_data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(response_data["toelichting"], "toelichting")
        self.assertEqual(response_data["status"], "verwerkt")
        self.assertTrue(
            InterneTaak.objects.filter(afgehandeld_op="2024-01-01T01:00:00Z").exists()
        )

    @freeze_time("2024-01-01T12:00:00Z")
    def test_update_internetaak(self):
        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        internetaak = InterneTaakFactory.create(
            actoren=[actor],
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
        self.assertEqual(len(data["toegewezenAanActoren"]), 1)
        self.assertEqual(
            data["toegewezenAanActoren"][0]["uuid"],
            str(actor.uuid),
        )
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
        self.assertEqual(len(data["toegewezenAanActoren"]), 1)
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
            # remove other actoren field
            del data["toegewezenAanActoren"]
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

        with self.subTest("with_afgehandeld_op_data_value"):
            data = {
                "toegewezenAanActor": {"uuid": str(actor2.uuid)},
                "aanleidinggevendKlantcontact": {"uuid": str(klantcontact2.uuid)},
                "gevraagdeHandeling": "changed",
                "status": "verwerkt",
                "afgehandeldOp": "2024-01-01T01:00:00Z",
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
                InterneTaak.objects.filter(
                    afgehandeld_op="2024-01-01T01:00:00Z"
                ).exists()
            )

        with self.subTest("validate_afgehandeld_op_error_with_te_verwerken_status"):
            data = {
                "toegewezenAanActor": {"uuid": str(actor2.uuid)},
                "aanleidinggevendKlantcontact": {"uuid": str(klantcontact2.uuid)},
                "gevraagdeHandeling": "changed",
                "status": "te_verwerken",
                "afgehandeldOp": "2024-01-01T01:00:00Z",
            }
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "afgehandeldOp")
            self.assertEqual(
                data["invalidParams"][0]["reason"],
                "De Internetaak kan geen afgehandeld op datum bevatten als de status niet op 'verwerkt' staat.",
            )

        with self.subTest("validate_acoren_field_required_neither_fields"):
            # no toegewezen_aan_actoren and toegewezen_aan_actor
            data = {
                "aanleidinggevendKlantcontact": {"uuid": str(klantcontact2.uuid)},
                "gevraagdeHandeling": "changed",
                "status": "te_verwerken",
                "afgehandeldOp": "2024-01-01T01:00:00Z",
            }
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "nonFieldErrors")
            self.assertEqual(
                data["invalidParams"][0]["reason"],
                "`toegewezen_aan_actor` of `toegewezen_aan_actoren` is required (mag niet beiden gebruiken).",
            )

        with self.subTest("validate_acoren_field_required_both_fields"):
            # no toegewezen_aan_actoren and toegewezen_aan_actor
            data = {
                "toegewezenAanActor": {"uuid": str(actor2.uuid)},
                "toegewezenAanActoren": [{"uuid": str(actor2.uuid)}],
                "aanleidinggevendKlantcontact": {"uuid": str(klantcontact2.uuid)},
                "gevraagdeHandeling": "changed",
                "status": "te_verwerken",
                "afgehandeldOp": "2024-01-01T01:00:00Z",
            }
            response = self.client.put(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "nonFieldErrors")
            self.assertEqual(
                data["invalidParams"][0]["reason"],
                "`toegewezen_aan_actor` en `toegewezen_aan_actoren` mag niet beiden gebruikt worden.",
            )

    @freeze_time("2024-01-01T12:00:00Z")
    def test_update_internetaak_with_multiple_actoren(self):
        actor, actor2, actor3 = ActorFactory.create_batch(3)
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        internetaak = InterneTaakFactory.create(
            actoren=[actor],
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
        self.assertEqual(len(data["toegewezenAanActoren"]), 1)
        self.assertEqual(
            data["toegewezenAanActoren"][0]["uuid"],
            str(actor.uuid),
        )
        self.assertEqual(
            data["aanleidinggevendKlantcontact"]["uuid"], str(klantcontact.uuid)
        )
        self.assertEqual(data["nummer"], "1237713712")
        self.assertEqual(data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(data["toelichting"], "toelichting")
        self.assertEqual(data["status"], "te_verwerken")

        data = {
            "toegewezenAanActoren": [
                {"uuid": str(actor3.uuid)},
                {"uuid": str(actor2.uuid)},
            ],
            "aanleidinggevendKlantcontact": {"uuid": str(klantcontact2.uuid)},
            "nummer": "9999999999",
            "gevraagdeHandeling": "changed",
            "toelichting": "changed",
            "status": "verwerkt",
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data["toegewezenAanActor"]["uuid"], str(actor3.uuid))
        self.assertEqual(len(response_data["toegewezenAanActoren"]), 2)
        self.assertEqual(
            response_data["toegewezenAanActoren"][0]["uuid"],
            str(actor3.uuid),
        )
        self.assertEqual(
            response_data["toegewezenAanActoren"][1]["uuid"],
            str(actor2.uuid),
        )
        self.assertEqual(
            response_data["aanleidinggevendKlantcontact"]["uuid"],
            str(klantcontact2.uuid),
        )
        self.assertEqual(response_data["nummer"], "9999999999")
        self.assertEqual(response_data["gevraagdeHandeling"], "changed")
        self.assertEqual(response_data["toelichting"], "changed")
        self.assertEqual(response_data["status"], "verwerkt")
        self.assertTrue(
            InterneTaak.objects.filter(afgehandeld_op="2024-01-01T12:00:00Z").exists()
        )

        with self.subTest(
            "update_toegewezen_aan_actor_resoltes_in_one_actor_being_set"
        ):
            # no toegewezen_aan_actoren and toegewezen_aan_actor
            del data["toegewezenAanActoren"]
            data = {
                "toegewezenAanActor": {"uuid": str(actor.uuid)},
            }
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()

            self.assertEqual(
                response_data["toegewezenAanActor"]["uuid"], str(actor.uuid)
            )
            self.assertEqual(len(response_data["toegewezenAanActoren"]), 1)
            self.assertEqual(
                response_data["toegewezenAanActoren"][0]["uuid"],
                str(actor.uuid),
            )

    def test_partial_update_internetaak(self):
        actor = ActorFactory.create()
        klantcontact = KlantcontactFactory.create()
        internetaak = InterneTaakFactory.create(
            actoren=[actor],
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

        with self.subTest("disable_actoren_validation"):
            # no toegewezen_aan_actoren and toegewezen_aan_actor
            data = {
                "gevraagdeHandeling": "changed",
            }
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

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
