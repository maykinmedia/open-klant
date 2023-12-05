from rest_framework.test import APITestCase as APITestCaseDRF

from openklant.components.token.tests.factories.token import TokenAuthFactory


class APITestCase(APITestCaseDRF):
    def setUp(self):
        super().setUp()
        self.token_auth = TokenAuthFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_auth.token)
