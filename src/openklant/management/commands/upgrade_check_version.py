from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from upgrade_check.models import Version, get_machine_name

PRE_REQUIRED_RELEASE = "2.4.0"
PRE_REQUIRED_GIT_SHA = "83f9aec4752026bf3ac077865f8efc7646386697"


class Command(BaseCommand):
    help = """

    python src/manage.py upgrade_check_version

    Ensures that any system upgrade must go through version 2.5.0, which includes a critical migration.

    On the first upgrade, the command records in the DjangoUpgradeCheck table the version immediately
    preceding the minimum required version. This allows the 'django-upgrade-check' library to later verify
    that all mandatory intermediate versions have been correctly applied.
    """

    def handle(self, *args, **options):
        self._detect_current_verion()

    def _table_has_column(self, table_name, column_name):
        if table_name in connection.introspection.table_names():
            with connection.cursor() as cursor:
                columns = [
                    col.name
                    for col in connection.introspection.get_table_description(
                        cursor, table_name
                    )
                ]
            return column_name in columns
        return True

    def _detect_current_verion(self):
        if not self._table_has_column("token_tokenauth", "identifier"):
            # As the starting version is unknown, we determine it based on the existence
            # of the field added in the minimal version.

            # Migrate `upgrade_check` to save the previous version to the one required
            call_command("migrate", "upgrade_check")
            Version.objects.get_or_create(
                version=PRE_REQUIRED_RELEASE,
                git_sha=PRE_REQUIRED_GIT_SHA,
                machine_name=get_machine_name(),
            )
