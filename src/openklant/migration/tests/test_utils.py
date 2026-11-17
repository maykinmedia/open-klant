from django.test import TestCase

from openklant.components.token.models import TokenAuth
from openklant.components.token.tests.factories.token import TokenAuthFactory
from openklant.migration.utils import MIGRATION_TOKEN_IDENTIFIER, _generate_dummy_token


class GenerateDummyTokenTests(TestCase):
    def test_creates_token_if_none_exists(self):
        token = _generate_dummy_token()

        token_auth = TokenAuth.objects.get(application=MIGRATION_TOKEN_IDENTIFIER)
        self.assertEqual(token, token_auth.token)

    def test_reuses_existing_token(self):
        existing = TokenAuthFactory.create(application=MIGRATION_TOKEN_IDENTIFIER)

        token = _generate_dummy_token()

        self.assertEqual(token, existing.token)
        self.assertEqual(
            TokenAuth.objects.filter(application=MIGRATION_TOKEN_IDENTIFIER).count(), 1
        )

    def test_keeps_first_token_and_removes_duplicates(self):
        first, *_ = TokenAuthFactory.create_batch(
            3, application=MIGRATION_TOKEN_IDENTIFIER
        )
        other_token = TokenAuthFactory.create(application="Other application")

        token = _generate_dummy_token()

        self.assertEqual(token, first.token)
        self.assertQuerySetEqual(
            TokenAuth.objects.filter(application=MIGRATION_TOKEN_IDENTIFIER),
            [first],
        )
        self.assertTrue(TokenAuth.objects.filter(pk=other_token.pk).exists())
