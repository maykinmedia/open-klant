from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from django_webtest import WebTest
from maykin_2fa.test import disable_admin_mfa
from maykin_common.vcr import VCRMixin
from requests.exceptions import RequestException, Timeout
from zgw_consumers.test.factories import ServiceFactory

from openklant.accounts.tests.factories import SuperUserFactory
from openklant.components.klantinteracties.models.tests.factories import (
    KlantcontactFactory,
)

from ..models import ReferentielijstenConfig


@disable_admin_mfa()
class ReferentielijstenConfigAdminTests(VCRMixin, WebTest):
    url = reverse_lazy("admin:config_referentielijstenconfig_change")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = SuperUserFactory.create()

        cls.service = ServiceFactory.create(
            slug="referentielijsten",
            api_root="http://localhost:8004/api/v1",
        )

    def setUp(self):
        super().setUp()

        self.app.set_user(self.user)

        self._clear_config()
        self.addCleanup(self._clear_config)

    def _clear_config(self):
        ReferentielijstenConfig.get_solo().delete()

    def test_success(self):
        response = self.app.get(self.url)

        form = response.forms["referentielijstenconfig_form"]

        form["enabled"] = True
        form["service"] = self.service.pk
        form["kanalen_tabel_code"] = "KANAAL"

        response = form.submit()

        self.assertEqual(response.status_code, 302)

        config = ReferentielijstenConfig.get_solo()

        self.assertTrue(config.enabled)
        self.assertEqual(config.service, self.service)
        self.assertEqual(config.kanalen_tabel_code, "KANAAL")

    def test_if_disabled_does_not_trigger_validation(self):
        service = ServiceFactory.create(
            slug="non-existent-service",
            api_root="http://does-not-exist:8004/api/v1",
        )
        response = self.app.get(self.url)

        form = response.forms["referentielijstenconfig_form"]

        form["enabled"] = False
        form["service"] = service.pk
        form["kanalen_tabel_code"] = "KANAAL"

        response = form.submit()

        self.assertEqual(response.status_code, 302)

        config = ReferentielijstenConfig.get_solo()

        self.assertFalse(config.enabled)
        self.assertEqual(config.service, service)
        self.assertEqual(config.kanalen_tabel_code, "KANAAL")

    def test_missing_service_raises_error(self):
        response = self.app.get(self.url)

        form = response.forms["referentielijstenconfig_form"]

        form["enabled"] = True
        form["kanalen_tabel_code"] = "KANAAL"

        response = form.submit()

        self.assertEqual(response.status_code, 200)

        config = ReferentielijstenConfig.get_solo()

        self.assertFalse(config.enabled)
        self.assertIsNone(config.service)
        self.assertEqual(config.kanalen_tabel_code, "")

    def test_missing_kanalen_tabel_code_raises_error(self):
        response = self.app.get(self.url)

        form = response.forms["referentielijstenconfig_form"]

        form["enabled"] = True
        form["service"] = self.service.pk
        form["kanalen_tabel_code"] = ""

        response = form.submit()

        self.assertEqual(response.status_code, 200)

        config = ReferentielijstenConfig.get_solo()

        self.assertFalse(config.enabled)
        self.assertIsNone(config.service)
        self.assertEqual(config.kanalen_tabel_code, "")

    def test_request_error_from_referentielijsten_raises_error(self):
        response = self.app.get(self.url)

        form = response.forms["referentielijstenconfig_form"]

        form["enabled"] = True
        form["service"] = self.service.pk
        form["kanalen_tabel_code"] = "KANAAL"

        with self.vcr_raises(Timeout):
            response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["errors"],
            [
                [
                    "Er is een fout opgetreden bij het ophalen van de kanalen uit de Referentielijsten API."
                ]
            ],
        )

        config = ReferentielijstenConfig.get_solo()

        self.assertFalse(config.enabled)
        self.assertIsNone(config.service)
        self.assertEqual(config.kanalen_tabel_code, "")

    def test_existing_klantcontacten_with_invalid_kanalen_raises_error(self):
        KlantcontactFactory.create(kanaal="non-existent1")
        KlantcontactFactory.create(kanaal="non-existent2")

        response = self.app.get(self.url)

        form = response.forms["referentielijstenconfig_form"]

        form["enabled"] = True
        form["service"] = self.service.pk
        form["kanalen_tabel_code"] = "KANAAL"

        response = form.submit()

        self.assertEqual(response.status_code, 200)

        invalid_kanalen = "non-existent1, non-existent2"

        self.assertEqual(
            response.context["errors"],
            [
                [
                    _(
                        "Sommige bestaande Klantcontact.kanaal waarden zijn niet aanwezig in Referentielijsten: {invalid_kanalen}"
                    ).format(invalid_kanalen=invalid_kanalen)
                ]
            ],
        )

        config = ReferentielijstenConfig.get_solo()

        self.assertFalse(config.enabled)
        self.assertIsNone(config.service)
        self.assertEqual(config.kanalen_tabel_code, "")

    def test_status_check_returns_http_status_and_items(self):
        response = self.app.get(self.url)
        form = response.forms["referentielijstenconfig_form"]

        form["enabled"] = True
        form["service"] = self.service.pk
        form["kanalen_tabel_code"] = "KANAAL"

        form.submit()

        config = ReferentielijstenConfig.get_solo()

        try:
            result = config.status_check()
        except RequestException:
            self.fail("Connection to Referentielijsten service failed")

        self.assertIn("status_code", result)
        self.assertIn("items", result)
        self.assertEqual(result["status_code"], 200)
        self.assertIsInstance(result["items"], list)
