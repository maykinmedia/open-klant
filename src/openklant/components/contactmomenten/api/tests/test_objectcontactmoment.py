import uuid
from unittest.mock import patch

from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse
from zds_client.tests.mocks import mock_client

from openklant.components.contactmomenten.datamodel.constants import ObjectTypes
from openklant.components.contactmomenten.datamodel.models import ObjectContactMoment
from openklant.components.contactmomenten.datamodel.tests.factories import (
    ContactMomentFactory,
    ObjectContactMomentFactory,
)

ZAAK = "http://example.com/api/v1/zaken/1"


class ObjectContactMomentTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_objectcontactmomenten(self):
        list_url = reverse(ObjectContactMoment)
        ObjectContactMomentFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_objectcontactmoment(self):
        contactmoment = ContactMomentFactory.create()
        contactmoment_url = reverse(contactmoment)
        objectcontactmoment = ObjectContactMomentFactory.create(
            contactmoment=contactmoment
        )
        detail_url = reverse(objectcontactmoment)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "contactmoment": f"http://testserver{contactmoment_url}",
                "objectType": objectcontactmoment.object_type,
                "object": objectcontactmoment.object,
            },
        )

    @override_settings(
        LINK_FETCHER="vng_api_common.mocks.link_fetcher_200",
    )
    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    @patch("zds_client.tests.mocks.MockClient.fetch_schema", return_value={})
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_objectcontactmoment(self, *mocks):
        contactmoment = ContactMomentFactory.create()
        contactmoment_url = reverse(contactmoment)
        list_url = reverse(ObjectContactMoment)
        data = {
            "contactmoment": contactmoment_url,
            "objectType": ObjectTypes.zaak,
            "object": ZAAK,
        }
        responses = {
            "http://example.com/api/v1/zaakcontactmomenten": [
                {
                    "url": f"https://example.com/api/v1/zaakcontactmomenten/{uuid.uuid4()}",
                    "contactmoment": f"http://testserver/api/v1/contactmomenten/{uuid.uuid4()}",
                    "zaak": ZAAK,
                }
            ]
        }
        with mock_client(responses):
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        objectcontactmoment = ObjectContactMoment.objects.get()

        self.assertEqual(objectcontactmoment.contactmoment, contactmoment)
        self.assertEqual(objectcontactmoment.object_type, ObjectTypes.zaak)
        self.assertEqual(objectcontactmoment.object, ZAAK)

    @override_settings(
        LINK_FETCHER="vng_api_common.mocks.link_fetcher_200",
    )
    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    @patch("zds_client.tests.mocks.MockClient.fetch_schema", return_value={})
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_objectcontactmoment_fail_no_remote_relation(self, *mocks):
        contactmoment = ContactMomentFactory.create()
        contactmoment_url = reverse(contactmoment)
        list_url = reverse(ObjectContactMoment)
        data = {
            "contactmoment": contactmoment_url,
            "objectType": ObjectTypes.zaak,
            "object": ZAAK,
        }
        responses = {"http://example.com/api/v1/zaakcontactmomenten": []}
        with mock_client(responses):
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "inconsistent-relation")

    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    @patch("zds_client.tests.mocks.MockClient.fetch_schema", return_value={})
    def test_destroy_objectcontactmoment(self, *mocks):
        objectcontactmoment = ObjectContactMomentFactory.create(
            object=ZAAK, object_type=ObjectTypes.zaak
        )
        detail_url = reverse(objectcontactmoment)
        responses = {"http://example.com/api/v1/zaakcontactmomenten": []}

        with mock_client(responses):
            response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ObjectContactMoment.objects.count(), 0)

    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    @patch("zds_client.tests.mocks.MockClient.fetch_schema", return_value={})
    def test_destroy_fail_existing_relation(self, *mocks):
        objectcontactmoment = ObjectContactMomentFactory.create(
            object=ZAAK, object_type=ObjectTypes.zaak
        )
        detail_url = reverse(objectcontactmoment)
        responses = {
            "http://example.com/api/v1/zaakcontactmomenten": [
                {
                    "url": f"https://example.com/api/v1/zaakcontactmomenten/{uuid.uuid4()}",
                    "contactmoment": f"http://testserver/api/v1/contactmomenten/{uuid.uuid4()}",
                    "zaak": ZAAK,
                }
            ]
        }

        with mock_client(responses):
            response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "remote-relation-exists")


class ObjectContactMomentFilterTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True
    list_url = reverse(ObjectContactMoment)

    def test_filter_contactmoment(self):
        oio = ObjectContactMomentFactory.create()
        contactmoment_url = reverse(oio.contactmoment)

        response = self.client.get(
            self.list_url,
            {"contactmoment": f"http://testserver.com{contactmoment_url}"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["contactmoment"],
            f"http://testserver.com{contactmoment_url}",
        )

    def test_filter_object(self):
        oio = ObjectContactMomentFactory.create()

        response = self.client.get(self.list_url, {"object": oio.object})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["object"], oio.object)

    def test_filter_object_type(self):
        ObjectContactMomentFactory.create(object_type=ObjectTypes.zaak)

        response = self.client.get(self.list_url, {"objectType": ObjectTypes.zaak})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["object_type"], ObjectTypes.zaak)

    def test_pagination_default(self):
        ObjectContactMomentFactory.create_batch(2)
        url = reverse(ObjectContactMoment)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        ObjectContactMomentFactory.create_batch(2)
        url = reverse(ObjectContactMoment)

        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
