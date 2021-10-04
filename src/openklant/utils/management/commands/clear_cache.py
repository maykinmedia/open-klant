from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.core.management import BaseCommand
from django.utils.translation import gettext as _


class Command(BaseCommand):
    help = "Clears the Django cache"

    def add_arguments(self, parser):
        parser.add_argument("--alias", help=_("Clear given cache only"))

    def handle(self, *args, **options):
        alias = options["alias"]
        cache = caches[alias] if alias else caches[DEFAULT_CACHE_ALIAS]

        cache.clear()
