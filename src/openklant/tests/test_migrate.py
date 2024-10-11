import os

from io import StringIO
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import LiveServerTestCase

import vcr
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.constants import SoortPartij
from openklant.components.klantinteracties.models.partijen import Partij, Persoon, Organisatie

CASSETTE_DIR = Path(__file__).resolve().parent / "fixtures" / "migrate_command" / "cassettes"


class MigrateTestCase(LiveServerTestCase):
    host = "localhost"
    port = 8005

    def setUp(self):
        super().setUp()

        os.environ["ACCESS_TOKEN"] = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJpc3MiOiJ0ZXN0c3VpdGUiLCJpYXQiOjE3Mjg2MzU1NDUsImNsaWVudF9pZCI6I"
            "nRlc3RzdWl0ZSIsInVzZXJfaWQiOiJ0ZXN0X3VzZXJfaWQiLCJ1c2VyX3JlcHJlc2V"
            "udGF0aW9uIjoiVGVzdCBVc2VyIn0.puffLXIskm2mfih0knOPKnMh89bpoiHJ539hPfywZto"
        )

    def _get_partij_url(self, partij) -> str:
        return reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

    @vcr.use_cassette(
        str(CASSETTE_DIR / "single_run.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_single_run(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
        )

        partij = Partij.objects.get()

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    @vcr.use_cassette(
        str(CASSETTE_DIR / "pagination.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_pagination(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
        )

        partijen = Partij.objects.all()

        self.assertEqual(partijen.count(), 200)

        output = stdout.getvalue().splitlines()

        expected_urls = [
            f"{self.live_server_url}{self._get_partij_url(partij)}"
            for partij in partijen
        ]

        self.assertCountEqual(output, expected_urls)

    @vcr.use_cassette(
        str(CASSETTE_DIR / "natuurlijk_persoon.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_natuurlijk_persoon(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
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

    @vcr.use_cassette(
        str(CASSETTE_DIR / "niet_natuurlijk_persoon.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_niet_natuurlijk_persoon(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
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

    @vcr.use_cassette(
        str(CASSETTE_DIR / "vestiging.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_vestiging(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
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

    @vcr.use_cassette(
        str(CASSETTE_DIR / "no_subject_and_subject_identificatie.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_no_subject_and_subject_identificatie(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
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

    @vcr.use_cassette(
        str(CASSETTE_DIR / "subject_and_no_subject_identificatie.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_subject_and_no_subject_identificatie(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
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

    @vcr.use_cassette(
        str(CASSETTE_DIR / "no_subject_and_no_subject_identificatie.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_no_subject_and_no_subject_identificatie(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    @vcr.use_cassette(
        str(CASSETTE_DIR / "incorrect_subject_identificatie.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_incorrect_subject_identificatie(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    @vcr.use_cassette(
        str(CASSETTE_DIR / "incorrect_subject_url.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_incorrect_subject_url(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    @vcr.use_cassette(
        str(CASSETTE_DIR / "subject_404.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_subject_404(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    @vcr.use_cassette(
        str(CASSETTE_DIR / "digitaal_adres.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_digitaal_adres(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
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
                "http://127.0.0.1:8001",
                self.live_server_url,
                stdout=stdout
            )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    @vcr.use_cassette(
        str(CASSETTE_DIR / "no_subject_type.yaml"),
        ignore_hosts=["localhost"],
        filter_headers=["authorization"]
    )
    def test_no_subject_type(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://127.0.0.1:8001",
            self.live_server_url,
            stdout=stdout
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        self.assertEqual(output, [])

    def test_invalid_urls(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "foobar.com",
            self.live_server_url,
            stdout=stdout
        )

        self.assertEqual(Partij.objects.count(), 0)

        output = stdout.getvalue().splitlines()

        message = next(iter(output))

        self.assertIn("Invalid URL(s)", message)
