from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django.test import override_settings

from upgrade_check import UpgradeCheck, VersionRange
from upgrade_check.constraints import UpgradePaths
from upgrade_check.models import Version

from openklant.tests.test_migrate import BaseMigrationTest

UPGRADE_CHECK_PATHS: UpgradePaths = {
    "2.6.0": UpgradeCheck(VersionRange(minimum="2.5.0")),
}


class TestUpgradeCheck(BaseMigrationTest):
    app = "token"
    migrate_from = "0001_initial"
    migrate_to = "0002_identifier_migration"

    def setUp(self):
        super().setUp()
        self._flush_versions()

    def _flush_versions(self):
        Version.objects.all().delete()

    @override_settings(UPGRADE_CHECK_PATHS=UPGRADE_CHECK_PATHS, RELEASE="2.0.0")
    def test_upgrade_check_lower_version(self):
        TokenAuth = self.old_app_state.get_model("token", "TokenAuth")
        self.assertFalse(hasattr(TokenAuth, "identifier"))

        call_command("upgrade_check_version")
        call_command("check")

        self.assertFalse(hasattr(TokenAuth, "identifier"))

    @override_settings(UPGRADE_CHECK_PATHS=UPGRADE_CHECK_PATHS, RELEASE="2.6.0")
    def test_upgrade_check_higher_version_ok(self):
        TokenAuth = self.old_app_state.get_model("token", "TokenAuth")
        self.assertFalse(hasattr(TokenAuth, "identifier"))

        self._perform_migration()

        TokenAuth = self.apps.get_model("token", "TokenAuth")
        self.assertTrue(hasattr(TokenAuth, "identifier"))

        call_command("upgrade_check_version")
        call_command("check")

    @override_settings(UPGRADE_CHECK_PATHS=UPGRADE_CHECK_PATHS, RELEASE="2.6.0")
    def test_upgrade_check_higher_version_denied(self):
        TokenAuth = self.old_app_state.get_model("token", "TokenAuth")
        self.assertFalse(hasattr(TokenAuth, "identifier"))

        with self.assertRaises(SystemCheckError) as error:
            call_command("upgrade_check_version")
            call_command("check")
        self.assertTrue(
            "Upgrading from 2.4.0 to 2.6.0 is not possible" in str(error.exception)
        )
        self.assertFalse(hasattr(TokenAuth, "identifier"))
