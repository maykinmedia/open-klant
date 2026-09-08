from django.contrib import admin
from django.test import TestCase

from openklant.components.klantinteracties.models.klantcontacten import (
    Betrokkene,
    Klantcontact,
)
from openklant.components.klantinteracties.models.partijen import Persoon

from ..checks import _check_model_admin, _flatten, check_admin_relation_fields


class RawIdFieldsCheckTests(TestCase):
    def test_flags_foreign_key_without_raw_id_or_autocomplete_fields(self):
        class BareBetrokkeneAdmin(admin.ModelAdmin):
            fields = ("partij", "klantcontact")

        model_admin = BareBetrokkeneAdmin(Betrokkene, admin.site)

        flagged = {error.obj for error in _check_model_admin(Betrokkene, model_admin)}

        self.assertIn("klantinteracties.Betrokkene.partij", flagged)
        self.assertIn("klantinteracties.Betrokkene.klantcontact", flagged)

    def test_raw_id_fields_silences_the_warning(self):
        class RawIdBetrokkeneAdmin(admin.ModelAdmin):
            fields = ("partij", "klantcontact")
            raw_id_fields = ("partij", "klantcontact")

        model_admin = RawIdBetrokkeneAdmin(Betrokkene, admin.site)

        self.assertEqual(_check_model_admin(Betrokkene, model_admin), [])

    def test_autocomplete_fields_silences_the_warning(self):
        class AutocompleteBetrokkeneAdmin(admin.ModelAdmin):
            fields = ("partij", "klantcontact")
            autocomplete_fields = ("partij", "klantcontact")

        model_admin = AutocompleteBetrokkeneAdmin(Betrokkene, admin.site)

        self.assertEqual(_check_model_admin(Betrokkene, model_admin), [])

    def test_field_not_shown_in_admin_is_not_flagged(self):
        class PartialBetrokkeneAdmin(admin.ModelAdmin):
            fields = ("partij",)

        model_admin = PartialBetrokkeneAdmin(Betrokkene, admin.site)

        flagged = {error.obj for error in _check_model_admin(Betrokkene, model_admin)}

        self.assertIn("klantinteracties.Betrokkene.partij", flagged)
        self.assertNotIn("klantinteracties.Betrokkene.klantcontact", flagged)

    def test_excluded_field_is_not_flagged(self):
        class ExcludedBetrokkeneAdmin(admin.ModelAdmin):
            exclude = ("klantcontact",)

        model_admin = ExcludedBetrokkeneAdmin(Betrokkene, admin.site)

        flagged = {error.obj for error in _check_model_admin(Betrokkene, model_admin)}

        self.assertNotIn("klantinteracties.Betrokkene.klantcontact", flagged)

    def test_inline_non_parent_foreign_key_is_flagged(self):
        class BetrokkeneInline(admin.StackedInline):
            model = Betrokkene
            fields = ("partij", "klantcontact")

        class KlantcontactAdminWithInline(admin.ModelAdmin):
            inlines = [BetrokkeneInline]

        model_admin = KlantcontactAdminWithInline(Klantcontact, admin.site)

        flagged = {error.obj for error in _check_model_admin(Klantcontact, model_admin)}

        self.assertIn("klantinteracties.Betrokkene.partij", flagged)
        self.assertNotIn("klantinteracties.Betrokkene.klantcontact", flagged)

    def test_one_to_one_field_is_never_flagged(self):
        class BarePersoonAdmin(admin.ModelAdmin):
            fields = ("partij",)

        model_admin = BarePersoonAdmin(Persoon, admin.site)

        self.assertEqual(_check_model_admin(Persoon, model_admin), [])

    def test_registered_admin_site_has_no_unaddressed_warnings(self):
        errors = check_admin_relation_fields(app_configs=None)

        self.assertEqual(errors, [])

    def test_readonly_field_is_not_flagged(self):
        class ReadonlyBetrokkeneAdmin(admin.ModelAdmin):
            fields = ("partij", "klantcontact")
            readonly_fields = ("klantcontact",)

        model_admin = ReadonlyBetrokkeneAdmin(Betrokkene, admin.site)

        flagged = {error.obj for error in _check_model_admin(Betrokkene, model_admin)}

        self.assertNotIn("klantinteracties.Betrokkene.klantcontact", flagged)

    def test_check_can_be_scoped_to_app_configs(self):
        app_config = Betrokkene._meta.app_config

        errors = check_admin_relation_fields(app_configs=[app_config])

        self.assertEqual(errors, [])

    def test_flatten_handles_nested_lists_and_tuples(self):
        self.assertEqual(
            _flatten(("partij", ("klantcontact", "foo"), ["bar"])),
            ["partij", "klantcontact", "foo", "bar"],
        )
