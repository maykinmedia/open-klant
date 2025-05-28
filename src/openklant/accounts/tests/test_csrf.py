from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from openklant.accounts.tests.factories import SuperUserFactory


@override_settings(CSRF_FAILURE_VIEW="openklant.accounts.views.csrf.csrf_failure")
class CSRFCustomViewTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = SuperUserFactory(
            username="admin",
            password="admin",
        )

    def test_redirect_on_csrf_failure_if_logged_in(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("admin:login"), {})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)

    def test_normal_csrf_failure_when_not_logged_in(self):
        response = self.client.post(reverse("admin:login"), {})
        self.assertEqual(response.status_code, 403)
