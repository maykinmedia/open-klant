from django.test import TestCase

from ..converters import (
    camel_to_snake_converter,
    nl_code_to_iso_code_country_converter,
    snake_to_camel_converter,
)


class ConverterTests(TestCase):
    def test_camel_to_snake_converter(self):
        self.assertEqual(
            camel_to_snake_converter("snakeCaseTestString"), "snake_case_test_string"
        )

    def test_snake_to_camel_converter(self):
        self.assertEqual(
            snake_to_camel_converter("camel_case_test_string"), "camelCaseTestString"
        )

    def test_nl_code_to_iso_code_country_converter(self):
        self.assertEqual(nl_code_to_iso_code_country_converter(""), "")
        self.assertEqual(nl_code_to_iso_code_country_converter("1"), "")
        self.assertEqual(nl_code_to_iso_code_country_converter("A"), "")
        self.assertEqual(nl_code_to_iso_code_country_converter("AA"), "")
        self.assertEqual(nl_code_to_iso_code_country_converter("1111"), "")

        # valid
        self.assertEqual(nl_code_to_iso_code_country_converter("6030"), "NL")
