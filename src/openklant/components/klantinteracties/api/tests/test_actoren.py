from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
    GeautomatiseerdeActorFactory,
    MedewerkerFactory,
    OrganisatorischeEenheidFactory,
)


class ActorTests(JWTAuthMixin, APITestCase):
    def test_list_actor(self):
        list_url = reverse("actor-list")
        ActorFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_actor(self):
        actor = ActorFactory.create()
        detail_url = reverse("actor-detail", kwargs={"uuid": str(actor.uuid)})

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_actor(self):
        list_url = reverse("actor-list")
        data = {
            "naam": "Phil",
            "soortActor": "medewerker",
            "indicatieActief": True,
            "objectidentificator": {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["naam"], "Phil")
        self.assertEqual(data["soortActor"], "medewerker")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

        # TODO: write subtest test to test if actor's unique is true validation works propperly

    def test_update_actor(self):
        actor = ActorFactory.create(
            naam="Phil",
            soort_actor="medewerker",
            indicatie_actief=True,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        detail_url = reverse("actor-detail", kwargs={"uuid": str(actor.uuid)})
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["naam"], "Phil")
        self.assertEqual(data["soortActor"], "medewerker")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

        data = {
            "naam": "changed",
            "soortActor": "geautomatiseerde_actor",
            "indicatieActief": False,
            "objectidentificator": {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["naam"], "changed")
        self.assertEqual(data["soortActor"], "geautomatiseerde_actor")
        self.assertFalse(data["indicatieActief"])
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        )

        # TODO: write subtest test to test if actor's unique is true validation works propperly

    def test_partial_update_actor(self):
        actor = ActorFactory.create(
            naam="Phil",
            soort_actor="medewerker",
            indicatie_actief=True,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        detail_url = reverse("actor-detail", kwargs={"uuid": str(actor.uuid)})
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["naam"], "Phil")
        self.assertEqual(data["soortActor"], "medewerker")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

        data = {
            "naam": "changed",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["naam"], "changed")
        self.assertEqual(data["soortActor"], "medewerker")
        self.assertTrue(data["indicatieActief"])
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

    def test_destroy_actor(self):
        actor = ActorFactory.create()
        detail_url = reverse("actor-detail", kwargs={"uuid": str(actor.uuid)})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("actor-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class GeautomatiseerdeActorTests(JWTAuthMixin, APITestCase):
    def test_list_geatomatiseerde_actor(self):
        list_url = reverse("geautomatiseerdeactor-list")
        GeautomatiseerdeActorFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_geatomatiseerde_actor(self):
        geautomatiseerde_actor = GeautomatiseerdeActorFactory.create()
        detail_url = reverse(
            "geautomatiseerdeactor-detail",
            kwargs={"id": str(geautomatiseerde_actor.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_geatomatiseerde_actor(self):
        actor = ActorFactory.create()
        list_url = reverse("geautomatiseerdeactor-list")
        data = {
            "actor": {"uuid": str(actor.uuid)},
            "functie": "functie",
            "omschrijving": "omschrijving",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "functie")
        self.assertEqual(data["omschrijving"], "omschrijving")

    def test_update_geatomatiseerde_actor(self):
        actor, actor2 = ActorFactory.create_batch(2)
        geatomatiseerde_actor = GeautomatiseerdeActorFactory.create(
            actor=actor,
            functie="functie",
            omschrijving="omschrijving",
        )
        detail_url = reverse(
            "geautomatiseerdeactor-detail",
            kwargs={"id": str(geatomatiseerde_actor.id)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "functie")
        self.assertEqual(data["omschrijving"], "omschrijving")

        data = {
            "actor": {"uuid": str(actor2.uuid)},
            "functie": "changed",
            "omschrijving": "changed",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor2.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "changed")
        self.assertEqual(data["omschrijving"], "changed")

    def test_partial_update_geatomatiseerde_actor(self):
        actor = ActorFactory.create()
        geatomatiseerde_actor = GeautomatiseerdeActorFactory.create(
            actor=actor,
            functie="functie",
            omschrijving="omschrijving",
        )
        detail_url = reverse(
            "geautomatiseerdeactor-detail",
            kwargs={"id": str(geatomatiseerde_actor.id)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "functie")
        self.assertEqual(data["omschrijving"], "omschrijving")

        data = {
            "functie": "changed",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "changed")
        self.assertEqual(data["omschrijving"], "omschrijving")

    def test_destroy_geatomatiseerde_actor(self):
        geautomatiseerde_actor = GeautomatiseerdeActorFactory.create()
        detail_url = reverse(
            "geautomatiseerdeactor-detail",
            kwargs={"id": str(geautomatiseerde_actor.id)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("geautomatiseerdeactor-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class MedewerkerTests(JWTAuthMixin, APITestCase):
    def test_list_medewerker(self):
        list_url = reverse("medewerker-list")
        MedewerkerFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_medewerker(self):
        medewerker = MedewerkerFactory.create()
        detail_url = reverse(
            "medewerker-detail",
            kwargs={"id": str(medewerker.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_medewerker(self):
        actor = ActorFactory.create()
        list_url = reverse("medewerker-list")
        data = {
            "actor": {"uuid": str(actor.uuid)},
            "functie": "functie",
            "emailadres": "example@email.com",
            "telefoonnummer": "7762323",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "functie")
        self.assertEqual(data["emailadres"], "example@email.com")
        self.assertEqual(data["telefoonnummer"], "7762323")

    def test_update_medewerker(self):
        actor, actor2 = ActorFactory.create_batch(2)
        medewerker = MedewerkerFactory.create(
            actor=actor,
            functie="functie",
            emailadres="example@email.com",
            telefoonnummer="7762323",
        )
        detail_url = reverse(
            "medewerker-detail",
            kwargs={"id": str(medewerker.id)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "functie")
        self.assertEqual(data["emailadres"], "example@email.com")
        self.assertEqual(data["telefoonnummer"], "7762323")

        data = {
            "actor": {"uuid": str(actor2.uuid)},
            "functie": "changed",
            "emailadres": "changed@email.com",
            "telefoonnummer": "5551212",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor2.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "changed")
        self.assertEqual(data["emailadres"], "changed@email.com")
        self.assertEqual(data["telefoonnummer"], "5551212")

    def test_partial_update_medewerker(self):
        actor = ActorFactory.create()
        medewerker = MedewerkerFactory.create(
            actor=actor,
            functie="functie",
            emailadres="example@email.com",
            telefoonnummer="7762323",
        )
        detail_url = reverse(
            "medewerker-detail",
            kwargs={"id": str(medewerker.id)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "functie")
        self.assertEqual(data["emailadres"], "example@email.com")
        self.assertEqual(data["telefoonnummer"], "7762323")

        data = {
            "functie": "changed",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["functie"], "changed")
        self.assertEqual(data["emailadres"], "example@email.com")
        self.assertEqual(data["telefoonnummer"], "7762323")

    def test_destroy_medewerker(self):
        medewerker = MedewerkerFactory.create()
        detail_url = reverse(
            "medewerker-detail",
            kwargs={"id": str(medewerker.id)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("medewerker-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class OrganisatorischeEenheidTests(JWTAuthMixin, APITestCase):
    def test_list_organisatorische_eenheid(self):
        list_url = reverse("organisatorischeeenheid-list")
        OrganisatorischeEenheidFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_organisatorische_eenheid(self):
        organisatorische_eenheid = OrganisatorischeEenheidFactory.create()
        detail_url = reverse(
            "organisatorischeeenheid-detail",
            kwargs={"id": str(organisatorische_eenheid.id)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organisatorische_eenheid(self):
        actor = ActorFactory.create()
        list_url = reverse("organisatorischeeenheid-list")
        data = {
            "actor": {"uuid": str(actor.uuid)},
            "omschrijving": "omschrijving",
            "emailadres": "example@email.com",
            "faxnummer": "7762323",
            "telefoonnummer": "7762323",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["omschrijving"], "omschrijving")
        self.assertEqual(data["emailadres"], "example@email.com")
        self.assertEqual(data["faxnummer"], "7762323")
        self.assertEqual(data["telefoonnummer"], "7762323")

        # TODO: write subtest test to test if actor's unique is true validation works propperly

    def test_update_organisatorische_eenheid(self):
        actor, actor2 = ActorFactory.create_batch(2)
        organisatorische_eenheid = OrganisatorischeEenheidFactory.create(
            actor=actor,
            omschrijving="omschrijving",
            emailadres="example@email.com",
            faxnummer="7762323",
            telefoonnummer="7762323",
        )
        detail_url = reverse(
            "organisatorischeeenheid-detail",
            kwargs={"id": str(organisatorische_eenheid.id)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["omschrijving"], "omschrijving")
        self.assertEqual(data["emailadres"], "example@email.com")
        self.assertEqual(data["faxnummer"], "7762323")
        self.assertEqual(data["telefoonnummer"], "7762323")

        data = {
            "actor": {"uuid": str(actor2.uuid)},
            "omschrijving": "changed",
            "emailadres": "changed@email.com",
            "faxnummer": "5551212",
            "telefoonnummer": "5551212",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor2.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
            },
        )
        self.assertEqual(data["omschrijving"], "changed")
        self.assertEqual(data["emailadres"], "changed@email.com")
        self.assertEqual(data["faxnummer"], "5551212")
        self.assertEqual(data["telefoonnummer"], "5551212")

        # TODO: write subtest test to test if actor's unique is true validation works propperly

    def test_partial_update_organisatorische_eenheid(self):
        actor = ActorFactory.create()
        organisatorische_eenheid = OrganisatorischeEenheidFactory.create(
            actor=actor,
            omschrijving="omschrijving",
            emailadres="example@email.com",
            faxnummer="7762323",
            telefoonnummer="7762323",
        )
        detail_url = reverse(
            "organisatorischeeenheid-detail",
            kwargs={"id": str(organisatorische_eenheid.id)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["omschrijving"], "omschrijving")
        self.assertEqual(data["emailadres"], "example@email.com")
        self.assertEqual(data["faxnummer"], "7762323")
        self.assertEqual(data["telefoonnummer"], "7762323")

        data = {
            "omschrijving": "changed",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["actor"],
            {
                "uuid": str(actor.uuid),
                "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
            },
        )
        self.assertEqual(data["omschrijving"], "changed")
        self.assertEqual(data["emailadres"], "example@email.com")
        self.assertEqual(data["faxnummer"], "7762323")
        self.assertEqual(data["telefoonnummer"], "7762323")

    def test_destroy_organisatorische_eenheid(self):
        organisatorische_eenheid = OrganisatorischeEenheidFactory.create()
        detail_url = reverse(
            "organisatorischeeenheid-detail",
            kwargs={"id": str(organisatorische_eenheid.id)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("organisatorischeeenheid-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
