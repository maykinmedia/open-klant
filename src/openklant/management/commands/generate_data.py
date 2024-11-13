from django.core.management.base import BaseCommand

from openklant.components.klanten.models.constants import KlantType
from openklant.components.klanten.models.tests.factories import (
    KlantFactory,
    NatuurlijkPersoonFactory,
    NietNatuurlijkPersoonFactory,
    VestigingFactory,
)


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        # NatuurlijkPersoonFactory(
        #     klant__voornaam="Harry",
        #     klant__achternaam="Potter",
        #     klant__voorvoegsel_achternaam="",
        #     klant__subject_type=KlantType.natuurlijk_persoon,
        #     inp_bsn="024325818",
        #     voorletters="H",
        # )

        # NatuurlijkPersoonFactory.create_batch(
        #     klant__subject_type=KlantType.natuurlijk_persoon,
        #     size=200,
        # )

        # NietNatuurlijkPersoonFactory(
        #     klant__subject_type=KlantType.niet_natuurlijk_persoon,
        #     inn_nnp_id="807371440",
        #     statutaire_naam="Foobar Inc."
        # )

        # VestigingFactory(
        #     klant__subject_type=KlantType.vestiging,
        #     klant__bedrijfsnaam="Foobar Inc."
        #     vestigings_nummer="123456789",
        # )

        # KlantFactory(
        #     subject="http://example.com/subject/1",
        #     subject_type=None,
        # )

        # KlantFactory(subject_type=None, subject="")

        # KlantFactory(subject_type=None, subject="foobar")

        # KlantFactory(subject_type=None, subject="http://unknown-url.com")
