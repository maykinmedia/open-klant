from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "openklant.utils"

    def ready(self):
        from . import checks  # noqa
