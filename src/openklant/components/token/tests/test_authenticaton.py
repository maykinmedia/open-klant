from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
)


class TestCrudCallsWithoutAuthorization(APITestCase):
    def test_list(self):
        list_url = reverse("klantinteracties:actor-list")
        ActorFactory.create_batch(2)

        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_read_actor(self):
        actor = ActorFactory.create()
        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_actor(self):
        list_url = reverse("klantinteracties:actor-list")

        response = self.client.post(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_actor(self):
        actor = ActorFactory.create()
        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )

        response = self.client.put(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_actor(self):
        actor = ActorFactory.create()
        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )

        response = self.client.patch(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_actor(self):
        actor = ActorFactory.create()
        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
