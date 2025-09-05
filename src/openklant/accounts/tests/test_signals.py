from django.apps import apps
from django.test import TestCase

from django_admin_index.models import AppGroup

from openklant.accounts.signals import update_admin_index


class UpdateAdminIndexSignalTests(TestCase):
    def test_update_admin_index_loads_fixture(self):
        AppGroup.objects.all().delete()
        self.assertEqual(AppGroup.objects.count(), 0)

        update_admin_index(sender=apps.get_app_config("openklant"))

        self.assertGreater(
            AppGroup.objects.count(),
            0,
            "Expected default_admin_index.json to load AppGroups",
        )
