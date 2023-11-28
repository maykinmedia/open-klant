from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
    GeautomatiseerdeActorFactory,
    MedewerkerFactory,
    OrganisatorischeEenheidFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class ActorTests(APITestCase):
    def test_list_actor(self):
        list_url = reverse("klantinteracties:actor-list")
        ActorFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_actor(self):
        actor = ActorFactory.create()
        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_actor_medewerker(self):
        list_url = reverse("klantinteracties:actor-list")
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
            "actorIdentificatie": {
                "functie": "functie",
                "emailadres": "phil@bozeman.com",
                "telefoonnummer": "3168234723",
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "functie",
                "emailadres": "phil@bozeman.com",
                "telefoonnummer": "3168234723",
            },
        )

    def test_create_actor_organisatorische_eenheid(self):
        list_url = reverse("klantinteracties:actor-list")
        data = {
            "naam": "Phil",
            "soortActor": "organisatorische_eenheid",
            "indicatieActief": True,
            "objectidentificator": {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
            "actorIdentificatie": {
                "omschrijving": "omschrijving",
                "emailadres": "phil@bozeman.com",
                "faxnummer": "316893487573",
                "telefoonnummer": "3168234723",
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["naam"], "Phil")
        self.assertEqual(data["soortActor"], "organisatorische_eenheid")
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "omschrijving": "omschrijving",
                "emailadres": "phil@bozeman.com",
                "faxnummer": "316893487573",
                "telefoonnummer": "3168234723",
            },
        )

    def test_create_actor_geautomatiseerde_actor(self):
        list_url = reverse("klantinteracties:actor-list")
        data = {
            "naam": "Phil",
            "soortActor": "geautomatiseerde_actor",
            "indicatieActief": True,
            "objectidentificator": {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
            "actorIdentificatie": {
                "functie": "functie",
                "omschrijving": "omschrijving",
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["naam"], "Phil")
        self.assertEqual(data["soortActor"], "geautomatiseerde_actor")
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "functie",
                "omschrijving": "omschrijving",
            },
        )

    def test_update_actor_medewerker(self):
        actor = ActorFactory.create(
            naam="Phil",
            soort_actor="medewerker",
            indicatie_actief=True,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        MedewerkerFactory.create(
            actor=actor,
            functie="functie",
            emailadres="phil@bozeman.com",
            telefoonnummer="3168234723",
        )

        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "functie",
                "emailadres": "phil@bozeman.com",
                "telefoonnummer": "3168234723",
            },
        )

        data = {
            "naam": "changed",
            "soortActor": "medewerker",
            "indicatieActief": False,
            "objectidentificator": {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
            "actorIdentificatie": {
                "functie": "vocalist",
                "emailadres": "phil@whitechapel.com",
                "telefoonnummer": "315834573",
            },
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["naam"], "changed")
        self.assertEqual(data["soortActor"], "medewerker")
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "vocalist",
                "emailadres": "phil@whitechapel.com",
                "telefoonnummer": "315834573",
            },
        )

    def test_update_actor_organisatorische_eenheid(self):
        actor = ActorFactory.create(
            naam="Phil",
            soort_actor="organisatorische_eenheid",
            indicatie_actief=True,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        OrganisatorischeEenheidFactory.create(
            actor=actor,
            omschrijving="omschrijving",
            emailadres="phil@bozeman.com",
            faxnummer="316893487573",
            telefoonnummer="3168234723",
        )

        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["naam"], "Phil")
        self.assertEqual(data["soortActor"], "organisatorische_eenheid")
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "omschrijving": "omschrijving",
                "emailadres": "phil@bozeman.com",
                "faxnummer": "316893487573",
                "telefoonnummer": "3168234723",
            },
        )

        data = {
            "naam": "changed",
            "soortActor": "organisatorische_eenheid",
            "indicatieActief": False,
            "objectidentificator": {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
            "actorIdentificatie": {
                "omschrijving": "changed",
                "emailadres": "phil@whitechapel.com",
                "faxnummer": "316853458345",
                "telefoonnummer": "3169456732",
            },
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["naam"], "changed")
        self.assertEqual(data["soortActor"], "organisatorische_eenheid")
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "omschrijving": "changed",
                "emailadres": "phil@whitechapel.com",
                "faxnummer": "316853458345",
                "telefoonnummer": "3169456732",
            },
        )

    def test_update_actor_geautomatiseerde_actor(self):
        actor = ActorFactory.create(
            naam="Phil",
            soort_actor="geautomatiseerde_actor",
            indicatie_actief=True,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        GeautomatiseerdeActorFactory.create(
            actor=actor,
            functie="functie",
            omschrijving="omschrijving",
        )

        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["naam"], "Phil")
        self.assertEqual(data["soortActor"], "geautomatiseerde_actor")
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "functie",
                "omschrijving": "omschrijving",
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
            "actorIdentificatie": {
                "functie": "changed",
                "omschrijving": "changed",
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "changed",
                "omschrijving": "changed",
            },
        )

    def test_update_actor_medewerker_to_geautomatiseerde_actor(self):
        actor = ActorFactory.create(
            naam="Phil",
            soort_actor="medewerker",
            indicatie_actief=True,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        MedewerkerFactory.create(
            actor=actor,
            functie="functie",
            emailadres="phil@bozeman.com",
            telefoonnummer="3168234723",
        )

        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "functie",
                "emailadres": "phil@bozeman.com",
                "telefoonnummer": "3168234723",
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
            "actorIdentificatie": {
                "functie": "changed",
                "omschrijving": "changed",
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "changed",
                "omschrijving": "changed",
            },
        )

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
        MedewerkerFactory.create(
            actor=actor,
            functie="functie",
            emailadres="phil@bozeman.com",
            telefoonnummer="3168234723",
        )
        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "functie",
                "emailadres": "phil@bozeman.com",
                "telefoonnummer": "3168234723",
            },
        )

        data = {
            "soortActor": "medewerker",
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
        self.assertEqual(
            data["actorIdentificatie"],
            {
                "functie": "functie",
                "emailadres": "phil@bozeman.com",
                "telefoonnummer": "3168234723",
            },
        )

    def test_destroy_actor(self):
        actor = ActorFactory.create()
        detail_url = reverse(
            "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:actor-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
