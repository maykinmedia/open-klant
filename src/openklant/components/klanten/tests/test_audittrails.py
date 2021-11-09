from copy import deepcopy

import requests_mock
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.audittrails.models import AuditTrail
from vng_api_common.tests import JWTAuthMixin, reverse

from ..datamodel.constants import KlantType
from ..datamodel.models import Klant

SUBJECT = "https://example.com/subject/1"


class AuditTrailTests(JWTAuthMixin, APITestCase):

    heeft_alle_autorisaties = True

    def _create_klant(self):
        list_url = reverse(Klant)
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
            response = self.client.post(list_url, data)

        return response.data

    def test_create_klant_audittrail(self):
        klant_response = self._create_klant()

        audittrails = AuditTrail.objects.filter(hoofd_object=klant_response["url"])
        self.assertEqual(audittrails.count(), 1)

        klant_create_audittrail = audittrails.get()
        self.assertEqual(klant_create_audittrail.bron, "Klanten")
        self.assertEqual(klant_create_audittrail.actie, "create")
        self.assertEqual(klant_create_audittrail.resultaat, 201)
        self.assertEqual(klant_create_audittrail.oud, None)
        self.assertEqual(klant_create_audittrail.nieuw, klant_response)

    def test_update_klant_audittrails(self):
        klant_data = self._create_klant()
        modified_data = deepcopy(klant_data)
        url = modified_data.pop("url")
        del modified_data["subject_identificatie"]
        modified_data["emailadres"] = "new@gmail.com"

        with requests_mock.Mocker() as m:
            m.get(SUBJECT, json={})
            response = self.client.put(url, modified_data)

        klant_response = response.data

        audittrails = AuditTrail.objects.filter(
            hoofd_object=klant_response["url"]
        ).order_by("pk")
        self.assertEqual(audittrails.count(), 2)

        klant_update_audittrail = audittrails[1]
        self.assertEqual(klant_update_audittrail.bron, "Klanten")
        self.assertEqual(klant_update_audittrail.actie, "update")
        self.assertEqual(klant_update_audittrail.resultaat, 200)
        self.assertEqual(klant_update_audittrail.oud, klant_data)
        self.assertEqual(klant_update_audittrail.nieuw, klant_response)

    def test_partial_update_klant_audittrails(self):
        klant_data = self._create_klant()

        response = self.client.patch(klant_data["url"], {"emailadres": "new@gmail.com"})
        klant_response = response.data

        audittrails = AuditTrail.objects.filter(
            hoofd_object=klant_response["url"]
        ).order_by("pk")
        self.assertEqual(audittrails.count(), 2)

        klant_update_audittrail = audittrails[1]
        self.assertEqual(klant_update_audittrail.bron, "Klanten")
        self.assertEqual(klant_update_audittrail.actie, "partial_update")
        self.assertEqual(klant_update_audittrail.resultaat, 200)
        self.assertEqual(klant_update_audittrail.oud, klant_data)
        self.assertEqual(klant_update_audittrail.nieuw, klant_response)

    def test_delete_klant_cascade_audittrails(self):
        klant_data = self._create_klant()

        # Delete the Klant
        self.client.delete(klant_data["url"])

        audittrails = AuditTrail.objects.filter(hoofd_object=klant_data["url"])
        self.assertFalse(audittrails.exists())

    def test_read_audittrail(self):
        self._create_klant()

        klant = Klant.objects.get()
        audittrails = AuditTrail.objects.get()
        audittrails_url = reverse(audittrails, kwargs={"klant_uuid": klant.uuid})

        response_audittrails = self.client.get(audittrails_url)

        self.assertEqual(response_audittrails.status_code, status.HTTP_200_OK)
