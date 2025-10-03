from django.apps import AppConfig


class KlantinteractiesConfig(AppConfig):
    name = "openklant.components.klantinteracties"

    def ready(self):
        from . import metrics  # noqa
