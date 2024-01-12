from django.apps import AppConfig


class KlantenConfig(AppConfig):
    name = "openklant.components.legacy.klanten"

    def ready(self):
        from openklant.components.legacy import extensions  # noqa
