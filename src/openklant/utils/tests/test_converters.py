from datetime import datetime, timezone

from django.test import TestCase

from ..converters import (
    camel_to_snake_converter,
    parse_datetime,
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


class ParseIsoDatetimeTests(TestCase):
    def test_valid_iso_datetime(self):
        value = "2025-11-28T15:30:00+00:00"
        expected = datetime(2025, 11, 28, 15, 30, 0, tzinfo=timezone.utc)

        result = parse_datetime(value)

        self.assertEqual(result, expected)

    def test_valid_iso_datetime_without_timezone(self):
        value = "2025-11-28T15:30:00"
        expected = datetime(2025, 11, 28, 15, 30, 0)

        result = parse_datetime(value)

        self.assertEqual(result, expected)

    def test_valid_iso_datetime_without_time(self):
        value = "2025-11-28"
        expected = datetime(2025, 11, 28, 0, 0, 0)

        result = parse_datetime(value)

        self.assertEqual(result, expected)

    def test_invalid_strings_return_none(self):
        invalid_inputs = [
            "invalid-date",
            "2025-13-01T00:00:00",  # invalid month
            "2025-00-10T12:00:00",  # month 0 is invalid
            "2025-11-31T12:00:00",  # invalid day for November
            "2025-11-28T25:00:00",  # invalid hour
            "2025-11-28T12:60:00",  # invalid minutes
            "2025-11-28T12:00:60",  # invalid seconds
            "2025/11/28 12:00:00",  # wrong format
            "28-11-2025T12:00:00",  # day-month-year format
            "T12:00:00",  # time only, no date
        ]
        for invalid in invalid_inputs:
            with self.subTest(invalid=invalid):
                self.assertEqual(parse_datetime(invalid), None)
