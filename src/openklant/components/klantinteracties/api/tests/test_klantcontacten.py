from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
)
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
    KlantcontactFactory,
)


class KlantContactTests(JWTAuthMixin, APITestCase):
    def test_list_klantcontact(self):
        list_url = reverse("klantcontact-list")
        KlantcontactFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_klantcontact(self):
        klantcontact = KlantcontactFactory.create()
        detail_url = reverse(
            "klantcontact-detail", kwargs={"uuid": str(klantcontact.uuid)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_klantcontact(self):
        actor, actor2 = ActorFactory.create_batch(2)
        list_url = reverse("klantcontact-list")
        data = {
            "nummer": "1234567890",
            "kanaal": "kanaal",
            "onderwerp": "onderwerp",
            "actoren": [{"uuid": str(actor.uuid)}, {"uuid": str(actor2.uuid)}],
            "inhoud": "inhoud",
            "indicatieContactGelukt": True,
            "taal": "taal",
            "vertrouwelijk": True,
            "plaatsgevondenOp": "2019-08-24T14:15:22Z",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["nummer"], "1234567890")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "taal")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                    "naam": str(actor.naam),
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                    "naam": str(actor2.naam),
                },
            ],
        )

    def test_update_klantcontact(self):
        actor, actor2, actor3, actor4 = ActorFactory.create_batch(4)
        klantcontact = KlantcontactFactory.create(
            nummer="1234567890",
            kanaal="kanaal",
            onderwerp="onderwerp",
            actoren=[actor, actor2],
            inhoud="inhoud",
            indicatie_contact_gelukt=True,
            taal="taal",
            vertrouwelijk=True,
            plaatsgevonden_op="2019-08-24T14:15:22Z",
        )
        detail_url = reverse(
            "klantcontact-detail", kwargs={"uuid": str(klantcontact.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1234567890")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "taal")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                    "naam": str(actor.naam),
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                    "naam": str(actor2.naam),
                },
            ],
        )

        data = {
            "nummer": "7948723947",
            "kanaal": "changed",
            "onderwerp": "changed",
            "actoren": [{"uuid": str(actor3.uuid)}, {"uuid": str(actor4.uuid)}],
            "inhoud": "changed",
            "indicatieContactGelukt": False,
            "taal": "changed",
            "vertrouwelijk": False,
            "plaatsgevondenOp": "2020-08-24T14:15:22Z",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["nummer"], "7948723947")
        self.assertEqual(data["kanaal"], "changed")
        self.assertEqual(data["onderwerp"], "changed")
        self.assertEqual(data["inhoud"], "changed")
        self.assertEqual(data["taal"], "changed")
        self.assertEqual(data["plaatsgevondenOp"], "2020-08-24T14:15:22Z")
        self.assertFalse(data["indicatieContactGelukt"])
        self.assertFalse(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor3.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor3.uuid)}",
                    "naam": str(actor3.naam),
                },
                {
                    "uuid": str(actor4.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor4.uuid)}",
                    "naam": str(actor4.naam),
                },
            ],
        )

    def test_partial_update_klantcontact(self):
        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact = KlantcontactFactory.create(
            nummer="1234567890",
            kanaal="kanaal",
            onderwerp="onderwerp",
            actoren=[actor, actor2],
            inhoud="inhoud",
            indicatie_contact_gelukt=True,
            taal="taal",
            vertrouwelijk=True,
            plaatsgevonden_op="2019-08-24T14:15:22Z",
        )
        detail_url = reverse(
            "klantcontact-detail", kwargs={"uuid": str(klantcontact.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1234567890")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "taal")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                    "naam": str(actor.naam),
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                    "naam": str(actor2.naam),
                },
            ],
        )

        data = {
            "nummer": "7948723947",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["nummer"], "7948723947")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "taal")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                    "naam": str(actor.naam),
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                    "naam": str(actor2.naam),
                },
            ],
        )

    def test_destroy_klantcontact(self):
        klantcontact = KlantcontactFactory.create()
        detail_url = reverse(
            "klantcontact-detail", kwargs={"uuid": str(klantcontact.uuid)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantcontact-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class BetrokkeneTests(JWTAuthMixin, APITestCase):
    def test_list_betrokkene(self):
        list_url = reverse("betrokkene-list")
        BetrokkeneFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_betrokkene(self):
        klantcontact = BetrokkeneFactory.create()
        detail_url = reverse(
            "betrokkene-detail", kwargs={"uuid": str(klantcontact.uuid)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_betrokkene(self):
        klantcontact = KlantcontactFactory.create()
        digitaal_adres = DigitaalAdresFactory.create()
        list_url = reverse("betrokkene-list")
        data = {
            "klantcontact": {"uuid": str(klantcontact.uuid)},
            "digitaalAdres": {"uuid": str(digitaal_adres.uuid)},
            "bezoekadres": {
                "nummeraanduidingId": "4a282b5c-16d7-401d-9737-28e98c865ab2",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "c06918d9-899b-4d98-a10d-08436ebc6c20",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
            "contactnaam": {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
            "rol": "vertegenwoordiger",
            "organisatienaam": "Whitechapel",
            "initiator": True,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "4a282b5c-16d7-401d-9737-28e98c865ab2",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "c06918d9-899b-4d98-a10d-08436ebc6c20",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres.uuid))

    def test_update_betrokkene(self):
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        digitaal_adres, digitaal_adres2 = DigitaalAdresFactory.create_batch(2)
        betrokkene = BetrokkeneFactory.create(
            klantcontact=klantcontact,
            digitaal_adres=digitaal_adres,
            bezoekadres_nummeraanduiding_id="4a282b5c-16d7-401d-9737-28e98c865ab2",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="6030",
            correspondentieadres_nummeraanduiding_id="c06918d9-899b-4d98-a10d-08436ebc6c20",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="6030",
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
            rol="vertegenwoordiger",
            organisatienaam="Whitechapel",
            initiator=True,
        )
        detail_url = reverse("betrokkene-detail", kwargs={"uuid": str(betrokkene.uuid)})
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "4a282b5c-16d7-401d-9737-28e98c865ab2",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "c06918d9-899b-4d98-a10d-08436ebc6c20",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres.uuid))

        data = {
            "klantcontact": {"uuid": str(klantcontact2.uuid)},
            "digitaalAdres": {"uuid": str(digitaal_adres2.uuid)},
            "bezoekadres": {
                "nummeraanduidingId": "4a282b5c-16d7-401d-9737-28e98c865ab2",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "c06918d9-899b-4d98-a10d-08436ebc6c20",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
            "contactnaam": {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
            "rol": "klant",
            "organisatienaam": "changed",
            "initiator": False,
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "4a282b5c-16d7-401d-9737-28e98c865ab2",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "c06918d9-899b-4d98-a10d-08436ebc6c20",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
        )
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "changed",
                "voornaam": "changed",
                "voorvoegselAchternaam": "changed",
                "achternaam": "changed",
            },
        )
        self.assertEqual(data["rol"], "klant")
        self.assertEqual(data["organisatienaam"], "changed")
        self.assertFalse(data["initiator"])
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact2.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres2.uuid))

    def test_partial_update_betrokkene(self):
        klantcontact = KlantcontactFactory.create()
        digitaal_adres = DigitaalAdresFactory.create()
        betrokkene = BetrokkeneFactory.create(
            klantcontact=klantcontact,
            digitaal_adres=digitaal_adres,
            bezoekadres_nummeraanduiding_id="4a282b5c-16d7-401d-9737-28e98c865ab2",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="6030",
            correspondentieadres_nummeraanduiding_id="c06918d9-899b-4d98-a10d-08436ebc6c20",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="6030",
            contactnaam_voorletters="P",
            contactnaam_voornaam="Phil",
            contactnaam_voorvoegsel_achternaam="",
            contactnaam_achternaam="Bozeman",
            rol="vertegenwoordiger",
            organisatienaam="Whitechapel",
            initiator=True,
        )
        detail_url = reverse("betrokkene-detail", kwargs={"uuid": str(betrokkene.uuid)})
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "4a282b5c-16d7-401d-9737-28e98c865ab2",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "c06918d9-899b-4d98-a10d-08436ebc6c20",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres.uuid))

        data = {
            "bezoekadres": {
                "nummeraanduidingId": "4a282b5c-16d7-401d-9737-28e98c865ab2",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "4a282b5c-16d7-401d-9737-28e98c865ab2",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "3060",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "c06918d9-899b-4d98-a10d-08436ebc6c20",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "6030",
            },
        )
        self.assertEqual(
            data["contactnaam"],
            {
                "voorletters": "P",
                "voornaam": "Phil",
                "voorvoegselAchternaam": "",
                "achternaam": "Bozeman",
            },
        )
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(data["digitaalAdres"]["uuid"], str(digitaal_adres.uuid))

    def test_destroy_betrokkene(self):
        betrokkene = BetrokkeneFactory.create()
        detail_url = reverse("betrokkene-detail", kwargs={"uuid": str(betrokkene.uuid)})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("betrokkene-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
