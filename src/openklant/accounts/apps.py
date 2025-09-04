from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "openklant.accounts"

    def ready(self):
        from . import metrics  # noqa
        from . import signals  # noqa
