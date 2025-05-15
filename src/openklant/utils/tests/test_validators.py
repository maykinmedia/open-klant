from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from openklant.utils.validators import (
    validate_bag_id,
    validate_charfield_entry,
    validate_country,
    validate_iban,
    validate_no_space,
    validate_phone_number,
    validate_postal_code,
)


class ValidatorsTestCase(SimpleTestCase):
    """
    Validates the functions defined in ``utils.validators`` module.
    """

    def test_validate_charfield_entry_apostrophe_not_allowed(self):
        """
        Tests the ``validate_charfield_entry`` function when not explicitly
        allowing apostrophe character.
        """
        self.assertRaisesMessage(
            ValidationError,
            "Uw invoer bevat een ongeldig teken: '",
            validate_charfield_entry,
            "let's fail",
        )

    def test_validate_charfield_entry_apostrophe_allowed(self):
        """
        Tests the ``validate_charfield_entry`` function when explicitly
        allowing apostrophe character.
        """
        self.assertEqual(
            validate_charfield_entry("let's pass", allow_apostrophe=True), "let's pass"
        )

    def test_validate_postal_code(self):
        """
        Test all valid postal code and also test invalid values
        """
        invalid_postal_codes = [
            "0000AA",
            "0999AA",
            "1000  AA",
            "1000 AAA",
            "1000AAA",
            "0000aa",
            "0000 aa",
            "0999aa",
            "1000  aa",
            "1000 aaa",
            "1000aaa",
            "1111,aa",
            "1111,a",
            '1111"a',
            '1111"aa',
            "1111 Aa",
            "1111 aA",
            "1015CJ",
        ]
        for invalid_postal_code in invalid_postal_codes:
            self.assertRaisesMessage(
                ValidationError,
                "Postcode moet aan het volgende formaat voldoen: `1234 AB` (met spatie)",
                validate_postal_code,
                invalid_postal_code,
            )
        self.assertIsNone(validate_postal_code("1015 CJ"))

    def test_validate_phone_number(self):
        valid_phone_numbers = [
            "+31612345678",
            "+441134960000",  # US test number
            "+12065550100",  # US test number
            "0612345678",
            "0031612345678",
            "09001234567",
            "080085285212",
            "1400",
            "14012",
            "14079",
            "0313028612",
            "0313028600",
        ]
        invalid_phone_numbers = [
            "0695azerty",
            "azerty0545",
            "@4566544++8",
            "onetwothreefour",
            "020 753 0523",
            "+311234",
            "031302860000",
            "03130286000",
            "00311234567",
            "00313223344555",
            "316123456789",
        ]
        for invalid_phone_number in invalid_phone_numbers:
            with self.subTest(invalid_phone_number):
                self.assertRaisesMessage(
                    ValidationError,
                    "Het opgegeven telefoonnummer is ongeldig.",
                    validate_phone_number,
                    invalid_phone_number,
                )

        for valid_phone_number in valid_phone_numbers:
            with self.subTest(valid_phone_number):
                validate_phone_number(valid_phone_number)

    def test_validate_no_space_validator(self):
        invalid_strings = [
            "aaaa aaaa",
            " bbbbbbbb",
            "cccccccc ",
            "d d d d d",
        ]

        for invalid_string in invalid_strings:
            self.assertRaisesMessage(
                ValidationError,
                "Geen spaties toegestaan",
                validate_no_space,
                invalid_string,
            )

        self.assertIsNone(validate_no_space("nospaces"))

    def test_validate_iban(self):
        invalid_ibans = [
            "1231md4832842834",
            "jda42034nnndnd23923",
            "AB123dasd#asdasda",
            "AB12",
            "AB1259345934953495934953495345345345",
        ]

        for invalid_iban in invalid_ibans:
            self.assertRaisesMessage(
                ValidationError,
                "Ongeldige IBAN",
                validate_iban,
                invalid_iban,
            )

        self.assertIsNone(validate_iban("AB12TEST1253678"))
        self.assertIsNone(validate_iban("AB12test1253678"))
        self.assertIsNone(validate_iban("ab1299999999999"))
        self.assertIsNone(validate_iban("ab129"))
        self.assertIsNone(validate_iban("ab12aaaaaaaaaa"))

    def test_validate_bag_id(self):
        """
        Test Basisregistratie Adressen en Gebouwen ID
        """
        invalid_ids = [
            "",
            "1",
            "1000 AAA",
            "1000AAA",
            "000000000000000",
            "AAAAAAAAAAAAAAAA",
            "1234-1234-1234-1234",
            "123A123A123A123A",
        ]
        for bag_id in invalid_ids:
            self.assertRaisesMessage(
                ValidationError,
                "Ongeldige nummeraanduiding BAG-ID",
                validate_bag_id,
                bag_id,
            )

        validate_bag_id("1234567890000001")
        validate_bag_id("1111111111111111")

    def test_validate_country(self):
        invalid_codes = [
            "",
            "1",
            "10",
            "ZZ",
            "1Z",
            "nl",
        ]
        for code in invalid_codes:
            self.assertRaisesMessage(
                ValidationError,
                "Ongeldige landcode, de code moet behoren tot de ISO 3166-standaard",
                validate_country,
                code,
            )

        validate_country("NL")
