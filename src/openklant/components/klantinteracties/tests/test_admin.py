from uuid import uuid4

from django.test import tag
from django.urls import reverse
from django.utils.translation import gettext as _

from django_webtest import WebTest
from maykin_2fa.test import disable_admin_mfa
from webtest import TestResponse

from openklant.accounts.tests.factories import SuperUserFactory
from openklant.components.klantinteracties.models import DigitaalAdres
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijFactory,
    PersoonFactory,
)
from openklant.utils.tests.webtest import add_dynamic_field

from ..constants import SoortDigitaalAdres


@disable_admin_mfa()
class PartijAdminTests(WebTest):
    def test_search(self):
        user = SuperUserFactory.create()
        self.app.set_user(user)

        nummer_persoon = PersoonFactory(
            partij__nummer="123456789",
            contactnaam_voornaam="Willem",
            contactnaam_achternaam="Wever",
        )

        uuid = uuid4()
        uuid_persoon = PersoonFactory(
            partij__uuid=uuid,
            contactnaam_voornaam="Henk",
            contactnaam_achternaam="Broek",
        )

        digitaal_adres = DigitaalAdresFactory(adres="foobar@example.com")

        digitaal_adres_persoon = PersoonFactory(
            partij__voorkeurs_digitaal_adres=digitaal_adres,
            contactnaam_voornaam="Sjaak",
            contactnaam_achternaam="Willemse",
        )

        admin_url = reverse("admin:klantinteracties_partij_changelist")

        # Test a nummer search query
        response: TestResponse = self.app.get(admin_url)
        search_form = response.forms["changelist-search"]

        search_form["q"] = nummer_persoon.partij.nummer
        search_response = search_form.submit()

        self.assertContains(search_response, nummer_persoon.get_full_name())
        self.assertNotContains(search_response, uuid_persoon.get_full_name())
        self.assertNotContains(search_response, digitaal_adres_persoon.get_full_name())

        # Test a uuid search query
        response: TestResponse = self.app.get(admin_url)
        search_form = response.forms["changelist-search"]

        search_form["q"] = str(uuid)
        search_response = search_form.submit()

        self.assertContains(search_response, uuid_persoon.get_full_name())
        self.assertNotContains(search_response, nummer_persoon.get_full_name())
        self.assertNotContains(search_response, digitaal_adres_persoon.get_full_name())

        # Test a adres search query
        response: TestResponse = self.app.get(admin_url)
        search_form = response.forms["changelist-search"]

        search_form["q"] = digitaal_adres.adres
        search_response = search_form.submit()

        self.assertContains(search_response, digitaal_adres_persoon.get_full_name())
        self.assertNotContains(search_response, nummer_persoon.get_full_name())
        self.assertNotContains(search_response, uuid_persoon.get_full_name())

    @disable_admin_mfa()
    def test_digitaal_adres_inline(self):
        """
        Regression test for #226

        betrokkene should be optional
        """

        user = SuperUserFactory(username="admin", password="admin")
        self.app.set_user(user)

        partij = PartijFactory(soort_partij="persoon", voorkeurs_digitaal_adres=None)
        PersoonFactory(partij=partij)
        url = reverse("admin:klantinteracties_partij_change", args=[partij.pk])

        response = self.app.get(url)

        form = response.form
        form["digitaaladres_set-TOTAL_FORMS"] = 1
        add_dynamic_field(form, "digitaaladres_set-0-omschrijving", "description")
        add_dynamic_field(form, "digitaaladres_set-0-soort_digitaal_adres", "email")
        add_dynamic_field(form, "digitaaladres_set-0-adres", "email@example.com")

        response = form.submit()
        self.assertEqual(response.status_code, 302)

        adres = DigitaalAdres.objects.get()

        self.assertEqual(adres.omschrijving, "description")
        self.assertEqual(adres.adres, "email@example.com")
        self.assertIsNone(adres.betrokkene)


@disable_admin_mfa()
class DigitaalAdresAdminTests(WebTest):
    @tag("gh-234")
    def test_email_validation(self):
        """
        Check that the admin applies conditional email validation on `adres`, only if
        `soort_digitaal_adres` is `email`
        """
        user = SuperUserFactory.create()
        self.app.set_user(user)

        betrokkene = BetrokkeneFactory.create()

        admin_url = reverse("admin:klantinteracties_digitaaladres_add")

        with self.subTest("apply validation for soort_digitaal_adres == email"):
            response: TestResponse = self.app.get(admin_url)

            form = response.form
            form["betrokkene"] = betrokkene.pk
            form["soort_digitaal_adres"] = SoortDigitaalAdres.email
            form["adres"] = "invalid"
            form["omschrijving"] = "foo"

            response = form.submit()

            self.assertEqual(response.status_code, 200)
            self.assertFalse(DigitaalAdres.objects.exists())
            self.assertEqual(
                response.context["errors"], [[_("Voer een geldig e-mailadres in.")]]
            )

        with self.subTest("do not apply validation for soort_digitaal_adres != email"):
            response: TestResponse = self.app.get(admin_url)

            form = response.form
            form["betrokkene"] = betrokkene.pk
            form["soort_digitaal_adres"] = SoortDigitaalAdres.telefoonnummer
            form["adres"] = "0612345678"
            form["omschrijving"] = "foo"

            response = form.submit()

            self.assertEqual(response.status_code, 302)
            self.assertTrue(DigitaalAdres.objects.exists())
