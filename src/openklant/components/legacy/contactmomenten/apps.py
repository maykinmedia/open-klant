from django.apps import AppConfig


class ContactmomentenConfig(AppConfig):
    name = "openklant.components.legacy.contactmomenten"

    def ready(self):
        from openklant.components.legacy import extensions  # noqa
