import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..api.tests import factories


class ReferentielijstenAdminTests(TestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(
            get_user_model()._default_manager.create(
                username="root", is_superuser=True, is_staff=True
            )
        )

    def test_landadmin_indicatie_actief_true(self):
        factories.LandFactory(ingangsdatum_land=datetime.date.today())
        url = reverse("admin:referentielijsten_land_changelist")

        response = self.client.get(url)

        self.assertContains(
            response,
            '<td class="field-indicatie_actief"><img src="/static/admin/img/icon-yes.svg" alt="True"></td>',
        )
        self.assertNotContains(
            response,
            '<td class="field-indicatie_actief"><img src="/static/admin/img/icon-no.svg" alt="False"></td>',
        )

    def test_landadmin_indicatie_actief_false(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        factories.LandFactory(ingangsdatum_land=tomorrow)
        url = reverse("admin:referentielijsten_land_changelist")

        response = self.client.get(url)

        self.assertNotContains(
            response,
            '<td class="field-indicatie_actief"><img src="/static/admin/img/icon-yes.svg" alt="True"></td>',
        )
        self.assertContains(
            response,
            '<td class="field-indicatie_actief"><img src="/static/admin/img/icon-no.svg" alt="False"></td>',
        )
