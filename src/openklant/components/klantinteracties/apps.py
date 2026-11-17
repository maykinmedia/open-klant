from django.apps import AppConfig


class KlantinteractiesConfig(AppConfig):
    name = "openklant.components.klantinteracties"

    def ready(self) -> None:
        from . import metrics  # noqa
