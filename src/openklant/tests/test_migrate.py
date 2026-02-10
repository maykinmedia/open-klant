import os
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import CommandError, call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.state import StateApps
from django.test import LiveServerTestCase, TransactionTestCase

from maykin_common.vcr import VCRMixin
from requests import Request
from vcr.config import RecordMode
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models.constants import (
    PartijIdentificatorCodeObjectType,
    PartijIdentificatorCodeRegister,
    PartijIdentificatorCodeSoortObjectId,
    SoortPartij,
)
from openklant.components.klantinteracties.models.digitaal_adres import DigitaalAdres
from openklant.components.klantinteracties.models.partijen import (
    Organisatie,
    Partij,
    Persoon,
)
from openklant.components.klantinteracties.models.tests.factories import (
    DigitaalAdresFactory,
    PartijFactory,
)
from openklant.components.token.models import TokenAuth
from openklant.migration.utils import generate_jwt_token

LIVE_SERVER_HOST = "localhost"
LIVE_SERVER_PORT = 8005


def vcr_request_filter(request: Request):
    if f"{LIVE_SERVER_HOST}:{LIVE_SERVER_PORT}" in request.url:
        return

    return request


class BaseMigrationTest(TransactionTestCase):
    app: str
    migrate_from: str  # The migration before the one we want to test
    migrate_to: str  # The migration we want to test

    setting_overrides: dict = {}

    old_app_state: StateApps
    app_state: StateApps

    def setUp(self) -> None:
        """
        Setup the migration test by reversing to `migrate_from` state,
        then applying the `migrate_to` state.
        """
        assert self.app is not None, "You must define the `app` attribute"
        assert self.migrate_from is not None, "You must define `migrate_from`"
        assert self.migrate_to is not None, "You must define `migrate_to`"

        # Step 1: Set up the MigrationExecutor
        executor = MigrationExecutor(connection)

        # Step 2: Reverse to the starting migration state
        migrate_from = [(self.app, self.migrate_from)]
        old_migrate_state = executor.migrate(migrate_from)

        self.old_app_state = old_migrate_state.apps

    def _perform_migration(self) -> None:
        migrate_to = [(self.app, self.migrate_to)]

        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload the graph in case of dependency changes
        executor.migrate(migrate_to)

        self.apps = executor.loader.project_state(migrate_to).apps

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        # reset to latest migration
        call_command("migrate", verbosity=0, database=connection._alias)


class MigrateTestCase(VCRMixin, LiveServerTestCase):
    host = LIVE_SERVER_HOST
    port = LIVE_SERVER_PORT

    def _get_cassette_library_dir(self) -> str:
        base_dir = Path(settings.BASE_DIR)
        return str(base_dir / "migration" / "cassettes")

    def _get_cassette_name(self) -> str:
        """Return the filename for cassette

        Default VCR behaviour puts class name in the cassettename
        we put them in a directory.
        """
        return f"{self._testMethodName}.yaml"

    def _get_vcr_kwargs(self, **kwargs) -> dict:
        kwargs = super()._get_vcr_kwargs(**kwargs)
        return {
            **kwargs,
            "record_mode": RecordMode.ONCE,
            # Decompress for human readable cassette diffs when re-recoding
            "decode_compressed_response": True,
            "filter_headers": ["authorization"],
            # Use `before_record_request` as `ignore_hosts` does not take port
            # numbers into account
            "before_record_request": vcr_request_filter,
        }

    def _get_partij_url(self, partij) -> str:
        return reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

    def setUp(self) -> None:
        super().setUp()

        default_token = generate_jwt_token("migration", "foobar")
        os.environ.setdefault("ACCESS_TOKEN", default_token)

    def test_single_run(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        partij = Partij.objects.get()

        self.assertEqual(partij.nummer, "024325818")

        partij_identificator = partij.partijidentificator_set.get()

        self.assertEqual(
            partij_identificator.partij_identificator_code_objecttype,
            PartijIdentificatorCodeObjectType.natuurlijk_persoon,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_code_register,
            PartijIdentificatorCodeRegister.brp,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_code_soort_object_id,
            PartijIdentificatorCodeSoortObjectId.bsn,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_object_id, "024325818"
        )

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )
        expected_output = f"{self.live_server_url}{partij_url}"
        output = stdout.getvalue().splitlines()
        self.assertEqual(output, [expected_output])

    @patch.dict(os.environ, {"CLIENT_ID": "migration", "SECRET": "foobar"}, clear=True)
    def test_single_run_with_client_id_and_secret(self):
        stdout = StringIO()

        with patch(
            "openklant.management.commands.migrate_to_v2.generate_jwt_token",
            wraps=generate_jwt_token,
        ) as mock_generate:
            call_command(
                "migrate_to_v2",
                "http://localhost:8000",
                self.live_server_url,
                stdout=stdout,
            )

            mock_generate.assert_called_once_with("migration", "foobar")

        partij = Partij.objects.get()

        self.assertEqual(partij.nummer, "111222333")

        partij_identificator = partij.partijidentificator_set.get()

        self.assertEqual(
            partij_identificator.partij_identificator_code_objecttype,
            PartijIdentificatorCodeObjectType.natuurlijk_persoon,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_code_register,
            PartijIdentificatorCodeRegister.brp,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_code_soort_object_id,
            PartijIdentificatorCodeSoortObjectId.bsn,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_object_id, "111222333"
        )

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )
        expected_output = f"{self.live_server_url}{partij_url}"
        output = stdout.getvalue().splitlines()
        self.assertEqual(output, [expected_output])

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

    def test_natuurlijk_persoon_bsn_with_leading_zeroes(self):
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
        self.assertEqual(partij.nummer, "012345672")
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

    def test_natuurlijk_persoon_invalid_bsn(self):
        stdout = StringIO()

        call_command(
            "migrate_to_v2",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        self.assertFalse(Partij.objects.exists())
        self.assertFalse(Persoon.objects.exists())

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
        self.assertEqual(partij.nummer, "80737144")
        self.assertIsNone(partij.voorkeurs_digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)

        self.assertEqual(organisatie.naam, "Foobar Inc.")

        partij_identificator = partij.partijidentificator_set.get()

        self.assertEqual(
            partij_identificator.partij_identificator_code_objecttype,
            PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_code_register,
            PartijIdentificatorCodeRegister.hr,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_code_soort_object_id,
            PartijIdentificatorCodeSoortObjectId.kvk_nummer,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_object_id, "80737144"
        )

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

        self.assertEqual(persoon.contactnaam_voorletters, "W")
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
        self.assertEqual(partij.voorkeurs_digitaal_adres, digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)

        self.assertEqual(digitaal_adres.partij, partij)
        self.assertIsNone(digitaal_adres.betrokkene)
        self.assertEqual(digitaal_adres.soort_digitaal_adres, SoortDigitaalAdres.email)
        self.assertEqual(digitaal_adres.adres, "example@maykinmedia.nl")
        self.assertEqual(digitaal_adres.omschrijving, "")
        self.assertEqual(digitaal_adres.referentie, "portaalvoorkeur")

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
        with self.assertRaises(CommandError) as context_manager:
            call_command("migrate_to_v2", "foobar.com", self.live_server_url)

        self.assertEqual(Partij.objects.count(), 0)

        self.assertEqual(context_manager.exception.returncode, 1)
        self.assertIn("Invalid URL(s)", context_manager.exception.args[0])

    def test_existing_dummy_tokens(self):
        stdout = StringIO()

        token_application = "Migration application"

        TokenAuth(application=token_application)
        TokenAuth(application=token_application)
        TokenAuth(application=token_application)

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

        migration_tokens = TokenAuth.objects.filter(application=token_application)

        self.assertEqual(migration_tokens.count(), 0)

    def test_rsin(self):
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
        self.assertEqual(partij.nummer, "296648875")
        self.assertIsNone(partij.voorkeurs_digitaal_adres)
        self.assertIsNone(partij.voorkeurs_rekeningnummer)
        self.assertEqual(partij.interne_notitie, "")
        self.assertFalse(partij.indicatie_geheimhouding)
        self.assertEqual(partij.voorkeurstaal, "")
        self.assertTrue(partij.indicatie_actief)
        self.assertEqual(organisatie.naam, "Foobar Inc.")

        partij_identificator = partij.partijidentificator_set.get()
        self.assertEqual(
            partij_identificator.partij_identificator_code_objecttype,
            PartijIdentificatorCodeObjectType.niet_natuurlijk_persoon,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_code_register,
            PartijIdentificatorCodeRegister.hr,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_code_soort_object_id,
            PartijIdentificatorCodeSoortObjectId.rsin,
        )
        self.assertEqual(
            partij_identificator.partij_identificator_object_id, "296648875"
        )

        output = stdout.getvalue().splitlines()

        partij_url = reverse(
            "klantinteracties:partij-detail",
            kwargs={"uuid": str(partij.uuid)},
        )

        self.assertEqual(output, [f"{self.live_server_url}{partij_url}"])

    def test_telefoonnummer(self):
        partij = PartijFactory.create(
            soort_partij=SoortPartij.persoon, nummer="024325818"
        )

        stdout = StringIO()

        call_command(
            "migrate_to_v2_phonenumbers",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        digitaal_adressen = DigitaalAdres.objects.filter(partij=partij)

        self.assertEqual(digitaal_adressen.count(), 1)

        digitaal_adres = digitaal_adressen.first()
        self.assertEqual(digitaal_adres.adres, "0612345678")
        self.assertEqual(digitaal_adres.soort_digitaal_adres, "telefoonnummer")
        self.assertEqual(digitaal_adres.referentie, "portaalvoorkeur")
        self.assertEqual(digitaal_adres.partij, partij)

    def test_telefoonnummer_niet_natuurlijk_persoon(self):
        partij = PartijFactory.create(
            soort_partij=SoortPartij.organisatie, nummer="024325818"
        )

        stdout = StringIO()

        call_command(
            "migrate_to_v2_phonenumbers",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        digitaal_adressen = DigitaalAdres.objects.filter(partij=partij)

        self.assertEqual(digitaal_adressen.count(), 1)

        digitaal_adres = digitaal_adressen.first()
        self.assertEqual(digitaal_adres.adres, "0612345678")
        self.assertEqual(digitaal_adres.soort_digitaal_adres, "telefoonnummer")
        self.assertEqual(digitaal_adres.referentie, "portaalvoorkeur")
        self.assertEqual(digitaal_adres.partij, partij)

    def test_skip_telefoonnummer(self):
        partij = PartijFactory.create(
            soort_partij=SoortPartij.persoon, nummer="024325818"
        )
        DigitaalAdresFactory.create(
            partij=partij,
            adres="0123456789",
            soort_digitaal_adres="telefoonnummer",
            referentie="portaalvoorkeur",
        )
        digitaal_adressen = DigitaalAdres.objects.filter(partij=partij)

        self.assertEqual(digitaal_adressen.count(), 1)

        stdout = StringIO()

        call_command(
            "migrate_to_v2_phonenumbers",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        digitaal_adressen = DigitaalAdres.objects.filter(partij=partij)

        self.assertEqual(digitaal_adressen.count(), 1)

        digitaal_adres = digitaal_adressen.first()
        self.assertEqual(digitaal_adres.adres, "0123456789")
        self.assertEqual(digitaal_adres.soort_digitaal_adres, "telefoonnummer")
        self.assertEqual(digitaal_adres.referentie, "portaalvoorkeur")
        self.assertEqual(digitaal_adres.partij, partij)

    def test_no_telefoonnummer(self):
        partij = PartijFactory.create(
            soort_partij=SoortPartij.persoon, nummer="024325818"
        )

        stdout = StringIO()

        call_command(
            "migrate_to_v2_phonenumbers",
            "http://localhost:8000",
            self.live_server_url,
            stdout=stdout,
        )

        digitaal_adressen = DigitaalAdres.objects.filter(partij=partij)

        self.assertEqual(digitaal_adressen.count(), 0)
