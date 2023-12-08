import uuid
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.test import override_settings

import requests_mock
from factory.django import FileField
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse
from zgw_consumers.constants import APITypes

from openklant.components.legacy.contactmomenten.models.constants import ObjectTypes
from openklant.components.legacy.contactmomenten.models.contactmomenten import (
    ObjectContactMoment,
)
from openklant.components.legacy.contactmomenten.models.tests.factories import (
    ContactMomentFactory,
    ObjectContactMomentFactory,
)
from openklant.components.tests.factories import ServiceFactory

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
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_objectcontactmoment(self, *mocks):
        ServiceFactory.create(
            api_root="http://example.com/api/v1/zaken",
            api_type=APITypes.zrc,
            oas_file=FileField(
                from_path=Path(settings.BASE_DIR)
                / "src"
                / "openklant"
                / "components"
                / "legacy"
                / "contactmomenten"
                / "api"
                / "tests"
                / "files"
                / "zaken.yaml"
            ),
        )
        contactmoment = ContactMomentFactory.create()
        contactmoment_url = reverse(contactmoment)
        list_url = reverse(ObjectContactMoment)
        data = {
            "contactmoment": contactmoment_url,
            "objectType": ObjectTypes.zaak,
            "object": ZAAK,
        }
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/api/v1/zaken/1",
                json={
                    "url": f"https://example.com/api/v1/zaakcontactmomenten/{uuid.uuid4()}",
                    "contactmoment": f"http://testserver/api/v1/contactmomenten/{uuid.uuid4()}",
                    "zaak": ZAAK,
                },
            )
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
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_objectcontactmoment_without_service(self, *mocks):
        contactmoment = ContactMomentFactory.create()
        contactmoment_url = reverse(contactmoment)
        list_url = reverse(ObjectContactMoment)
        data = {
            "contactmoment": contactmoment_url,
            "objectType": ObjectTypes.zaak,
            "object": ZAAK,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "configuration-error")

    @override_settings(
        LINK_FETCHER="vng_api_common.mocks.link_fetcher_200",
    )
    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_objectcontactmoment_service_does_not_match(self, *mocks):
        ServiceFactory.create(
            api_root="http://example.com/api/v2/zaken",
            api_type=APITypes.zrc,
            oas_file=FileField(
                from_path=Path(settings.BASE_DIR)
                / "src"
                / "openklant"
                / "components"
                / "legacy"
                / "contactmomenten"
                / "api"
                / "tests"
                / "files"
                / "zaken.yaml"
            ),
        )
        contactmoment = ContactMomentFactory.create()
        contactmoment_url = reverse(contactmoment)
        list_url = reverse(ObjectContactMoment)
        data = {
            "contactmoment": contactmoment_url,
            "objectType": ObjectTypes.zaak,
            "object": ZAAK,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "configuration-error")

    @override_settings(
        LINK_FETCHER="vng_api_common.mocks.link_fetcher_200",
    )
    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_objectcontactmoment_fail_no_remote_relation(self, *mocks):
        ServiceFactory.create(
            api_root="http://example.com/api/v1/zaken",
            api_type=APITypes.zrc,
            oas_file=FileField(
                from_path=Path(settings.BASE_DIR)
                / "src"
                / "openklant"
                / "components"
                / "legacy"
                / "contactmomenten"
                / "api"
                / "tests"
                / "files"
                / "zaken.yaml"
            ),
        )
        contactmoment = ContactMomentFactory.create()
        contactmoment_url = reverse(contactmoment)
        list_url = reverse(ObjectContactMoment)
        data = {
            "contactmoment": contactmoment_url,
            "objectType": ObjectTypes.zaak,
            "object": ZAAK,
        }
        with requests_mock.Mocker() as m:
            m.get("http://example.com/api/v1/zaken/1", json={})

            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "inconsistent-relation")

    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    def test_destroy_objectcontactmoment(self, *mocks):
        ServiceFactory.create(
            api_root="http://example.com/api/v1/zaken",
            api_type=APITypes.zrc,
            oas_file=FileField(
                from_path=Path(settings.BASE_DIR)
                / "src"
                / "openklant"
                / "components"
                / "legacy"
                / "contactmomenten"
                / "api"
                / "tests"
                / "files"
                / "zaken.yaml"
            ),
        )
        objectcontactmoment = ObjectContactMomentFactory.create(
            object=ZAAK, object_type=ObjectTypes.zaak
        )
        detail_url = reverse(objectcontactmoment)

        with requests_mock.Mocker() as m:
            m.get("http://example.com/api/v1/zaken/1", json={})
            response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ObjectContactMoment.objects.count(), 0)

    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    def test_destroy_without_service(self, *mocks):
        objectcontactmoment = ObjectContactMomentFactory.create(
            object=ZAAK, object_type=ObjectTypes.zaak
        )
        detail_url = reverse(objectcontactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "configuration-error")

    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    def test_destroyt_service_does_not_match(self, *mocks):
        ServiceFactory.create(
            api_root="http://example.com/api/v2/zaken",
            api_type=APITypes.zrc,
            oas_file=FileField(
                from_path=Path(settings.BASE_DIR)
                / "src"
                / "openklant"
                / "components"
                / "legacy"
                / "contactmomenten"
                / "api"
                / "tests"
                / "files"
                / "zaken.yaml"
            ),
        )
        objectcontactmoment = ObjectContactMomentFactory.create(
            object=ZAAK, object_type=ObjectTypes.zaak
        )
        detail_url = reverse(objectcontactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "configuration-error")

    @patch(
        "zds_client.client.get_operation_url",
        return_value="/api/v1/zaakcontactmomenten",
    )
    def test_destroy_fail_existing_relation(self, *mocks):
        ServiceFactory.create(
            api_root="http://example.com/api/v1/zaken",
            api_type=APITypes.zrc,
            oas_file=FileField(
                from_path=Path(settings.BASE_DIR)
                / "src"
                / "openklant"
                / "components"
                / "legacy"
                / "contactmomenten"
                / "api"
                / "tests"
                / "files"
                / "zaken.yaml"
            ),
        )
        objectcontactmoment = ObjectContactMomentFactory.create(
            object=ZAAK, object_type=ObjectTypes.zaak
        )
        detail_url = reverse(objectcontactmoment)
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/api/v1/zaken/1",
                json={
                    "url": f"https://example.com/api/v1/zaakcontactmomenten/{uuid.uuid4()}",
                    "contactmoment": f"http://testserver/api/v1/contactmomenten/{uuid.uuid4()}",
                    "zaak": ZAAK,
                },
            )
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
