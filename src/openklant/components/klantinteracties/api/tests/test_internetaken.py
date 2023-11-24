from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
)
from openklant.components.klantinteracties.models.tests.factories.internetaken import (
    InterneTaakFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    KlantcontactFactory,
)


class InterneTaakTests(JWTAuthMixin, APITestCase):
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

        data = response.json()

        self.assertEqual(data["toegewezenAanActor"]["uuid"], str(actor.uuid))
        self.assertEqual(
            data["aanleidinggevendKlantcontact"]["uuid"], str(klantcontact.uuid)
        )
        self.assertEqual(data["nummer"], "1312312312")
        self.assertEqual(data["gevraagdeHandeling"], "gevraagdeHandeling")
        self.assertEqual(data["toelichting"], "toelichting")
        self.assertEqual(data["status"], "verwerkt")

    def test_update_internetaak(self):
        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
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

        data = {
            "toegewezenAanActor": {"uuid": str(actor2.uuid)},
            "aanleidinggevendKlantcontact": {"uuid": str(klantcontact2.uuid)},
            "nummer": "9999999999",
            "gevraagdeHandeling": "changed",
            "toelichting": "changed",
            "status": "te_verwerken",
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
        self.assertEqual(data["status"], "te_verwerken")

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
