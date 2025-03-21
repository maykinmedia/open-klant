from uuid import uuid4

from django.test import tag
from django.urls import reverse
from django.utils.translation import gettext as _

from django_webtest import WebTest
from freezegun.api import freeze_time
from maykin_2fa.test import disable_admin_mfa
from webtest import TestResponse

from openklant.accounts.tests.factories import SuperUserFactory
from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    ActorKlantcontactFactory,
    BetrokkeneFactory,
    DigitaalAdresFactory,
    GeautomatiseerdeActorFactory,
    InterneTaakFactory,
    KlantcontactFactory,
    MedewerkerFactory,
    PartijFactory,
    PersoonFactory,
)
from openklant.utils.tests.webtest import add_dynamic_field

from ..constants import SoortDigitaalAdres
from ..models import (
    Actor,
    ActorKlantcontact,
    DigitaalAdres,
    InterneTaak,
    InterneTakenActorenThoughModel,
    Klantcontact,
    Medewerker,
    SoortActor,
    Taakstatus,
)


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
        user = SuperUserFactory.create()
        self.app.set_user(user)

        betrokkene = BetrokkeneFactory.create()

        admin_url = reverse("admin:klantinteracties_digitaaladres_add")

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

    @tag("gh-234")
    def test_telefoonnummer_validation(self):
        user = SuperUserFactory.create()
        self.app.set_user(user)

        betrokkene = BetrokkeneFactory.create()

        admin_url = reverse("admin:klantinteracties_digitaaladres_add")

        response: TestResponse = self.app.get(admin_url)

        form = response.form
        form["betrokkene"] = betrokkene.pk
        form["soort_digitaal_adres"] = SoortDigitaalAdres.telefoonnummer
        form["adres"] = "invalid"
        form["omschrijving"] = "foo"

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(DigitaalAdres.objects.exists())
        self.assertEqual(
            response.context["errors"],
            [[_("Het opgegeven telefoonnummer is ongeldig.")]],
        )

    @tag("gh-234")
    def test_overig_has_no_validation(self):
        user = SuperUserFactory.create()
        self.app.set_user(user)

        betrokkene = BetrokkeneFactory.create()

        admin_url = reverse("admin:klantinteracties_digitaaladres_add")

        response: TestResponse = self.app.get(admin_url)

        form = response.form
        form["betrokkene"] = betrokkene.pk
        form["soort_digitaal_adres"] = SoortDigitaalAdres.overig
        form["adres"] = "whatever"
        form["omschrijving"] = "foo"

        response = form.submit()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(DigitaalAdres.objects.exists())


@disable_admin_mfa()
class ActorenAdminTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = SuperUserFactory.create()

    def test_search_naam(self):
        self.app.set_user(self.user)

        ActorFactory.create(naam="Richard")
        ActorFactory.create(naam="Pauline")

        admin_url = reverse("admin:klantinteracties_actor_changelist")

        response: TestResponse = self.app.get(admin_url)

        self.assertContains(response, "field-naam", 2)

        search_form = response.forms["changelist-search"]
        search_form["q"] = "Pauline"

        search_response: TestResponse = search_form.submit()

        self.assertEqual(search_response.status_code, 200)
        self.assertContains(search_response, "field-naam", 1)

    def test_list_filter_soort_actor(self):
        self.app.set_user(self.user)

        MedewerkerFactory.create(actor__soort_actor=SoortActor.medewerker)
        GeautomatiseerdeActorFactory.create(
            actor__soort_actor=SoortActor.geautomatiseerde_actor
        )

        admin_url = reverse("admin:klantinteracties_actor_changelist")

        response: TestResponse = self.app.get(admin_url)

        self.assertContains(response, "field-soort_actor", 2)

        search_response: TestResponse = response.click(
            description=_(SoortActor.medewerker.label)
        )

        self.assertEqual(search_response.status_code, 200)
        self.assertContains(search_response, "field-soort_actor", 1)

    def test_list_filter_indicatie_actief(self):
        self.app.set_user(self.user)

        ActorFactory.create(indicatie_actief=True)
        ActorFactory.create(indicatie_actief=False)

        admin_url = reverse("admin:klantinteracties_actor_changelist")

        response: TestResponse = self.app.get(admin_url)

        self.assertContains(response, "field-naam", 2)

        search_response: TestResponse = response.click(href="indicatie_actief__exact=1")

        self.assertEqual(search_response.status_code, 200)
        self.assertContains(search_response, "field-soort_actor", 1)

    def test_actor_create(self):
        assert not Actor.objects.exists()
        assert not Medewerker.objects.exists()
        assert not InterneTakenActorenThoughModel.objects.exists()
        assert not ActorKlantcontact.objects.exists()

        self.app.set_user(self.user)

        klantcontact: Klantcontact = KlantcontactFactory.create()
        internetaak: InterneTaak = InterneTaakFactory.create()

        admin_url = reverse("admin:klantinteracties_actor_add")

        response: TestResponse = self.app.get(admin_url)

        form = response.forms["actor_form"]
        form["actorklantcontact_set-TOTAL_FORMS"] = 1
        form["medewerker-TOTAL_FORMS"] = 1
        form["internetakenactorenthoughmodel_set-TOTAL_FORMS"] = 1

        form["naam"] = "Richard"
        form["soort_actor"].select(text=SoortActor.medewerker.label)
        form["indicatie_actief"] = 1

        form["actoridentificator_code_objecttype"] = "objecttype code"
        form["actoridentificator_code_soort_object_id"] = "soort object id"
        form["actoridentificator_object_id"] = "object id"
        form["actoridentificator_code_register"] = "code register"

        add_dynamic_field(form, "actorklantcontact_set-0-klantcontact", klantcontact.pk)

        add_dynamic_field(form, "medewerker-0-functie", "TEST")
        add_dynamic_field(form, "medewerker-0-emailadres", "example@test.com")
        add_dynamic_field(form, "medewerker-0-telefoonnummer", "+31618234723")

        add_dynamic_field(
            form,
            "internetakenactorenthoughmodel_set-0-internetaak",
            str(internetaak.pk),
        )

        add_response: TestResponse = form.submit(name="_save")

        self.assertRedirects(
            add_response, reverse("admin:klantinteracties_actor_changelist")
        )

        created_actor: Actor = Actor.objects.get()

        self.assertEqual(created_actor.naam, "Richard")
        self.assertEqual(created_actor.soort_actor, SoortActor.medewerker)
        self.assertEqual(created_actor.indicatie_actief, True)

        self.assertEqual(
            created_actor.actoridentificator_code_objecttype, "objecttype code"
        )
        self.assertEqual(
            created_actor.actoridentificator_code_soort_object_id, "soort object id"
        )
        self.assertEqual(created_actor.actoridentificator_object_id, "object id")
        self.assertEqual(
            created_actor.actoridentificator_code_register, "code register"
        )

        created_actor_klantcontact: ActorKlantcontact = ActorKlantcontact.objects.get()

        self.assertEqual(created_actor_klantcontact.actor, created_actor)
        self.assertEqual(created_actor_klantcontact.klantcontact, klantcontact)

        created_medewerker: Medewerker = Medewerker.objects.get()

        self.assertEqual(created_medewerker.actor, created_actor)
        self.assertEqual(created_medewerker.functie, "TEST")
        self.assertEqual(created_medewerker.emailadres, "example@test.com")
        self.assertEqual(created_medewerker.telefoonnummer, "+31618234723")

        created_internetaak_actoren_m2m: InterneTakenActorenThoughModel = (
            InterneTakenActorenThoughModel.objects.get()
        )

        self.assertEqual(created_internetaak_actoren_m2m.actor, created_actor)
        self.assertEqual(created_internetaak_actoren_m2m.internetaak, internetaak)

    def test_actor_update(self):
        self.app.set_user(self.user)

        actor = ActorFactory.create(
            naam="Richard",
            soort_actor=SoortActor.medewerker,
            indicatie_actief=False,
            actoridentificator_object_id="a",
            actoridentificator_code_objecttype="a",
            actoridentificator_code_register="a",
            actoridentificator_code_soort_object_id="a",
        )

        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        InterneTaakFactory.create(actoren=[actor])
        internetaak2: InterneTaak = InterneTaakFactory.create()

        ActorKlantcontactFactory.create(actor=actor, klantcontact=klantcontact)

        MedewerkerFactory.create(
            actor=actor,
            functie="TEST",
            emailadres="example@test.com",
            telefoonnummer="+31618234723",
        )

        admin_url = reverse("admin:klantinteracties_actor_change", args=[actor.id])

        response: TestResponse = self.app.get(admin_url)

        form = response.forms["actor_form"]
        form["naam"] = "Pauline"
        form["soort_actor"].select(text=SoortActor.medewerker.label)
        form["indicatie_actief"] = 1

        form["actoridentificator_code_objecttype"] = "objecttype code"
        form["actoridentificator_code_soort_object_id"] = "soort object id"
        form["actoridentificator_object_id"] = "object id"
        form["actoridentificator_code_register"] = "code register"

        form["actorklantcontact_set-0-klantcontact"] = klantcontact2.pk

        form["medewerker-0-functie"] = "changed"
        form["medewerker-0-emailadres"] = "changed@email.com"
        form["medewerker-0-telefoonnummer"] = "+31618239999"

        form["internetakenactorenthoughmodel_set-0-internetaak"] = str(internetaak2.pk)

        add_response: TestResponse = form.submit(name="_save")

        self.assertRedirects(
            add_response, reverse("admin:klantinteracties_actor_changelist")
        )

        actor.refresh_from_db()

        self.assertEqual(actor.naam, "Pauline")
        self.assertEqual(actor.soort_actor, SoortActor.medewerker)
        self.assertEqual(actor.indicatie_actief, True)

        self.assertEqual(actor.actoridentificator_code_objecttype, "objecttype code")
        self.assertEqual(
            actor.actoridentificator_code_soort_object_id, "soort object id"
        )
        self.assertEqual(actor.actoridentificator_object_id, "object id")
        self.assertEqual(actor.actoridentificator_code_register, "code register")

        actor_klantcontact: ActorKlantcontact = actor.actorklantcontact_set.get()

        self.assertEqual(actor_klantcontact.klantcontact, klantcontact2)

        medewerker: Medewerker = actor.medewerker

        self.assertEqual(medewerker.functie, "changed")
        self.assertEqual(medewerker.emailadres, "changed@email.com")
        self.assertEqual(medewerker.telefoonnummer, "+31618239999")

        interetaak_actoren: InterneTakenActorenThoughModel = (
            actor.internetakenactorenthoughmodel_set.get()
        )

        self.assertEqual(interetaak_actoren.internetaak, internetaak2)

    def test_actor_delete(self):
        self.app.set_user(self.user)

        actor: Actor = ActorFactory.create()

        delete_url = reverse("admin:klantinteracties_actor_delete", args=[actor.id])

        response: TestResponse = self.app.get(delete_url)

        self.assertEqual(response.status_code, 200)

        form = response.forms[0]

        response: TestResponse = form.submit()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Actor.objects.filter(uuid=actor.uuid).exists())


@disable_admin_mfa()
class IntereTaakAdminTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = SuperUserFactory.create()

    def test_internetaak_search(self):
        self.app.set_user(self.user)

        InterneTaakFactory.create(nummer="0000000001")
        InterneTaakFactory.create(nummer="0000000002")

        admin_url = reverse("admin:klantinteracties_internetaak_changelist")

        response: TestResponse = self.app.get(admin_url)

        self.assertContains(response, "field-nummer", 2)

        search_form = response.forms["changelist-search"]
        search_form["q"] = "0000000002"

        search_response: TestResponse = search_form.submit()

        self.assertEqual(search_response.status_code, 200)
        self.assertContains(search_response, "field-nummer", 1)

    def test_internetaak_filter_actors(self):
        self.app.set_user(self.user)

        actor: Actor = ActorFactory.create(naam="Richard")
        actor2: Actor = ActorFactory.create(naam="Pauline")

        InterneTaakFactory.create(nummer="0000000001", actoren=[actor])
        InterneTaakFactory.create(nummer="0000000002", actoren=[actor2])

        admin_url = reverse("admin:klantinteracties_internetaak_changelist")

        response: TestResponse = self.app.get(admin_url)

        self.assertContains(response, "field-nummer", 2)

        # See if both actors are filter options
        self.assertContains(response, "Richard", 1)
        self.assertContains(response, "Pauline", 1)

        # Filter on actor name
        search_response: TestResponse = response.click(description="Richard")

        self.assertEqual(search_response.status_code, 200)
        self.assertContains(search_response, "field-nummer", 1)
        self.assertContains(search_response, "0000000001", 1)

    def test_internetaak_filter_status(self):
        self.app.set_user(self.user)

        InterneTaakFactory.create(nummer="0000000001", status=Taakstatus.te_verwerken)
        InterneTaakFactory.create(nummer="0000000002", status=Taakstatus.verwerkt)

        admin_url = reverse("admin:klantinteracties_internetaak_changelist")

        response: TestResponse = self.app.get(admin_url)

        self.assertContains(response, "field-nummer", 2)

        # Filter on actor name
        search_response: TestResponse = response.click(
            description=_(Taakstatus.verwerkt.label)
        )

        self.assertEqual(search_response.status_code, 200)
        self.assertContains(search_response, "field-nummer", 1)
        self.assertContains(search_response, "0000000002", 1)

    def test_interetaak_create(self):
        assert not InterneTaak.objects.exists()
        assert not InterneTakenActorenThoughModel.objects.exists()

        self.app.set_user(self.user)

        actor: Actor = ActorFactory.create()
        klantcontact: Klantcontact = KlantcontactFactory.create()

        admin_url = reverse("admin:klantinteracties_internetaak_add")

        response: TestResponse = self.app.get(admin_url)

        form = response.forms["internetaak_form"]
        form["internetakenactorenthoughmodel_set-TOTAL_FORMS"] = 1

        form["klantcontact"].select(text=str(klantcontact))
        form["nummer"] = "0000000001"
        form["gevraagde_handeling"] = "Terugbellen"
        form["toelichting"] = "bla bla bla"
        form["status"].select(text=_(Taakstatus.verwerkt.label))
        form["afgehandeld_op_0"] = "2024-01-01"
        form["afgehandeld_op_1"] = "16:30:00"

        add_dynamic_field(form, "internetakenactorenthoughmodel_set-0-actor", actor.pk)

        with freeze_time("2024-01-01 18:00:00+00:00"):
            add_response: TestResponse = form.submit(name="_save")

        self.assertRedirects(
            add_response, reverse("admin:klantinteracties_internetaak_changelist")
        )

        created_internetaak: InterneTaak = InterneTaak.objects.get()

        self.assertEqual(created_internetaak.klantcontact, klantcontact)
        self.assertEqual(created_internetaak.nummer, "0000000001")
        self.assertEqual(created_internetaak.gevraagde_handeling, "Terugbellen")
        self.assertEqual(created_internetaak.toelichting, "bla bla bla")
        self.assertEqual(created_internetaak.status, Taakstatus.verwerkt)
        self.assertEqual(
            str(created_internetaak.toegewezen_op), "2024-01-01 18:00:00+00:00"
        )
        self.assertEqual(
            str(created_internetaak.afgehandeld_op), "2024-01-01 16:30:00+00:00"
        )

        self.assertEqual(created_internetaak.actoren.get(), actor)

    def test_interetaak_create_number_automatically_sets_itself(self):
        assert not InterneTaak.objects.exists()
        assert not InterneTakenActorenThoughModel.objects.exists()

        self.app.set_user(self.user)

        klantcontact: Klantcontact = KlantcontactFactory.create()

        admin_url = reverse("admin:klantinteracties_internetaak_add")

        response: TestResponse = self.app.get(admin_url)

        form = response.forms["internetaak_form"]
        form["klantcontact"].select(text=str(klantcontact))
        form["gevraagde_handeling"] = "Terugbellen"
        form["status"].select(text=_(Taakstatus.verwerkt.label))

        add_response: TestResponse = form.submit(name="_save")

        self.assertRedirects(
            add_response, reverse("admin:klantinteracties_internetaak_changelist")
        )

        created_internetaak: InterneTaak = InterneTaak.objects.get()

        # set number at first possible index
        self.assertEqual(created_internetaak.nummer, "0000000001")

    def test_internetaak_update(self):
        self.app.set_user(self.user)

        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)

        with freeze_time("2023-01-01 00:00:00+00:00"):
            internetaak: InterneTaak = InterneTaakFactory.create(
                actoren=[actor],
                klantcontact=klantcontact,
                nummer="0000000001",
                gevraagde_handeling="foo",
                toelichting="bar",
                status=Taakstatus.te_verwerken,
                afgehandeld_op="2023-01-01 00:00:00+00:00",
            )

        admin_url = reverse(
            "admin:klantinteracties_internetaak_change", args=[internetaak.pk]
        )

        response: TestResponse = self.app.get(admin_url)

        form = response.forms["internetaak_form"]
        form["klantcontact"].select(text=str(klantcontact2))
        form["nummer"] = "0000000009"
        form["gevraagde_handeling"] = "Terugbellen"
        form["toelichting"] = "bla bla bla"
        form["status"].select(text=_(Taakstatus.verwerkt.label))
        form["afgehandeld_op_0"] = "2024-01-01"
        form["afgehandeld_op_1"] = "16:30:00"

        form["internetakenactorenthoughmodel_set-0-actor"] = actor2.pk

        with freeze_time("2024-01-01 18:00:00+00:00"):
            add_response: TestResponse = form.submit(name="_save")

        self.assertRedirects(
            add_response, reverse("admin:klantinteracties_internetaak_changelist")
        )

        created_internetaak: InterneTaak = InterneTaak.objects.get()

        self.assertEqual(created_internetaak.klantcontact, klantcontact2)
        self.assertEqual(created_internetaak.nummer, "0000000009")
        self.assertEqual(created_internetaak.gevraagde_handeling, "Terugbellen")
        self.assertEqual(created_internetaak.toelichting, "bla bla bla")
        self.assertEqual(created_internetaak.status, Taakstatus.verwerkt)
        self.assertEqual(
            str(created_internetaak.toegewezen_op), "2023-01-01 00:00:00+00:00"
        )
        self.assertEqual(
            str(created_internetaak.afgehandeld_op), "2024-01-01 16:30:00+00:00"
        )

        self.assertEqual(created_internetaak.actoren.get(), actor2)

    def test_internetaak_delete(self):
        self.app.set_user(self.user)

        internetaak: InterneTaak = InterneTaakFactory.create()

        delete_url = reverse(
            "admin:klantinteracties_internetaak_delete", args=[internetaak.id]
        )

        response: TestResponse = self.app.get(delete_url)

        self.assertEqual(response.status_code, 200)

        form = response.forms[0]

        response: TestResponse = form.submit()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(InterneTaak.objects.filter(uuid=internetaak.uuid).exists())
