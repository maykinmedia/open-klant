import os
from io import StringIO
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import LiveServerTestCase

from vcr.config import RecordMode
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.partijen import (
    Organisatie,
    Partij,
    Persoon,
)
from openklant.tests.vcr import VCRMixin


class MigrateTestCase(VCRMixin, LiveServerTestCase):
    host = "localhost"
    port = 8005

    def _get_cassette_library_dir(self) -> str:
        parent_dir = Path(__file__).resolve().parent
        return str(parent_dir / "cassettes" / "migration")

    def _get_cassette_name(self) -> str:
        """Return the filename for cassette

        Default VCR behaviour puts class name in the cassettename
        we put them in a directory.
        """
        _, test_name = self._testMethodName.split("test_")
        return f"{test_name}.yaml"

    def _get_vcr_kwargs(self, **kwargs) -> dict:
        kwargs = super()._get_vcr_kwargs(**kwargs)
        return {
            **kwargs,
            "record_mode": RecordMode.ONCE,
            # Decompress for human readable cassette diffs when re-recoding
            "decode_compressed_response": True,
            "filter_headers": ["authorization"],
            "ignore_hosts": ["localhost"],
        }

    def _get_partij_url(self, partij) -> str:
        return reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

    def setUp(self) -> None:
        super().setUp()

        os.environ["ACCESS_TOKEN"] = "secret"

    def test_single_run(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partij = Partij.objects.get()

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    def test_pagination(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partijen = Partij.objects.all()

        self.assertEqual(partijen.count(), 200)

        output = stdout.getvalue().splitlines()

        expected_urls = [
            f"{self.live_server_url}{self._get_partij_url(partij)}"
            for partij in partijen
        ]

        self.assertCountEqual(output, expected_urls)

    def test_natuurlijk_persoon(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partij = Partij.objects.get()
        persoon = Persoon.objects.get()

        self.assertEqual(partij, persoon.partij)

        self.assertEqual(partij.soort_partij, SoortPartij.persoon)
        self.assertEqual(partij.nummer, "024325818")
        self.assertIsNone(partij.voorkeurs_digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)

        self.assertEqual(persoon.contactnaam_voorletters, "H")
        self.assertEqual(persoon.contactnaam_voornaam, "Harry")
        self.assertEqual(persoon.contactnaam_voorvoegsel_achternaam, "")
        self.assertEqual(persoon.contactnaam_achternaam, "Potter")

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    def test_niet_natuurlijk_persoon(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partij = Partij.objects.get()
        organisatie = Organisatie.objects.get()

        self.assertEqual(partij, organisatie.partij)

        self.assertEqual(partij.soort_partij, SoortPartij.organisatie)
        self.assertEqual(partij.nummer, "807371440")
        self.assertIsNone(partij.voorkeurs_digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)

        self.assertEqual(organisatie.naam, "Foobar Inc.")

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    def test_vestiging(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partij = Partij.objects.get()
        organisatie = Organisatie.objects.get()

        self.assertEqual(partij, organisatie.partij)

        self.assertEqual(partij.soort_partij, SoortPartij.organisatie)
        self.assertEqual(partij.nummer, "123456789")
        self.assertIsNone(partij.voorkeurs_digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)

        self.assertEqual(organisatie.naam, "Foobar Inc.")

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    def test_no_subject_and_subject_identificatie(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partij = Partij.objects.get()
        persoon = Persoon.objects.get()

        self.assertEqual(partij, persoon.partij)

        self.assertEqual(partij.soort_partij, SoortPartij.persoon)
        self.assertEqual(partij.nummer, "024325818")
        self.assertIsNone(partij.voorkeurs_digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)

        self.assertEqual(persoon.contactnaam_voorletters, "H")
        self.assertEqual(persoon.contactnaam_voornaam, "Harry")
        self.assertEqual(persoon.contactnaam_voorvoegsel_achternaam, "")
        self.assertEqual(persoon.contactnaam_achternaam, "Potter")

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    def test_subject_and_no_subject_identificatie(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partij = Partij.objects.get()
        persoon = Persoon.objects.get()

        self.assertEqual(partij, persoon.partij)

        self.assertEqual(partij.soort_partij, SoortPartij.persoon)
        self.assertEqual(partij.nummer, "024325818")
        self.assertIsNone(partij.voorkeurs_digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)

        self.assertEqual(persoon.contactnaam_voorletters, "H")
        self.assertEqual(persoon.contactnaam_voornaam, "Anthony")
        self.assertEqual(persoon.contactnaam_voorvoegsel_achternaam, "")
        self.assertEqual(persoon.contactnaam_achternaam, "Hopkins")

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    def test_no_subject_and_no_subject_identificatie(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    def test_incorrect_subject_url(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    def test_subject_404(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    def test_digitaal_adres(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partij = Partij.objects.get()
        persoon = Persoon.objects.get()
        digitaal_adres = DigitaalAdres.objects.get()

        self.assertEqual(partij, persoon.partij)

        self.assertEqual(partij.soort_partij, SoortPartij.persoon)
        self.assertEqual(partij.nummer, "0000000001")  # auto generated
        self.assertEqual(partij.voorkeurs_digitaal_adres, digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)

        self.assertEqual(digitaal_adres.partij, partij)
        self.assertIsNone(digitaal_adres.betrokkene)
        self.assertEqual(digitaal_adres.soort_digitaal_adres, "email")
        self.assertEqual(digitaal_adres.adres, "example@example.com")
        self.assertEqual(digitaal_adres.omschrijving, "Emailadres")

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    def test_no_access_token(self):
        stdout = StringIO()

        del os.environ["ACCESS_TOKEN"]

        with self.assertRaises(ImproperlyConfigured):
            call_command(
                "migrate_to_v2",
                "http://localhost:8000",
                self.live_server_url,
                stdout=stdout,
            )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    def test_invalid_urls(self):
        stdout = StringIO()

        call_command("migrate_to_v2", "foobar.com", self.live_server_url, stdout=stdout)

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        message = next(iter(output))

        self.assertIn("Invalid URL(s)", message)
