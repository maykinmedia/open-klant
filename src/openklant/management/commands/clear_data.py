from django.core.management.base import BaseCommand

from openklant.components.klanten.models.klanten import (
    Klant,
    NatuurlijkPersoon,
    NietNatuurlijkPersoon,
    Vestiging,
)


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        NatuurlijkPersoon.objects.all().delete()
        NietNatuurlijkPersoon.objects.all().delete()
        Vestiging.objects.all().delete()
        Klant.objects.all().delete()
