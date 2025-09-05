from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    name = "openklant.accounts"

    def ready(self):
        from .signals import update_admin_index

        post_migrate.connect(update_admin_index, sender=self)
