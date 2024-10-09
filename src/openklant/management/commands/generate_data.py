from django.core.management.base import BaseCommand

from openklant.components.klanten.models.tests.factories import (
    NatuurlijkPersoonFactory,
    NietNatuurlijkPersoonFactory,
    VestigingFactory,
)


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        VestigingFactory.create_batch(size=30)
        NietNatuurlijkPersoonFactory.create_batch(size=30)
        NatuurlijkPersoonFactory.create_batch(size=30)
