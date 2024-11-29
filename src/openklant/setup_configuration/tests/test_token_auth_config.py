from pathlib import Path

from django.test import TestCase

from django_setup_configuration.test_utils import execute_single_step

from openklant.components.token.models import TokenAuth
from openklant.components.token.tests.factories.token import TokenAuthFactory
from openklant.setup_configuration.steps import TokenAuthConfigurationStep


TEST_FILES = (Path(__file__).parent / "files").resolve()


class TokenAuthConfigurationStepTests(TestCase):
    def test_empty_database(self):
        test_file_path = str(TEST_FILES / "token_empty_database.yaml")

        execute_single_step(
            TokenAuthConfigurationStep, yaml_source=test_file_path
        )

        tokens = TokenAuth.objects.order_by("created")

        self.assertEqual(tokens.count(), 2)

        first_token: TokenAuth = tokens[0]

        self.assertEqual(first_token.identifier, "token-1")
        self.assertEqual(first_token.contact_person, "Person 1")
        self.assertEqual(first_token.email, "person-1@example.com")
        self.assertEqual(first_token.organization, "")
        self.assertEqual(first_token.application, "")
        self.assertEqual(first_token.administration, "")

        second_token: TokenAuth = tokens[1]

        self.assertEqual(second_token.identifier, "token-2")
        self.assertEqual(second_token.contact_person, "Person 2")
        self.assertEqual(second_token.email, "person-2@example.com")
        self.assertEqual(second_token.organization, "")
        self.assertEqual(second_token.application, "")
        self.assertEqual(second_token.administration, "")

    def test_existing_tokens(self):
        TokenAuthFactory(
            identifier="token-1",
            contact_person="Person 4",
            email="person-4@example.com",
        )

        TokenAuthFactory(
            identifier="token-2",
            contact_person="Person 2",
            email="person-2@example.com",
        )

        test_file_path = str(TEST_FILES / "token_existing_tokens.yaml")

        execute_single_step(TokenAuthConfigurationStep, yaml_source=test_file_path)

        tokens = TokenAuth.objects.order_by("created")

        self.assertEqual(tokens.count(), 3)

        first_token: TokenAuth = tokens[0]

        self.assertEqual(first_token.identifier, "token-1")
        self.assertEqual(first_token.contact_person, "Person 1")
        self.assertEqual(first_token.email, "person-1@example.com")
        self.assertEqual(first_token.organization, "")
        self.assertEqual(first_token.application, "")
        self.assertEqual(first_token.administration, "")

        second_token: TokenAuth = tokens[1]

        self.assertEqual(second_token.identifier, "token-2")
        self.assertEqual(second_token.contact_person, "Person 2")
        self.assertEqual(second_token.email, "person-2@example.com")
        self.assertEqual(second_token.organization, "")
        self.assertEqual(second_token.application, "")
        self.assertEqual(second_token.administration, "")

        third_token: TokenAuth = tokens[2]

        self.assertEqual(third_token.identifier, "token-3")
        self.assertEqual(third_token.contact_person, "Person 3")
        self.assertEqual(third_token.email, "person-3@example.com")
        self.assertEqual(third_token.organization, "")
        self.assertEqual(third_token.application, "")
        self.assertEqual(third_token.administration, "")

    def test_with_all_fields(self):
        TokenAuthFactory(
            identifier="token-1",
            contact_person="Person 4",
            email="person-4@example.com",
        )

        TokenAuthFactory(
            identifier="token-2",
            contact_person="Person 2",
            email="person-2@example.com",
        )

        test_file_path = str(TEST_FILES / "token_all_fields.yaml")

        execute_single_step(TokenAuthConfigurationStep, yaml_source=test_file_path)

        tokens = TokenAuth.objects.order_by("created")

        self.assertEqual(tokens.count(), 3)

        first_token: TokenAuth = tokens[0]

        self.assertEqual(first_token.identifier, "token-1")
        self.assertEqual(first_token.contact_person, "Person 1")
        self.assertEqual(first_token.email, "person-1@example.com")
        self.assertEqual(first_token.organization, "Organization XYZ")
        self.assertEqual(first_token.application, "Application XYZ")
        self.assertEqual(first_token.administration, "Administration XYZ")

        second_token: TokenAuth = tokens[1]

        self.assertEqual(second_token.identifier, "token-2")
        self.assertEqual(second_token.contact_person, "Person 2")
        self.assertEqual(second_token.email, "person-2@example.com")
        self.assertEqual(second_token.organization, "")
        self.assertEqual(second_token.application, "")
        self.assertEqual(second_token.administration, "")

        third_token: TokenAuth = tokens[2]

        self.assertEqual(third_token.identifier, "token-3")
        self.assertEqual(third_token.contact_person, "Person 3")
        self.assertEqual(third_token.email, "person-3@example.com")
        self.assertEqual(third_token.organization, "Organization ZYX")
        self.assertEqual(third_token.application, "Application ZYX")
        self.assertEqual(third_token.administration, "Administration ZYX")

    def test_validation_errors(self):
        TokenAuthFactory(
            identifier="token-1",
            contact_person="Person 4",
            email="person-4@example.com",
        )

        test_file_path = str(TEST_FILES / "token_validation_errors.yaml")

        execute_single_step(
            TokenAuthConfigurationStep, yaml_source=test_file_path
        )

        tokens = TokenAuth.objects.order_by("created")

        self.assertEqual(tokens.count(), 2)

        first_token: TokenAuth = tokens[0]

        self.assertEqual(first_token.identifier, "token-1")
        self.assertEqual(first_token.contact_person, "Person 4")
        self.assertEqual(first_token.email, "person-4@example.com")
        self.assertEqual(first_token.organization, "")
        self.assertEqual(first_token.application, "")
        self.assertEqual(first_token.administration, "")

        second_token: TokenAuth = tokens[1]

        self.assertEqual(second_token.identifier, "token-2")
        self.assertEqual(second_token.contact_person, "Person 2")
        self.assertEqual(second_token.email, "person-2@example.com")
        self.assertEqual(second_token.organization, "Organization ZYX")
        self.assertEqual(second_token.application, "Application ZYX")
        self.assertEqual(second_token.administration, "Administration ZYX")

    def test_idempotent_step(self):
        test_file_path = str(TEST_FILES / "token_idempotent.yaml")

        execute_single_step(
            TokenAuthConfigurationStep, yaml_source=test_file_path
        )

        tokens = TokenAuth.objects.order_by("created")

        self.assertEqual(tokens.count(), 2)

        first_token: TokenAuth = tokens[0]

        self.assertEqual(first_token.identifier, "token-1")
        self.assertEqual(first_token.contact_person, "Person 1")
        self.assertEqual(first_token.email, "person-1@example.com")
        self.assertEqual(first_token.organization, "Organization XYZ")
        self.assertEqual(first_token.application, "Application XYZ")
        self.assertEqual(first_token.administration, "Administration XYZ")

        second_token: TokenAuth = tokens[1]

        self.assertEqual(second_token.identifier, "token-2")
        self.assertEqual(second_token.contact_person, "Person 2")
        self.assertEqual(second_token.email, "person-2@example.com")
        self.assertEqual(second_token.organization, "Organization ZYX")
        self.assertEqual(second_token.application, "Application ZYX")
        self.assertEqual(second_token.administration, "Administration ZYX")

        execute_single_step(
            TokenAuthConfigurationStep, yaml_source=test_file_path
        )

        self.assertEqual(TokenAuth.objects.count(), 2)

        first_token.refresh_from_db()

        self.assertEqual(first_token.identifier, "token-1")
        self.assertEqual(first_token.contact_person, "Person 1")
        self.assertEqual(first_token.email, "person-1@example.com")
        self.assertEqual(first_token.organization, "Organization XYZ")
        self.assertEqual(first_token.application, "Application XYZ")
        self.assertEqual(first_token.administration, "Administration XYZ")

        second_token.refresh_from_db()

        self.assertEqual(second_token.identifier, "token-2")
        self.assertEqual(second_token.contact_person, "Person 2")
        self.assertEqual(second_token.email, "person-2@example.com")
        self.assertEqual(second_token.organization, "Organization ZYX")
        self.assertEqual(second_token.application, "Application ZYX")
        self.assertEqual(second_token.administration, "Administration ZYX")