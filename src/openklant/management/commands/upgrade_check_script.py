from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection
from upgrade_check.recorder import get_version_info
from django.conf import settings

from openklant.components.token.models import TokenAuth


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        self._migrate_upgrade_check()
        self._can_upgrade()

    def _migrate_upgrade_check(self):
        # migrate first the upgrade_check to save the current version on
        call_command("migrate", "upgrade_check")

    def _model_has_attr(self, table_name, column_name):
        pass

    def _can_upgrade(self):
        current_version = get_version_info()
        breakpoint()
        self._model_has_attr(TokenAuth, "identifier")
