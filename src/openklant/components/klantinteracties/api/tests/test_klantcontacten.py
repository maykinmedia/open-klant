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
    BijlageFactory,
    KlantcontactFactory,
    OnderwerpobjectFactory,
)


class KlantContactTests(JWTAuthMixin, APITestCase):
    def test_list_klantcontact(self):
        list_url = reverse("klantinteracties:klantcontact-list")
        KlantcontactFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_klantcontact(self):
        klantcontact = KlantcontactFactory.create()
        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_klantcontact(self):
        actor, actor2 = ActorFactory.create_batch(2)
        list_url = reverse("klantinteracties:klantcontact-list")
        data = {
            "gingOverOnderwerpobject": [],
            "omvatteBijlagen": [],
            "hadBetrokkene": [],
            "leideTotInterneTaken": [],
            "nummer": "1234567890",
            "kanaal": "kanaal",
            "onderwerp": "onderwerp",
            "actoren": [{"uuid": str(actor.uuid)}, {"uuid": str(actor2.uuid)}],
            "inhoud": "inhoud",
            "indicatieContactGelukt": True,
            "taal": "ndl",
            "vertrouwelijk": True,
            "plaatsgevondenOp": "2019-08-24T14:15:22Z",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["gingOverOnderwerpobject"], [])
        self.assertEqual(data["omvatteBijlagen"], [])
        self.assertEqual(data["nummer"], "1234567890")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                },
            ],
        )

    def test_create_klantcontact_with_reverse_lookup_fields(self):
        actor, actor2 = ActorFactory.create_batch(2)
        onderwerpobject = OnderwerpobjectFactory.create(klantcontact=None)
        bijlage = BijlageFactory.create(klantcontact=None)
        list_url = reverse("klantinteracties:klantcontact-list")
        data = {
            "gingOverOnderwerpobject": [
                {"uuid": str(onderwerpobject.uuid)},
            ],
            "omvatteBijlagen": [
                {"uuid": str(bijlage.uuid)},
            ],
            "hadBetrokkene": [
                {
                    "partij": [],
                    "bezoekadres": {
                        "nummeraanduidingId": "729512ab-1572-4dd7-a026-f6559db43bdc",
                        "adresregel1": "string",
                        "adresregel2": "string",
                        "adresregel3": "string",
                        "land": "1234",
                    },
                    "correspondentieadres": {
                        "nummeraanduidingId": "80e2fa71-f9bd-4748-ade4-1e125b756b8a",
                        "adresregel1": "string",
                        "adresregel2": "string",
                        "adresregel3": "string",
                        "land": "1234",
                    },
                    "contactnaam": {
                        "voorletters": "string",
                        "voornaam": "string",
                        "voorvoegselAchternaam": "string",
                        "achternaam": "12312",
                    },
                    "rol": "vertegenwoordiger",
                    "organisatienaam": "string",
                    "initiator": True,
                }
            ],
            "leideTotInterneTaken": [
                {
                    "nummer": "1273712737",
                    "gevraagdeHandeling": "string",
                    "actor": {"uuid": str(actor.uuid)},
                    "toelichting": "string",
                    "status": "te_verwerken",
                }
            ],
            "nummer": "1234567890",
            "kanaal": "kanaal",
            "onderwerp": "onderwerp",
            "actoren": [{"uuid": str(actor.uuid)}, {"uuid": str(actor2.uuid)}],
            "inhoud": "inhoud",
            "indicatieContactGelukt": True,
            "taal": "ndl",
            "vertrouwelijk": True,
            "plaatsgevondenOp": "2019-08-24T14:15:22Z",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(
            data["gingOverOnderwerpobject"],
            [
                {
                    "uuid": str(onderwerpobject.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/onderwerpobject/{str(onderwerpobject.uuid)}",
                }
            ],
        )
        self.assertEqual(
            data["omvatteBijlagen"],
            [
                {
                    "uuid": str(bijlage.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/bijlage/{str(bijlage.uuid)}",
                },
            ],
        )
        self.assertTrue(data["hadBetrokkene"])
        self.assertTrue(data["leideTotInterneTaken"])
        self.assertEqual(data["nummer"], "1234567890")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                },
            ],
        )

        with self.subTest("test_ging_over_onderwerp_unique"):
            data = {
                "gingOverOnderwerpobject": [
                    {"uuid": str(onderwerpobject.uuid)},
                ],
                "omvatteBijlagen": [],
                "hadBetrokkene": [],
                "leideTotInterneTaken": [],
                "nummer": "1234567890",
                "kanaal": "kanaal",
                "onderwerp": "onderwerp",
                "actoren": [],
                "inhoud": "inhoud",
                "indicatieContactGelukt": True,
                "taal": "ndl",
                "vertrouwelijk": True,
                "plaatsgevondenOp": "2019-08-24T14:15:22Z",
            }
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(
                data["invalidParams"][0]["name"], "gingOverOnderwerpobject.0.uuid"
            )

        with self.subTest("test_bijlage_unique"):
            data = {
                "gingOverOnderwerpobject": [],
                "omvatteBijlagen": [
                    {"uuid": str(bijlage.uuid)},
                ],
                "hadBetrokkene": [],
                "leideTotInterneTaken": [],
                "nummer": "1234567890",
                "kanaal": "kanaal",
                "onderwerp": "onderwerp",
                "actoren": [],
                "inhoud": "inhoud",
                "indicatieContactGelukt": True,
                "taal": "ndl",
                "vertrouwelijk": True,
                "plaatsgevondenOp": "2019-08-24T14:15:22Z",
            }
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(data["invalidParams"][0]["name"], "omvatteBijlagen.0.uuid")

    def test_update_klantcontact(self):
        actor, actor2, actor3, actor4 = ActorFactory.create_batch(4)
        klantcontact = KlantcontactFactory.create(
            nummer="1234567890",
            kanaal="kanaal",
            onderwerp="onderwerp",
            actoren=[actor, actor2],
            inhoud="inhoud",
            indicatie_contact_gelukt=True,
            taal="ndl",
            vertrouwelijk=True,
            plaatsgevonden_op="2019-08-24T14:15:22Z",
        )
        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["nummer"], "1234567890")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                },
            ],
        )

        data = {
            "gingOverOnderwerpobject": [],
            "omvatteBijlagen": [],
            "nummer": "7948723947",
            "kanaal": "changed",
            "onderwerp": "changed",
            "actoren": [{"uuid": str(actor3.uuid)}, {"uuid": str(actor4.uuid)}],
            "inhoud": "changed",
            "indicatieContactGelukt": False,
            "taal": "de",
            "vertrouwelijk": False,
            "plaatsgevondenOp": "2020-08-24T14:15:22Z",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["gingOverOnderwerpobject"], [])
        self.assertEqual(data["omvatteBijlagen"], [])
        self.assertEqual(data["nummer"], "7948723947")
        self.assertEqual(data["kanaal"], "changed")
        self.assertEqual(data["onderwerp"], "changed")
        self.assertEqual(data["inhoud"], "changed")
        self.assertEqual(data["taal"], "de")
        self.assertEqual(data["plaatsgevondenOp"], "2020-08-24T14:15:22Z")
        self.assertFalse(data["indicatieContactGelukt"])
        self.assertFalse(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor3.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor3.uuid)}",
                },
                {
                    "uuid": str(actor4.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor4.uuid)}",
                },
            ],
        )

    def test_update_klantcontact_with_reverse_lookup_fields(self):
        actor, actor2, actor3, actor4 = ActorFactory.create_batch(4)
        klantcontact = KlantcontactFactory.create(
            nummer="1234567890",
            kanaal="kanaal",
            onderwerp="onderwerp",
            actoren=[actor, actor2],
            inhoud="inhoud",
            indicatie_contact_gelukt=True,
            taal="ndl",
            vertrouwelijk=True,
            plaatsgevonden_op="2019-08-24T14:15:22Z",
        )
        onderwerpobject = OnderwerpobjectFactory.create(klantcontact=klantcontact)
        onderwerpobject2 = OnderwerpobjectFactory.create(klantcontact=None)

        bijlage = BijlageFactory.create(klantcontact=klantcontact)
        bijlage2 = BijlageFactory.create(klantcontact=None)

        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["gingOverOnderwerpobject"][0]["uuid"], str(onderwerpobject.uuid)
        )
        self.assertEqual(data["omvatteBijlagen"][0]["uuid"], str(bijlage.uuid))
        self.assertEqual(data["nummer"], "1234567890")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                },
            ],
        )

        data = {
            "gingOverOnderwerpobject": [
                {"uuid": str(onderwerpobject2.uuid)},
            ],
            "omvatteBijlagen": [
                {"uuid": str(bijlage2.uuid)},
            ],
            "nummer": "7948723947",
            "kanaal": "changed",
            "onderwerp": "changed",
            "actoren": [{"uuid": str(actor3.uuid)}, {"uuid": str(actor4.uuid)}],
            "inhoud": "changed",
            "indicatieContactGelukt": False,
            "taal": "de",
            "vertrouwelijk": False,
            "plaatsgevondenOp": "2020-08-24T14:15:22Z",
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["gingOverOnderwerpobject"],
            [
                {
                    "uuid": str(onderwerpobject2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/onderwerpobject/{str(onderwerpobject2.uuid)}",
                }
            ],
        )

        self.assertEqual(
            data["omvatteBijlagen"],
            [
                {
                    "uuid": str(bijlage2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/bijlage/{str(bijlage2.uuid)}",
                },
            ],
        )
        self.assertEqual(data["nummer"], "7948723947")
        self.assertEqual(data["kanaal"], "changed")
        self.assertEqual(data["onderwerp"], "changed")
        self.assertEqual(data["inhoud"], "changed")
        self.assertEqual(data["taal"], "de")
        self.assertEqual(data["plaatsgevondenOp"], "2020-08-24T14:15:22Z")
        self.assertFalse(data["indicatieContactGelukt"])
        self.assertFalse(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor3.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor3.uuid)}",
                },
                {
                    "uuid": str(actor4.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor4.uuid)}",
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
            taal="ndl",
            vertrouwelijk=True,
            plaatsgevonden_op="2019-08-24T14:15:22Z",
        )
        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["gingOverOnderwerpobject"], [])
        self.assertEqual(data["omvatteBijlagen"], [])
        self.assertEqual(data["nummer"], "1234567890")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                },
            ],
        )

        data = {
            "nummer": "7948723947",
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["gingOverOnderwerpobject"], [])
        self.assertEqual(data["omvatteBijlagen"], [])
        self.assertEqual(data["nummer"], "7948723947")
        self.assertEqual(data["kanaal"], "kanaal")
        self.assertEqual(data["onderwerp"], "onderwerp")
        self.assertEqual(data["inhoud"], "inhoud")
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])
        self.assertEqual(
            data["actoren"],
            [
                {
                    "uuid": str(actor.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                },
                {
                    "uuid": str(actor2.uuid),
                    "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor2.uuid)}",
                },
            ],
        )

    def test_destroy_klantcontact(self):
        klantcontact = KlantcontactFactory.create()
        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:klantcontact-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class BetrokkeneTests(JWTAuthMixin, APITestCase):
    def test_list_betrokkene(self):
        list_url = reverse("klantinteracties:betrokkene-list")
        BetrokkeneFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_betrokkene(self):
        klantcontact = BetrokkeneFactory.create()
        detail_url = reverse(
            "klantinteracties:betrokkene-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_betrokkene_with_partij(self):
        klantcontact = KlantcontactFactory.create()
        digitaal_adres = DigitaalAdresFactory.create()
        list_url = reverse("klantinteracties:betrokkene-list")
        data = {
            "klantcontact": {"uuid": str(klantcontact.uuid)},
            "partij": [
                {
                    "nummer": "8123818238",
                    "interneNotitie": "test123",
                    "digitaalAdres": {
                        "uuid": str(digitaal_adres.uuid),
                    },
                    "voorkeursDigitaalAdres": None,
                    "vertegenwoordigde": [],
                    "soortPartij": "persoon",
                    "indicatieGeheimhouding": False,
                    "voorkeurstaal": "ndl",
                    "indicatieActief": True,
                    "bezoekadres": {
                        "nummeraanduidingId": "",
                        "adresregel1": "",
                        "adresregel2": "",
                        "adresregel3": "",
                        "land": "",
                    },
                    "correspondentieadres": {
                        "nummeraanduidingId": "",
                        "adresregel1": "",
                        "adresregel2": "",
                        "adresregel3": "",
                        "land": "",
                    },
                }
            ],
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

        self.assertEqual(data["partij"][0]["nummer"], "8123818238")
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

    def test_create_betrokkene(self):
        klantcontact = KlantcontactFactory.create()
        list_url = reverse("klantinteracties:betrokkene-list")
        data = {
            "klantcontact": {"uuid": str(klantcontact.uuid)},
            "partij": [],
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

    def test_update_betrokkene(self):
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        betrokkene = BetrokkeneFactory.create(
            klantcontact=klantcontact,
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
        detail_url = reverse(
            "klantinteracties:betrokkene-detail", kwargs={"uuid": str(betrokkene.uuid)}
        )
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

        data = {
            "klantcontact": {"uuid": str(klantcontact2.uuid)},
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

    def test_partial_update_betrokkene(self):
        klantcontact = KlantcontactFactory.create()
        betrokkene = BetrokkeneFactory.create(
            klantcontact=klantcontact,
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
        detail_url = reverse(
            "klantinteracties:betrokkene-detail", kwargs={"uuid": str(betrokkene.uuid)}
        )
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

    def test_destroy_betrokkene(self):
        betrokkene = BetrokkeneFactory.create()
        detail_url = reverse(
            "klantinteracties:betrokkene-detail", kwargs={"uuid": str(betrokkene.uuid)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:betrokkene-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class BijlageTests(JWTAuthMixin, APITestCase):
    def test_list_bijlage(self):
        list_url = reverse("klantinteracties:bijlage-list")
        BijlageFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_bijlage(self):
        bijlage = BijlageFactory.create()
        detail_url = reverse(
            "klantinteracties:bijlage-detail", kwargs={"uuid": str(bijlage.uuid)}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_bijlage(self):
        list_url = reverse("klantinteracties:bijlage-list")
        data = {
            "klantcontact": None,
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

        self.assertEqual(data["klantcontact"], None)
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

        with self.subTest("create_bijlage_with_klantcontact"):
            klantcontact = KlantcontactFactory.create()
            data = {
                "klantcontact": {"uuid": str(klantcontact.uuid)},
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

            self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
            self.assertEqual(
                data["objectidentificator"],
                {
                    "objecttype": "objecttype",
                    "soortObjectId": "soortObjectId",
                    "objectId": "objectId",
                    "register": "register",
                },
            )

    def test_update_bijlage(self):
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        bijlage = BijlageFactory.create(
            klantcontact=klantcontact,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        detail_url = reverse(
            "klantinteracties:bijlage-detail", kwargs={"uuid": str(bijlage.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
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
            "klantcontact": {"uuid": str(klantcontact2.uuid)},
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

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact2.uuid))
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        )

        with self.subTest("unset_klantcontact"):
            data = {
                "klantcontact": None,
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

            self.assertIsNone(data["klantcontact"])
            self.assertEqual(
                data["objectidentificator"],
                {
                    "objecttype": "changed",
                    "soortObjectId": "changed",
                    "objectId": "changed",
                    "register": "changed",
                },
            )

    def test_partial_update_bijlage(self):
        klantcontact = KlantcontactFactory.create()
        bijlage = BijlageFactory.create(
            klantcontact=klantcontact,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        detail_url = reverse(
            "klantinteracties:bijlage-detail", kwargs={"uuid": str(bijlage.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
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
            "objectidentificator": {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        )

    def test_destroy_bijlage(self):
        bijlage = BijlageFactory.create()
        detail_url = reverse(
            "klantinteracties:bijlage-detail", kwargs={"uuid": str(bijlage.uuid)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:bijlage-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class OnderwerpobjectTests(JWTAuthMixin, APITestCase):
    def test_list_onderwerpobject(self):
        list_url = reverse("klantinteracties:onderwerpobject-list")
        OnderwerpobjectFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_onderwerpobject(self):
        onderwerpobject = OnderwerpobjectFactory.create()
        detail_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_onderwerpobject(self):
        list_url = reverse("klantinteracties:onderwerpobject-list")
        data = {
            "klantcontact": None,
            "wasKlantcontact": None,
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

        self.assertEqual(data["klantcontact"], None)
        self.assertEqual(data["wasKlantcontact"], None)
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "objecttype",
                "soortObjectId": "soortObjectId",
                "objectId": "objectId",
                "register": "register",
            },
        )

        with self.subTest("create_onderwerpobject_with_klantcontact"):
            klantcontact2 = KlantcontactFactory.create()
            data = {
                "klantcontact": {"uuid": str(klantcontact2.uuid)},
                "wasKlantcontact": None,
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

            self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact2.uuid))
            self.assertIsNone(data["wasKlantcontact"])
            self.assertEqual(
                data["objectidentificator"],
                {
                    "objecttype": "objecttype",
                    "soortObjectId": "soortObjectId",
                    "objectId": "objectId",
                    "register": "register",
                },
            )

        with self.subTest("create_onderwerpobject_with_was_klantcontact"):
            klantcontact3 = KlantcontactFactory.create()
            data = {
                "klantcontact": None,
                "wasKlantcontact": {"uuid": str(klantcontact3.uuid)},
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

            self.assertIsNone(data["klantcontact"])
            self.assertEqual(data["wasKlantcontact"]["uuid"], str(klantcontact3.uuid))
            self.assertEqual(
                data["objectidentificator"],
                {
                    "objecttype": "objecttype",
                    "soortObjectId": "soortObjectId",
                    "objectId": "objectId",
                    "register": "register",
                },
            )

    def test_update_onderwerpobject(self):
        (
            klantcontact,
            klantcontact2,
            klantcontact3,
            klantcontact4,
        ) = KlantcontactFactory.create_batch(4)
        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=klantcontact3,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        detail_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(data["wasKlantcontact"]["uuid"], str(klantcontact3.uuid))
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
            "klantcontact": {"uuid": str(klantcontact2.uuid)},
            "wasKlantcontact": {"uuid": str(klantcontact4.uuid)},
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

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact2.uuid))
        self.assertEqual(data["wasKlantcontact"]["uuid"], str(klantcontact4.uuid))
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        )

        with self.subTest("unset_klantcontact"):
            data = {
                "klantcontact": None,
                "wasKlantcontact": None,
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

            self.assertIsNone(data["klantcontact"])
            self.assertIsNone(data["wasKlantcontact"])
            self.assertEqual(
                data["objectidentificator"],
                {
                    "objecttype": "changed",
                    "soortObjectId": "changed",
                    "objectId": "changed",
                    "register": "changed",
                },
            )

    def test_partial_update_onderwerpobject(self):
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=klantcontact2,
            objectidentificator_objecttype="objecttype",
            objectidentificator_soort_object_id="soortObjectId",
            objectidentificator_object_id="objectId",
            objectidentificator_register="register",
        )
        detail_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(data["wasKlantcontact"]["uuid"], str(klantcontact2.uuid))
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
            "objectidentificator": {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(data["wasKlantcontact"]["uuid"], str(klantcontact2.uuid))
        self.assertEqual(
            data["objectidentificator"],
            {
                "objecttype": "changed",
                "soortObjectId": "changed",
                "objectId": "changed",
                "register": "changed",
            },
        )

    def test_destroy_onderwerpobject(self):
        onderwerpobject = OnderwerpobjectFactory.create()
        detail_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:onderwerpobject-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)
