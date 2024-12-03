from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from openklant.components.token.validators import validate_non_empty_chars


class WhiteSpaceValidatorTestCase(SimpleTestCase):
    def test_characters_only(self):
        self.assertIsNone(validate_non_empty_chars("test123"))

    def test_trailing_whitespace(self):
        self.assertIsNone(validate_non_empty_chars("test123  "))

    def test_leading_whitespace(self):
        self.assertIsNone(validate_non_empty_chars("  test123"))

    def test_whitespace_in_between(self):
        self.assertIsNone(validate_non_empty_chars("test  123"))

    def test_whitespace_only(self):
        with self.assertRaises(ValidationError):
            validate_non_empty_chars("  ")

    def test_trailing_tab_character(self):
        self.assertIsNone(validate_non_empty_chars("test123\t"))

    def test_leading_tab_character(self):
        self.assertIsNone(validate_non_empty_chars("\ttest123"))

    def test_tab_character_in_between(self):
        self.assertIsNone(validate_non_empty_chars("test\t123"))

    def test_tab_characters_only(self):
        with self.assertRaises(ValidationError):
            validate_non_empty_chars("\t\t")

    def test_blank_value(self):
        with self.assertRaises(ValidationError):
            validate_non_empty_chars("")
