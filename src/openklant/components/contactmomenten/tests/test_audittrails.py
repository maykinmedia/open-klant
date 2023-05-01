from copy import deepcopy

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.audittrails.models import AuditTrail
from vng_api_common.tests import JWTAuthMixin, reverse

from openklant.components.contactmomenten.models.constants import InitiatiefNemer
from openklant.components.contactmomenten.models.contactmomenten import ContactMoment

KLANT = "http://some.klanten.nl/api/v1/klanten/951e4660-3835-4643-8f9c-e523e364a30f"
MEDEWERKER = (
    "http://some.medewerkers.nl/api/v1/medewerkers/ffb1a466-fdad-4898-87fa-dae026df38c0"
)


class AuditTrailTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def _create_contactmoment(self):
        list_url = reverse(ContactMoment)
        data = {
            "bronorganisatie": "423182687",
            "klant": KLANT,
            "kanaal": "telephone",
            "tekst": "some text",
            "onderwerpLinks": [],
            "initiatiefnemer": InitiatiefNemer.gemeente,
            "medewerker": MEDEWERKER,
        }

        response = self.client.post(list_url, data)
        return response.data

    def test_create_contactmoment_audittrail(self):
        contactmoment_response = self._create_contactmoment()

        audittrails = AuditTrail.objects.filter(
            hoofd_object=contactmoment_response["url"]
        )
        self.assertEqual(audittrails.count(), 1)

        contactmoment_create_audittrail = audittrails.get()
        self.assertEqual(contactmoment_create_audittrail.bron, "Contactmomenten")
        self.assertEqual(contactmoment_create_audittrail.actie, "create")
        self.assertEqual(contactmoment_create_audittrail.resultaat, 201)
        self.assertEqual(contactmoment_create_audittrail.oud, None)
        self.assertEqual(contactmoment_create_audittrail.nieuw, contactmoment_response)

    def test_update_contactmoment_audittrails(self):
        contactmoment_data = self._create_contactmoment()
        modified_data = deepcopy(contactmoment_data)
        url = modified_data.pop("url")
        del modified_data["tekst"]
        modified_data["tekst"] = "new"

        response = self.client.put(url, modified_data)

        contactmoment_response = response.data

        audittrails = AuditTrail.objects.filter(
            hoofd_object=contactmoment_response["url"]
        )
        self.assertEqual(audittrails.count(), 2)

        contactmoment_update_audittrail = audittrails[1]
        self.assertEqual(contactmoment_update_audittrail.bron, "Contactmomenten")
        self.assertEqual(contactmoment_update_audittrail.actie, "update")
        self.assertEqual(contactmoment_update_audittrail.resultaat, 200)
        self.assertEqual(contactmoment_update_audittrail.oud, contactmoment_data)
        self.assertEqual(contactmoment_update_audittrail.nieuw, contactmoment_response)

    def test_partial_update_contactmoment_audittrails(self):
        contactmoment_data = self._create_contactmoment()

        response = self.client.patch(contactmoment_data["url"], {"tekst": "new"})
        contactmoment_response = response.data

        audittrails = AuditTrail.objects.filter(
            hoofd_object=contactmoment_response["url"]
        )
        self.assertEqual(audittrails.count(), 2)

        contactmoment_update_audittrail = audittrails[1]
        self.assertEqual(contactmoment_update_audittrail.bron, "Contactmomenten")
        self.assertEqual(contactmoment_update_audittrail.actie, "partial_update")
        self.assertEqual(contactmoment_update_audittrail.resultaat, 200)
        self.assertEqual(contactmoment_update_audittrail.oud, contactmoment_data)
        self.assertEqual(contactmoment_update_audittrail.nieuw, contactmoment_response)

    def test_delete_contactmoment_cascade_audittrails(self):
        contactmoment_data = self._create_contactmoment()

        # Delete the ContactMoment
        self.client.delete(contactmoment_data["url"])

        audittrails = AuditTrail.objects.filter(hoofd_object=contactmoment_data["url"])
        self.assertFalse(audittrails.exists())

    def test_read_audittrail(self):
        self._create_contactmoment()

        contactmoment = ContactMoment.objects.get()
        audittrails = AuditTrail.objects.get()
        audittrails_url = reverse(
            audittrails, kwargs={"contactmoment_uuid": contactmoment.uuid}
        )

        response_audittrails = self.client.get(audittrails_url)

        self.assertEqual(response_audittrails.status_code, status.HTTP_200_OK)
