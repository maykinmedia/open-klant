from openklant.tests.test_migrate import BaseMigrationTest


class TestTokenAuthUniqueness(BaseMigrationTest):
    app = "token"
    migrate_from = "0001_initial"
    migrate_to = "0002_identifier_migration"

    def test_migrate_tokens_to_unique_values(self):
        TokenAuth = self.old_app_state.get_model("token", "TokenAuth")

        TokenAuth.objects.create(
            token="aa018d1c576c9dae33be1e549f739f2834ebc811",
            contact_person="Person 1",
            email="test@example.com",
        )

        TokenAuth.objects.create(
            token="aa018d1c576c9dae33be1e549f739f2834ebc811",
            contact_person="Person 2",
            email="duplicate@example.com",
        )

        TokenAuth.objects.create(
            token="ab700d6bf906c2b4b42a961c529657314c6a8246",
            contact_person="Other person",
            email="somebody@else.com",
        )

        self._perform_migration()

        TokenAuth = self.apps.get_model("token", "TokenAuth")

        tokens = TokenAuth.objects.all()

        self.assertEqual(tokens.count(), 3)

        test_token = tokens.get(email="test@example.com")
        duplicate_token = tokens.get(email="duplicate@example.com")
        unrelated_token = tokens.get(email="somebody@else.com")

        self.assertNotEqual(
            test_token.token, "aa018d1c576c9dae33be1e549f739f2834ebc811"
        )
        self.assertNotEqual(
            duplicate_token.token, "aa018d1c576c9dae33be1e549f739f2834ebc811"
        )
        self.assertNotEqual(test_token.token, duplicate_token.token)

        # unrelated token should be not be mutated
        self.assertEqual(
            unrelated_token.token, "ab700d6bf906c2b4b42a961c529657314c6a8246"
        )

    def test_migrate_tokens_to_unique_identifiers(self):
        TokenAuth = self.old_app_state.get_model("token", "TokenAuth")

        TokenAuth.objects.create(
            token="aa018d1c576c9dae33be1e549f739f2834ebc811",
            contact_person="Person 1",
            email="test@example.com",
        )

        TokenAuth.objects.create(
            token="ab700d6bf906c2b4b42a961c529657314c6a8246",
            contact_person="Other person",
            email="somebody@else.com",
        )

        self._perform_migration()

        TokenAuth = self.apps.get_model("token", "TokenAuth")

        tokens = TokenAuth.objects.all()

        self.assertEqual(tokens.count(), 2)

        first_token = tokens[0]
        last_token = tokens[1]

        self.assertTrue(first_token.token)
        self.assertTrue(last_token.token)

        self.assertNotEqual(first_token.identifier, last_token.identifier)
