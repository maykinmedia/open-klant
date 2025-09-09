from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    name = "openklant.accounts"

    def ready(self):
        from . import metrics  # noqa
        from . import signals  # noqa

        post_migrate.connect(signals.update_admin_index, sender=self)
