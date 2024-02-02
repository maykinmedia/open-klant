from django.test import TestCase

from ..converters import camel_to_snake_converter, snake_to_camel_converter


class ConverterTests(TestCase):
    def test_camel_to_snake_converter(self):
        self.assertEqual(
            camel_to_snake_converter("snakeCaseTestString"), "snake_case_test_string"
        )

    def test_snake_to_camel_converter(self):
        self.assertEqual(
            snake_to_camel_converter("camel_case_test_string"), "camelCaseTestString"
        )
