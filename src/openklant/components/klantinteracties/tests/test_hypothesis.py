import re

from django.core.exceptions import ValidationError

from hypothesis import assume, given, settings, strategies as st
from hypothesis.extra.django import TestCase

from openklant.components.klantinteracties.models import Klantcontact, Partij
from openklant.components.klantinteracties.utils import (
    NUMMER_LENGTH,
    REGEX_NUMMER,
    pad_nummer,
    validate_nummer,
)
from openklant.utils.validators import validate_regex_nummer

empty = st.sampled_from(["", None])
valid_nummers = st.text(alphabet="0123456789", min_size=1, max_size=NUMMER_LENGTH)
ascii_digits = st.text(alphabet="0123456789", max_size=NUMMER_LENGTH + 3)
signed_integers = st.integers().map(str) | st.integers().map(lambda i: f"{i:+d}")
any_script_digits = st.text(
    alphabet=st.characters(categories=["Nd"]), max_size=NUMMER_LENGTH + 3
)

nummers_input = (
    empty
    | valid_nummers
    | ascii_digits
    | signed_integers
    | any_script_digits
    | st.text()
)

nummer_settings = settings(deadline=None)


def only_ascii_digits(value) -> bool:
    return value is not None and re.fullmatch(r"[0-9]+", value) is not None


class NummerHypothesisTests(TestCase):
    @nummer_settings
    @given(value=nummers_input)
    def test_padding_is_idempotent(self, value):
        self.assertEqual(pad_nummer(pad_nummer(value)), pad_nummer(value))

    @nummer_settings
    @given(value=nummers_input)
    def test_padding_never_truncates(self, value):
        padded = pad_nummer(value)
        if value is not None:
            self.assertTrue(padded.endswith(value))

    @nummer_settings
    @given(value=nummers_input)
    def test_only_ascii_digits_are_valid(self, value):
        assume(value is not None)

        if only_ascii_digits(value) and len(value) <= NUMMER_LENGTH:
            validate_regex_nummer(value)
        else:
            with self.assertRaises(ValidationError):
                validate_regex_nummer(value)

    @nummer_settings
    @given(nummer=nummers_input)
    def test_clean_and_save(self, nummer):
        try:
            validate_regex_nummer(nummer)
        except ValidationError:
            return

        klantcontact = Klantcontact(vertrouwelijk=False, nummer=nummer)
        klantcontact.clean()
        klantcontact.save()
        klantcontact.refresh_from_db()

        self.assertRegex(klantcontact.nummer, REGEX_NUMMER)
        self.assertEqual(int(klantcontact.nummer), int(nummer))

    @nummer_settings
    @given(value=valid_nummers, extra_zeros=st.integers(0, NUMMER_LENGTH))
    def test_nummer_in_use_raises_in_any_format(self, value, extra_zeros):
        Klantcontact.objects.create(vertrouwelijk=False, nummer=value)

        stripped = value.lstrip("0") or "0"
        other_format = stripped.zfill(min(len(stripped) + extra_zeros, NUMMER_LENGTH))

        with self.assertRaises(ValidationError) as cm:
            validate_nummer(
                Klantcontact, other_format, Klantcontact(vertrouwelijk=False)
            )
        self.assertEqual(cm.exception.error_list[0].code, "unique")

    @nummer_settings
    @given(value=valid_nummers)
    def test_object_does_not_conflict_with_itself(self, value):
        klantcontact = Klantcontact.objects.create(vertrouwelijk=False, nummer=value)

        klantcontact.nummer = value
        klantcontact.save()
        self.assertEqual(
            validate_nummer(Klantcontact, value, klantcontact), pad_nummer(value)
        )

    @nummer_settings
    @given(value=valid_nummers)
    def test_same_nummer_in_other_model_is_valid(self, value):
        klantcontact = Klantcontact.objects.create(vertrouwelijk=False, nummer=value)
        partij = Partij(soort_partij="persoon", nummer=value)

        self.assertEqual(
            validate_nummer(Partij, value, partij),
            validate_nummer(Klantcontact, value, klantcontact),
        )

    @nummer_settings
    @given(value=valid_nummers)
    def test_stored_nummer_is_always_12_digits(self, value):
        with self.subTest("supplied nummer"):
            klantcontact = Klantcontact.objects.create(
                vertrouwelijk=False, nummer=value
            )
            klantcontact.refresh_from_db()
            self.assertEqual(klantcontact.nummer, pad_nummer(value))

        for empty_value in ("", None):
            with self.subTest(f"generated nummer ({empty_value!r})"):
                klantcontact = Klantcontact.objects.create(
                    vertrouwelijk=False, nummer=empty_value
                )
                klantcontact.refresh_from_db()
                self.assertRegex(klantcontact.nummer, REGEX_NUMMER)

    @nummer_settings
    @given(value=valid_nummers)
    def test_pad_nummer_gives_12_digits_with_same_value(self, value):
        padded = pad_nummer(value)

        self.assertRegex(padded, REGEX_NUMMER)
        self.assertEqual(int(padded), int(value))

    @nummer_settings
    @given(a=valid_nummers, b=valid_nummers)
    def test_pad_nummer_different_numbers_stay_different(self, a, b):
        assume(int(a) != int(b))

        self.assertNotEqual(pad_nummer(a), pad_nummer(b))

    @nummer_settings
    @given(value=empty)
    def test_pad_nummer_empty_is_unchanged(self, value):
        self.assertEqual(pad_nummer(value), value)
