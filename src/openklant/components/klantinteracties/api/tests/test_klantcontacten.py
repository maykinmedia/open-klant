from django.utils.translation import gettext as _

from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models import (
    Betrokkene,
    Klantcontact,
    Onderwerpobject,
)
from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    ActorKlantcontactFactory,
    BetrokkeneFactory,
    BijlageFactory,
    DigitaalAdresFactory,
    KlantcontactFactory,
    MedewerkerFactory,
    OnderwerpobjectFactory,
    PartijFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase

from .factories import (
    BetrokkeneDataFactory,
    KlantContactDataFactory,
    OnderwerpObjectDataFactory,
)


class KlantContactTests(APITestCase):
    def test_list_klantcontact(self):
        list_url = reverse("klantinteracties:klantcontact-list")
        KlantcontactFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

        with self.subTest("test_empty_had_betrokken_actoren"):
            self.assertEqual(data["results"][0]["hadBetrokkenActoren"], [])
            self.assertEqual(data["results"][1]["hadBetrokkenActoren"], [])

    def test_list_filters(self):
        list_url = reverse("klantinteracties:onderwerpobject-list")
        OnderwerpobjectFactory.create(
            klantcontact=KlantcontactFactory.create(),
            onderwerpobjectidentificator_code_objecttype="codeObjecttype",
            onderwerpobjectidentificator_code_soort_object_id="codeSoortObjectId",
            onderwerpobjectidentificator_object_id="objectId",
            onderwerpobjectidentificator_code_register="codeRegister",
        )
        OnderwerpobjectFactory.create(
            klantcontact=KlantcontactFactory.create(),
            onderwerpobjectidentificator_code_objecttype="codeObjecttype_test",
            onderwerpobjectidentificator_code_soort_object_id="codeSoortObjectId_test",
            onderwerpobjectidentificator_object_id="objectId_test",
            onderwerpobjectidentificator_code_register="codeRegister_test",
        )
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["results"]), 2)

        with self.subTest("onderwerpobjectidentificatorCodeSoortObjectId filter"):
            response = self.client.get(
                list_url,
                {"onderwerpobjectidentificatorCodeSoortObjectId": "codeSoortObjectId"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(len(data["results"]), 1)
            self.assertEqual(
                data["results"][0]["onderwerpobjectidentificator"]["codeSoortObjectId"],
                "codeSoortObjectId",
            )

            response = self.client.get(
                list_url,
                {
                    "onderwerpobjectidentificatorCodeSoortObjectId": "codeSoortObjectId_test"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(len(data["results"]), 1)
            self.assertEqual(
                data["results"][0]["onderwerpobjectidentificator"]["codeSoortObjectId"],
                "codeSoortObjectId_test",
            )

            response = self.client.get(
                list_url,
                {"onderwerpobjectidentificatorCodeSoortObjectId": "test"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(len(data["results"]), 0)

    def test_list_pagination_pagesize_param(self):
        list_url = reverse("klantinteracties:klantcontact-list")
        KlantcontactFactory.create_batch(10)

        response = self.client.get(list_url, {"pageSize": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 10)
        self.assertEqual(len(data["results"]), 5)
        self.assertEqual(data["next"], f"http://testserver{list_url}?page=2&pageSize=5")

    def test_read_klantcontact(self):
        actor = ActorFactory.create(
            naam="Phil",
            soort_actor="medewerker",
            indicatie_actief=True,
            actoridentificator_code_objecttype="codeObjecttype",
            actoridentificator_code_soort_object_id="codeSoortObjectId",
            actoridentificator_object_id="objectId",
            actoridentificator_code_register="codeRegister",
        )
        MedewerkerFactory.create(
            actor=actor,
            functie="functie",
            emailadres="phil@bozeman.com",
            telefoonnummer="+31618234723",
        )
        klantcontact = KlantcontactFactory.create()
        ActorKlantcontactFactory.create(actor=actor, klantcontact=klantcontact)
        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

        with self.subTest("test_had_betrokken_actoren"):
            data = response.json()
            self.assertEqual(
                data["hadBetrokkenActoren"],
                [
                    {
                        "uuid": str(actor.uuid),
                        "url": f"http://testserver/klantinteracties/api/v1/actoren/{str(actor.uuid)}",
                        "naam": "Phil",
                        "soortActor": "medewerker",
                        "indicatieActief": True,
                        "actoridentificator": {
                            "codeObjecttype": "codeObjecttype",
                            "codeSoortObjectId": "codeSoortObjectId",
                            "objectId": "objectId",
                            "codeRegister": "codeRegister",
                        },
                        "actorIdentificatie": {
                            "functie": "functie",
                            "emailadres": "phil@bozeman.com",
                            "telefoonnummer": "+31618234723",
                        },
                    }
                ],
            )

    def test_create_klantcontact(self):
        list_url = reverse("klantinteracties:klantcontact-list")
        data = {
            "nummer": "1234567890",
            "kanaal": "kanaal",
            "onderwerp": "onderwerp",
            "inhoud": "inhoud",
            "indicatieContactGelukt": True,
            "taal": "ndl",
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
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])

        with self.subTest("auto_generate_max_nummer_plus_one"):
            data["nummer"] = ""
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = response.json()
            self.assertEqual(response_data["nummer"], "1234567891")

        with self.subTest("auto_generate_nummer_unique_validation"):
            data["nummer"] = "1234567891"
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(
                response_data["invalidParams"][0]["reason"],
                "Er bestaat al een klantcontact met eenzelfde nummer.",
            )

        with self.subTest("auto_generate_nummer_over_10_characters_error_message"):
            KlantcontactFactory.create(nummer="9999999999")
            data["nummer"] = ""
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
            response_data = response.json()
            self.assertEqual(
                response_data["detail"],
                "Er kon niet automatisch een opvolgend nummer worden gegenereerd. "
                "Het maximaal aantal tekens is bereikt.",
            )

    def test_create_klantcontact_with_reverse_lookup_fields(self):
        list_url = reverse("klantinteracties:klantcontact-list")
        data = {
            "nummer": "1234567890",
            "kanaal": "kanaal",
            "onderwerp": "onderwerp",
            "inhoud": "inhoud",
            "indicatieContactGelukt": True,
            "taal": "ndl",
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
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])

    def test_update_klantcontact(self):
        klantcontact = KlantcontactFactory.create(
            nummer="1234567890",
            kanaal="kanaal",
            onderwerp="onderwerp",
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

        data = {
            "nummer": "7948723947",
            "kanaal": "changed",
            "onderwerp": "changed",
            "inhoud": "changed",
            "indicatieContactGelukt": False,
            "taal": "de",
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
        self.assertEqual(data["taal"], "de")
        self.assertEqual(data["plaatsgevondenOp"], "2020-08-24T14:15:22Z")
        self.assertFalse(data["indicatieContactGelukt"])
        self.assertFalse(data["vertrouwelijk"])

    def test_update_klantcontact_with_reverse_lookup_fields(self):
        klantcontact = KlantcontactFactory.create(
            nummer="1234567890",
            kanaal="kanaal",
            onderwerp="onderwerp",
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

        data = {
            "nummer": "7948723947",
            "kanaal": "changed",
            "onderwerp": "changed",
            "inhoud": "changed",
            "indicatieContactGelukt": False,
            "taal": "de",
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
        self.assertEqual(data["taal"], "de")
        self.assertEqual(data["plaatsgevondenOp"], "2020-08-24T14:15:22Z")
        self.assertFalse(data["indicatieContactGelukt"])
        self.assertFalse(data["vertrouwelijk"])

    def test_partial_update_klantcontact(self):
        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact = KlantcontactFactory.create(
            nummer="1234567890",
            kanaal="kanaal",
            onderwerp="onderwerp",
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
        self.assertEqual(data["taal"], "ndl")
        self.assertEqual(data["plaatsgevondenOp"], "2019-08-24T14:15:22Z")
        self.assertTrue(data["indicatieContactGelukt"])
        self.assertTrue(data["vertrouwelijk"])

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


class BetrokkeneTests(APITestCase):
    def test_list_betrokkene(self):
        list_url = reverse("klantinteracties:betrokkene-list")
        BetrokkeneFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_betrokkene(self):
        betrokkene = BetrokkeneFactory.create()
        detail_url = reverse(
            "klantinteracties:betrokkene-detail",
            kwargs={"uuid": str(betrokkene.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

        with self.subTest("test_expand_digitale_adressen"):
            digitaal_adres = DigitaalAdresFactory(
                betrokkene=betrokkene,
                adres="test",
                soort_digitaal_adres="email",
            )
            response = self.client.get(detail_url, data={"expand": "digitaleAdressen"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            digitaal_adressen = data["_expand"]["digitaleAdressen"]
            self.assertEqual(len(digitaal_adressen), 1)
            self.assertEqual(digitaal_adressen[0]["uuid"], str(digitaal_adres.uuid))
            self.assertEqual(
                digitaal_adressen[0]["verstrektDoorBetrokkene"]["uuid"],
                str(betrokkene.uuid),
            )

    def test_create_betrokkene_with_partij(self):
        klantcontact = KlantcontactFactory.create()
        partij = PartijFactory.create()
        list_url = reverse("klantinteracties:betrokkene-list")
        data = {
            "hadKlantcontact": {"uuid": str(klantcontact.uuid)},
            "wasPartij": {"uuid": str(partij.uuid)},
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
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

        self.assertEqual(data["wasPartij"]["uuid"], str(partij.uuid))
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
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
        self.assertEqual(data["volledigeNaam"], "Phil Bozeman")
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["hadKlantcontact"]["uuid"], str(klantcontact.uuid))

    def test_create_betrokkene(self):
        klantcontact = KlantcontactFactory.create()
        list_url = reverse("klantinteracties:betrokkene-list")
        data = {
            "hadKlantcontact": {"uuid": str(klantcontact.uuid)},
            "wasPartij": None,
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
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

        self.assertIsNone(data["wasPartij"])
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
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
        self.assertEqual(data["volledigeNaam"], "Phil Bozeman")
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["hadKlantcontact"]["uuid"], str(klantcontact.uuid))

    def test_update_betrokkene(self):
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        partij, partij2 = PartijFactory.create_batch(2)
        betrokkene = BetrokkeneFactory.create(
            klantcontact=klantcontact,
            partij=partij,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            bezoekadres_straatnaam="straat",
            bezoekadres_huisnummer=10,
            bezoekadres_huisnummertoevoeging="A2",
            bezoekadres_postcode="1008 DG",
            bezoekadres_stad="Amsterdam",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="NL",
            correspondentieadres_nummeraanduiding_id="1234567890000002",
            correspondentieadres_straatnaam="straat",
            correspondentieadres_huisnummer=10,
            correspondentieadres_huisnummertoevoeging="A2",
            correspondentieadres_postcode="1008 DG",
            correspondentieadres_stad="Amsterdam",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="NL",
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

        self.assertEqual(data["wasPartij"]["uuid"], str(partij.uuid))
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
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
        self.assertEqual(data["volledigeNaam"], "Phil Bozeman")
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["hadKlantcontact"]["uuid"], str(klantcontact.uuid))

        data = {
            "wasPartij": {"uuid": str(partij2.uuid)},
            "hadKlantcontact": {"uuid": str(klantcontact2.uuid)},
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
            "correspondentieadres": {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
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

        self.assertEqual(data["wasPartij"]["uuid"], str(partij2.uuid))
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
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
        self.assertEqual(data["volledigeNaam"], "changed changed changed")
        self.assertEqual(data["rol"], "klant")
        self.assertEqual(data["organisatienaam"], "changed")
        self.assertFalse(data["initiator"])
        self.assertEqual(data["hadKlantcontact"]["uuid"], str(klantcontact2.uuid))

    def test_partial_update_betrokkene(self):
        klantcontact = KlantcontactFactory.create()
        partij = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create(
            klantcontact=klantcontact,
            partij=partij,
            bezoekadres_nummeraanduiding_id="1234567890000001",
            bezoekadres_straatnaam="straat",
            bezoekadres_huisnummer=10,
            bezoekadres_huisnummertoevoeging="A2",
            bezoekadres_postcode="1008 DG",
            bezoekadres_stad="Amsterdam",
            bezoekadres_adresregel1="adres1",
            bezoekadres_adresregel2="adres2",
            bezoekadres_adresregel3="adres3",
            bezoekadres_land="NL",
            correspondentieadres_nummeraanduiding_id="1234567890000002",
            correspondentieadres_straatnaam="straat",
            correspondentieadres_huisnummer=10,
            correspondentieadres_huisnummertoevoeging="A2",
            correspondentieadres_postcode="1008 DG",
            correspondentieadres_stad="Amsterdam",
            correspondentieadres_adresregel1="adres1",
            correspondentieadres_adresregel2="adres2",
            correspondentieadres_adresregel3="adres3",
            correspondentieadres_land="NL",
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

        self.assertEqual(data["wasPartij"]["uuid"], str(partij.uuid))
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
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
        self.assertEqual(data["volledigeNaam"], "Phil Bozeman")
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["hadKlantcontact"]["uuid"], str(klantcontact.uuid))

        data = {
            "bezoekadres": {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["wasPartij"]["uuid"], str(partij.uuid))
        self.assertEqual(
            data["bezoekadres"],
            {
                "nummeraanduidingId": "1234567890000001",
                "straatnaam": "changed",
                "huisnummer": 10,
                "huisnummertoevoeging": "changed",
                "postcode": "1001 AB",
                "stad": "Amsterdam",
                "adresregel1": "changed",
                "adresregel2": "changed",
                "adresregel3": "changed",
                "land": "NL",
            },
        )
        self.assertEqual(
            data["correspondentieadres"],
            {
                "nummeraanduidingId": "1234567890000002",
                "straatnaam": "straat",
                "huisnummer": 10,
                "huisnummertoevoeging": "A2",
                "postcode": "1008 DG",
                "stad": "Amsterdam",
                "adresregel1": "adres1",
                "adresregel2": "adres2",
                "adresregel3": "adres3",
                "land": "NL",
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
        self.assertEqual(data["volledigeNaam"], "Phil Bozeman")
        self.assertEqual(data["rol"], "vertegenwoordiger")
        self.assertEqual(data["organisatienaam"], "Whitechapel")
        self.assertTrue(data["initiator"])
        self.assertEqual(data["hadKlantcontact"]["uuid"], str(klantcontact.uuid))

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


class BijlageTests(APITestCase):
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
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create_bijlage(self):
        list_url = reverse("klantinteracties:bijlage-list")
        data = {
            "wasBijlageVanKlantcontact": None,
            "bijlageidentificator": {
                "codeObjecttype": "codeObjecttype",
                "codeSoortObjectId": "codeSoortObjectId",
                "objectId": "objectId",
                "codeRegister": "codeRegister",
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["wasBijlageVanKlantcontact"], None)
        self.assertEqual(
            data["bijlageidentificator"],
            {
                "codeObjecttype": "codeObjecttype",
                "codeSoortObjectId": "codeSoortObjectId",
                "objectId": "objectId",
                "codeRegister": "codeRegister",
            },
        )

        with self.subTest("create_bijlage_with_klantcontact"):
            klantcontact = KlantcontactFactory.create()
            data = {
                "wasBijlageVanKlantcontact": {"uuid": str(klantcontact.uuid)},
                "bijlageidentificator": {
                    "codeObjecttype": "codeObjecttype",
                    "codeSoortObjectId": "codeSoortObjectId",
                    "objectId": "objectId",
                    "codeRegister": "codeRegister",
                },
            }
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            data = response.json()

            self.assertEqual(
                data["wasBijlageVanKlantcontact"]["uuid"], str(klantcontact.uuid)
            )
            self.assertEqual(
                data["bijlageidentificator"],
                {
                    "codeObjecttype": "codeObjecttype",
                    "codeSoortObjectId": "codeSoortObjectId",
                    "objectId": "objectId",
                    "codeRegister": "codeRegister",
                },
            )

    def test_update_bijlage(self):
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        bijlage = BijlageFactory.create(
            klantcontact=klantcontact,
            bijlageidentificator_code_objecttype="codeObjecttype",
            bijlageidentificator_code_soort_object_id="codeSoortObjectId",
            bijlageidentificator_object_id="objectId",
            bijlageidentificator_code_register="codeRegister",
        )
        detail_url = reverse(
            "klantinteracties:bijlage-detail", kwargs={"uuid": str(bijlage.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["wasBijlageVanKlantcontact"]["uuid"], str(klantcontact.uuid)
        )
        self.assertEqual(
            data["bijlageidentificator"],
            {
                "codeObjecttype": "codeObjecttype",
                "codeSoortObjectId": "codeSoortObjectId",
                "objectId": "objectId",
                "codeRegister": "codeRegister",
            },
        )

        data = {
            "wasBijlageVanKlantcontact": {"uuid": str(klantcontact2.uuid)},
            "bijlageidentificator": {
                "codeObjecttype": "changed",
                "codeSoortObjectId": "changed",
                "objectId": "changed",
                "codeRegister": "changed",
            },
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["wasBijlageVanKlantcontact"]["uuid"], str(klantcontact2.uuid)
        )
        self.assertEqual(
            data["bijlageidentificator"],
            {
                "codeObjecttype": "changed",
                "codeSoortObjectId": "changed",
                "objectId": "changed",
                "codeRegister": "changed",
            },
        )

        with self.subTest("unset_klantcontact"):
            data = {
                "wasBijlageVanKlantcontact": None,
                "bijlageidentificator": {
                    "codeObjecttype": "changed",
                    "codeSoortObjectId": "changed",
                    "objectId": "changed",
                    "codeRegister": "changed",
                },
            }

            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertIsNone(data["wasBijlageVanKlantcontact"])
            self.assertEqual(
                data["bijlageidentificator"],
                {
                    "codeObjecttype": "changed",
                    "codeSoortObjectId": "changed",
                    "objectId": "changed",
                    "codeRegister": "changed",
                },
            )

    def test_partial_update_bijlage(self):
        klantcontact = KlantcontactFactory.create()
        bijlage = BijlageFactory.create(
            klantcontact=klantcontact,
            bijlageidentificator_code_objecttype="codeObjecttype",
            bijlageidentificator_code_soort_object_id="codeSoortObjectId",
            bijlageidentificator_object_id="objectId",
            bijlageidentificator_code_register="codeRegister",
        )
        detail_url = reverse(
            "klantinteracties:bijlage-detail", kwargs={"uuid": str(bijlage.uuid)}
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(
            data["wasBijlageVanKlantcontact"]["uuid"], str(klantcontact.uuid)
        )
        self.assertEqual(
            data["bijlageidentificator"],
            {
                "codeObjecttype": "codeObjecttype",
                "codeSoortObjectId": "codeSoortObjectId",
                "objectId": "objectId",
                "codeRegister": "codeRegister",
            },
        )

        data = {
            "bijlageidentificator": {
                "codeObjecttype": "changed",
                "codeSoortObjectId": "changed",
                "objectId": "changed",
                "codeRegister": "changed",
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data["wasBijlageVanKlantcontact"]["uuid"], str(klantcontact.uuid)
        )
        self.assertEqual(
            data["bijlageidentificator"],
            {
                "codeObjecttype": "changed",
                "codeSoortObjectId": "changed",
                "objectId": "changed",
                "codeRegister": "changed",
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


class OnderwerpobjectTests(APITestCase):
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
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create_onderwerpobject(self):
        list_url = reverse("klantinteracties:onderwerpobject-list")
        data = {
            "klantcontact": None,
            "wasKlantcontact": None,
            "onderwerpobjectidentificator": {
                "codeObjecttype": "codeObjecttype",
                "codeSoortObjectId": "codeSoortObjectId",
                "objectId": "objectId",
                "codeRegister": "codeRegister",
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data["klantcontact"], None)
        self.assertEqual(data["wasKlantcontact"], None)
        self.assertEqual(
            data["onderwerpobjectidentificator"],
            {
                "codeObjecttype": "codeObjecttype",
                "codeSoortObjectId": "codeSoortObjectId",
                "objectId": "objectId",
                "codeRegister": "codeRegister",
            },
        )

        with self.subTest("create_onderwerpobject_with_klantcontact"):
            klantcontact2 = KlantcontactFactory.create()
            data = {
                "klantcontact": {"uuid": str(klantcontact2.uuid)},
                "wasKlantcontact": None,
                "onderwerpobjectidentificator": {
                    "codeObjecttype": "codeObjecttype",
                    "codeSoortObjectId": "codeSoortObjectId",
                    "objectId": "objectId",
                    "codeRegister": "codeRegister",
                },
            }
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            data = response.json()

            self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact2.uuid))
            self.assertIsNone(data["wasKlantcontact"])
            self.assertEqual(
                data["onderwerpobjectidentificator"],
                {
                    "codeObjecttype": "codeObjecttype",
                    "codeSoortObjectId": "codeSoortObjectId",
                    "objectId": "objectId",
                    "codeRegister": "codeRegister",
                },
            )

        with self.subTest("create_onderwerpobject_with_was_klantcontact"):
            klantcontact3 = KlantcontactFactory.create()
            data = {
                "klantcontact": None,
                "wasKlantcontact": {"uuid": str(klantcontact3.uuid)},
                "onderwerpobjectidentificator": {
                    "codeObjecttype": "codeObjecttype",
                    "codeSoortObjectId": "codeSoortObjectId",
                    "objectId": "objectId",
                    "codeRegister": "codeRegister",
                },
            }
            response = self.client.post(list_url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            data = response.json()

            self.assertIsNone(data["klantcontact"])
            self.assertEqual(data["wasKlantcontact"]["uuid"], str(klantcontact3.uuid))
            self.assertEqual(
                data["onderwerpobjectidentificator"],
                {
                    "codeObjecttype": "codeObjecttype",
                    "codeSoortObjectId": "codeSoortObjectId",
                    "objectId": "objectId",
                    "codeRegister": "codeRegister",
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
            onderwerpobjectidentificator_code_objecttype="codeObjecttype",
            onderwerpobjectidentificator_code_soort_object_id="codeSoortObjectId",
            onderwerpobjectidentificator_object_id="objectId",
            onderwerpobjectidentificator_code_register="codeRegister",
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
            data["onderwerpobjectidentificator"],
            {
                "codeObjecttype": "codeObjecttype",
                "codeSoortObjectId": "codeSoortObjectId",
                "objectId": "objectId",
                "codeRegister": "codeRegister",
            },
        )

        data = {
            "klantcontact": {"uuid": str(klantcontact2.uuid)},
            "wasKlantcontact": {"uuid": str(klantcontact4.uuid)},
            "onderwerpobjectidentificator": {
                "codeObjecttype": "changed",
                "codeSoortObjectId": "changed",
                "objectId": "changed",
                "codeRegister": "changed",
            },
        }

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact2.uuid))
        self.assertEqual(data["wasKlantcontact"]["uuid"], str(klantcontact4.uuid))
        self.assertEqual(
            data["onderwerpobjectidentificator"],
            {
                "codeObjecttype": "changed",
                "codeSoortObjectId": "changed",
                "objectId": "changed",
                "codeRegister": "changed",
            },
        )

        with self.subTest("unset_klantcontact"):
            data = {
                "klantcontact": None,
                "wasKlantcontact": None,
                "onderwerpobjectidentificator": {
                    "codeObjecttype": "changed",
                    "codeSoortObjectId": "changed",
                    "objectId": "changed",
                    "codeRegister": "changed",
                },
            }

            response = self.client.put(detail_url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertIsNone(data["klantcontact"])
            self.assertIsNone(data["wasKlantcontact"])
            self.assertEqual(
                data["onderwerpobjectidentificator"],
                {
                    "codeObjecttype": "changed",
                    "codeSoortObjectId": "changed",
                    "objectId": "changed",
                    "codeRegister": "changed",
                },
            )

    def test_partial_update_onderwerpobject(self):
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=klantcontact,
            was_klantcontact=klantcontact2,
            onderwerpobjectidentificator_code_objecttype="codeObjecttype",
            onderwerpobjectidentificator_code_soort_object_id="codeSoortObjectId",
            onderwerpobjectidentificator_object_id="objectId",
            onderwerpobjectidentificator_code_register="codeRegister",
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
            data["onderwerpobjectidentificator"],
            {
                "codeObjecttype": "codeObjecttype",
                "codeSoortObjectId": "codeSoortObjectId",
                "objectId": "objectId",
                "codeRegister": "codeRegister",
            },
        )

        data = {
            "onderwerpobjectidentificator": {
                "codeObjecttype": "changed",
                "codeSoortObjectId": "changed",
                "objectId": "changed",
                "codeRegister": "changed",
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))
        self.assertEqual(data["wasKlantcontact"]["uuid"], str(klantcontact2.uuid))
        self.assertEqual(
            data["onderwerpobjectidentificator"],
            {
                "codeObjecttype": "changed",
                "codeSoortObjectId": "changed",
                "objectId": "changed",
                "codeRegister": "changed",
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


class ActorKlantcontactTests(APITestCase):
    def test_list_actorklantcontact(self):
        list_url = reverse("klantinteracties:actorklantcontact-list")
        ActorKlantcontactFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_actorklantcontact(self):
        actorklantcontact = ActorKlantcontactFactory.create()
        detail_url = reverse(
            "klantinteracties:actorklantcontact-detail",
            kwargs={"uuid": str(actorklantcontact.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create_actorklantcontact(self):
        list_url = reverse("klantinteracties:actorklantcontact-list")
        actor = ActorFactory.create()
        klantcontact = KlantcontactFactory.create()
        data = {
            "actor": {"uuid": str(actor.uuid)},
            "klantcontact": {"uuid": str(klantcontact.uuid)},
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["actor"]["uuid"], str(actor.uuid))
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))

        with self.subTest("test_unique_together"):
            response = self.client.post(list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(
                data["invalidParams"],
                [
                    {
                        "name": "nonFieldErrors",
                        "code": "unique",
                        "reason": "De velden actor, klantcontact moeten een unieke set zijn.",
                    }
                ],
            )

    def test_update_actorklantcontact(self):
        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        actorklantcontact = ActorKlantcontactFactory.create(
            actor=actor,
            klantcontact=klantcontact,
        )
        detail_url = reverse(
            "klantinteracties:actorklantcontact-detail",
            kwargs={"uuid": str(actorklantcontact.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["actor"]["uuid"], str(actor.uuid))
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))

        data = {
            "actor": {"uuid": str(actor2.uuid)},
            "klantcontact": {"uuid": str(klantcontact2.uuid)},
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["actor"]["uuid"], str(actor2.uuid))
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact2.uuid))

    def test_update_partial_actorklantcontact(self):
        actor, actor2 = ActorFactory.create_batch(2)
        klantcontact = KlantcontactFactory.create()
        actorklantcontact = ActorKlantcontactFactory.create(
            actor=actor,
            klantcontact=klantcontact,
        )
        detail_url = reverse(
            "klantinteracties:actorklantcontact-detail",
            kwargs={"uuid": str(actorklantcontact.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["actor"]["uuid"], str(actor.uuid))
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))

        data = {
            "actor": {"uuid": str(actor2.uuid)},
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["actor"]["uuid"], str(actor2.uuid))
        self.assertEqual(data["klantcontact"]["uuid"], str(klantcontact.uuid))

        with self.subTest("test_unique_together"):
            actorklantcontact = ActorKlantcontactFactory.create(
                actor=actor,
                klantcontact=klantcontact,
            )
            detail_url = reverse(
                "klantinteracties:actorklantcontact-detail",
                kwargs={"uuid": str(actorklantcontact.uuid)},
            )
            data = {
                "actor": {"uuid": str(actor2.uuid)},
            }

            # update new actorklantcontact object to have same data as the existing one.
            response = self.client.patch(detail_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertEqual(
                data["invalidParams"],
                [
                    {
                        "name": "nonFieldErrors",
                        "code": "unique",
                        "reason": "De velden actor, klantcontact moeten een unieke set zijn.",
                    }
                ],
            )

    def test_destroy_actorklantcontact(self):
        actorklantcontact = ActorKlantcontactFactory.create()
        detail_url = reverse(
            "klantinteracties:actorklantcontact-detail",
            kwargs={"uuid": str(actorklantcontact.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:actorklantcontact-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)


class MaakKlantcontactEndpointTests(APITestCase):
    maxDiff = None
    url = reverse("klantinteracties:maak-klantcontact-list")

    def test_create_success(self):
        post_data = {
            "klantcontact": KlantContactDataFactory.create(),
            "betrokkene": BetrokkeneDataFactory.create(),
            "onderwerpobject": OnderwerpObjectDataFactory.create(),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        klantcontact = Klantcontact.objects.get()
        betrokkene = Betrokkene.objects.get()
        onderwerpobject = Onderwerpobject.objects.get()

        klantcontact_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        betrokkene_url = reverse(
            "klantinteracties:betrokkene-detail",
            kwargs={"uuid": str(betrokkene.uuid)},
        )
        onderwerpobject_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )

        klantcontact_url = f"http://testserver{klantcontact_url}"
        betrokkene_url = f"http://testserver{betrokkene_url}"
        onderwerpobject_url = f"http://testserver{onderwerpobject_url}"

        data = response.json()

        self.assertEqual(
            list(data.keys()), ["klantcontact", "betrokkene", "onderwerpobject"]
        )

        with self.subTest("Klantcontact response data is correct"):
            expected_klantcontact = {
                "uuid": str(klantcontact.uuid),
                "url": klantcontact_url,
                "gingOverOnderwerpobjecten": [
                    {
                        "url": onderwerpobject_url,
                        "uuid": str(onderwerpobject.uuid),
                    }
                ],
                "hadBetrokkenActoren": [],
                "hadBetrokkenen": [
                    {
                        "url": betrokkene_url,
                        "uuid": str(betrokkene.uuid),
                    }
                ],
                "indicatieContactGelukt": False,
                "inhoud": "changed",
                "kanaal": "changed",
                "leiddeTotInterneTaken": [],
                "nummer": "7948723947",
                "omvatteBijlagen": [],
                "onderwerp": "changed",
                "plaatsgevondenOp": "2020-08-24T14:15:22Z",
                "taal": "de",
                "vertrouwelijk": False,
            }
            self.assertEqual(data["klantcontact"], expected_klantcontact)

        with self.subTest("Betrokkene response data is correct"):
            expected_betrokkene = {
                "uuid": str(betrokkene.uuid),
                "url": betrokkene_url,
                "hadKlantcontact": {
                    "url": klantcontact_url,
                    "uuid": str(klantcontact.uuid),
                },
                "wasPartij": None,
                "digitaleAdressen": [],
                "bezoekadres": {
                    "nummeraanduidingId": "1234567890000001",
                    "straatnaam": "straat",
                    "huisnummer": 10,
                    "huisnummertoevoeging": "A2",
                    "postcode": "1008 DG",
                    "stad": "Amsterdam",
                    "adresregel1": "adres1",
                    "adresregel2": "adres2",
                    "adresregel3": "adres3",
                    "land": "NL",
                },
                "correspondentieadres": {
                    "nummeraanduidingId": "1234567890000002",
                    "straatnaam": "straat",
                    "huisnummer": 10,
                    "huisnummertoevoeging": "A2",
                    "postcode": "1008 DG",
                    "stad": "Amsterdam",
                    "adresregel1": "adres1",
                    "adresregel2": "adres2",
                    "adresregel3": "adres3",
                    "land": "NL",
                },
                "contactnaam": {
                    "voorletters": "P",
                    "voornaam": "Phil",
                    "voorvoegselAchternaam": "",
                    "achternaam": "Bozeman",
                },
                "volledigeNaam": "Phil Bozeman",
                "rol": "vertegenwoordiger",
                "organisatienaam": "Whitechapel",
                "initiator": True,
            }
            self.assertEqual(data["betrokkene"], expected_betrokkene)
            self.assertEqual(betrokkene.klantcontact, klantcontact)

        with self.subTest("Onderwerpobject response data is correct"):
            expected_onderwerpobject = {
                "uuid": str(onderwerpobject.uuid),
                "url": onderwerpobject_url,
                "klantcontact": {
                    "url": klantcontact_url,
                    "uuid": str(klantcontact.uuid),
                },
                "wasKlantcontact": None,
                "onderwerpobjectidentificator": {
                    "codeObjecttype": "codeObjecttype",
                    "codeSoortObjectId": "codeSoortObjectId",
                    "objectId": "objectId",
                    "codeRegister": "codeRegister",
                },
            }
            self.assertEqual(data["onderwerpobject"], expected_onderwerpobject)
            self.assertEqual(onderwerpobject.klantcontact, klantcontact)

    def test_create_klantcontact_validation_error(self):
        """
        If there are validation errors in the Klantcontact, no resources should be created
        """
        post_data = {
            "klantcontact": KlantContactDataFactory.create(taal="incorrect"),
            "betrokkene": BetrokkeneDataFactory.create(),
            "onderwerpobject": OnderwerpObjectDataFactory.create(),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "klantcontact.taal",
                    "code": "max_length",
                    "reason": _(
                        "Zorg ervoor dat dit veld niet meer dan 3 karakters bevat."
                    ),
                }
            ],
        )

        self.assertFalse(Klantcontact.objects.exists())
        self.assertFalse(Betrokkene.objects.exists())
        self.assertFalse(Onderwerpobject.objects.exists())

    def test_create_betrokkene_validation_error(self):
        """
        If there are validation errors in the Betrokkene, no resources should be created
        """
        post_data = {
            "klantcontact": KlantContactDataFactory.create(),
            "betrokkene": BetrokkeneDataFactory.create(wasPartij="incorrect"),
            "onderwerpobject": OnderwerpObjectDataFactory.create(),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "betrokkene.wasPartij.nonFieldErrors",
                    "code": "invalid",
                    "reason": _(
                        "Ongeldige data. Verwacht een dictionary, kreeg een str."
                    ),
                }
            ],
        )

        self.assertFalse(Klantcontact.objects.exists())
        self.assertFalse(Betrokkene.objects.exists())
        self.assertFalse(Onderwerpobject.objects.exists())

    def test_create_use_read_only_betrokkene_attributes(self):
        post_data = {
            "klantcontact": KlantContactDataFactory.create(),
            # `hadKlantcontact` field should be ignored
            "betrokkene": BetrokkeneDataFactory.create(hadKlantcontact="foobar"),
            "onderwerpobject": OnderwerpObjectDataFactory.create(),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        klantcontact = Klantcontact.objects.get()
        betrokkene = Betrokkene.objects.get()
        onderwerpobject = Onderwerpobject.objects.get()

        klantcontact_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        betrokkene_url = reverse(
            "klantinteracties:betrokkene-detail",
            kwargs={"uuid": str(betrokkene.uuid)},
        )
        onderwerpobject_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )

        klantcontact_url = f"http://testserver{klantcontact_url}"
        betrokkene_url = f"http://testserver{betrokkene_url}"
        onderwerpobject_url = f"http://testserver{onderwerpobject_url}"

        data = response.json()

        self.assertEqual(
            list(data.keys()), ["klantcontact", "betrokkene", "onderwerpobject"]
        )

        with self.subTest("Klantcontact is linked to Betrokkene"):
            self.assertEqual(
                data["klantcontact"]["hadBetrokkenen"],
                [
                    {
                        "url": betrokkene_url,
                        "uuid": str(betrokkene.uuid),
                    }
                ],
            )

        with self.subTest("Betrokkene is linked to Klantcontact"):
            self.assertEqual(
                data["betrokkene"]["hadKlantcontact"],
                {
                    "url": klantcontact_url,
                    "uuid": str(klantcontact.uuid),
                },
            )
            self.assertEqual(betrokkene.klantcontact, klantcontact)

    def test_create_betrokkene_was_partij_and_partij(self):
        partij = PartijFactory.create(voorkeurs_digitaal_adres=None)
        post_data = {
            "klantcontact": KlantContactDataFactory.create(),
            # `partij` should be ignored
            "betrokkene": BetrokkeneDataFactory.create(
                partij="foobar", wasPartij={"uuid": str(partij.uuid)}
            ),
            "onderwerpobject": OnderwerpObjectDataFactory.create(),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        klantcontact = Klantcontact.objects.get()
        betrokkene = Betrokkene.objects.get()
        onderwerpobject = Onderwerpobject.objects.get()

        klantcontact_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        betrokkene_url = reverse(
            "klantinteracties:betrokkene-detail",
            kwargs={"uuid": str(betrokkene.uuid)},
        )
        onderwerpobject_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )

        klantcontact_url = f"http://testserver{klantcontact_url}"
        betrokkene_url = f"http://testserver{betrokkene_url}"
        onderwerpobject_url = f"http://testserver{onderwerpobject_url}"

        data = response.json()

        self.assertEqual(
            list(data.keys()), ["klantcontact", "betrokkene", "onderwerpobject"]
        )

        with self.subTest("Klantcontact is linked to Betrokkene"):
            self.assertEqual(
                data["klantcontact"]["hadBetrokkenen"],
                [
                    {
                        "url": betrokkene_url,
                        "uuid": str(betrokkene.uuid),
                    }
                ],
            )

        with self.subTest("Betrokkene is linked to Klantcontact and Partij"):
            self.assertEqual(
                data["betrokkene"]["hadKlantcontact"],
                {
                    "url": klantcontact_url,
                    "uuid": str(klantcontact.uuid),
                },
            )
            self.assertEqual(betrokkene.klantcontact, klantcontact)
            self.assertEqual(betrokkene.partij, partij)

    def test_create_onderwerpobject_validation_error(self):
        """
        If there are validation errors in the Betrokkene, no resources should be created
        """
        post_data = {
            "klantcontact": KlantContactDataFactory.create(),
            "betrokkene": BetrokkeneDataFactory.create(),
            "onderwerpobject": OnderwerpObjectDataFactory.create(
                onderwerpobjectidentificator__objectId=True
            ),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(
            data["invalidParams"],
            [
                {
                    "name": "onderwerpobject.onderwerpobjectidentificator.objectId",
                    "code": "invalid",
                    "reason": _("Not a valid string."),
                }
            ],
        )

        self.assertFalse(Klantcontact.objects.exists())
        self.assertFalse(Betrokkene.objects.exists())
        self.assertFalse(Onderwerpobject.objects.exists())

    def test_create_use_read_only_onderwerpobject_attributes(self):
        post_data = {
            "klantcontact": KlantContactDataFactory.create(),
            "betrokkene": BetrokkeneDataFactory.create(),
            # `klantcontact` field should be ignored
            "onderwerpobject": OnderwerpObjectDataFactory.create(klantcontact="foobar"),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        klantcontact = Klantcontact.objects.get()
        betrokkene = Betrokkene.objects.get()
        onderwerpobject = Onderwerpobject.objects.get()

        klantcontact_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        betrokkene_url = reverse(
            "klantinteracties:betrokkene-detail",
            kwargs={"uuid": str(betrokkene.uuid)},
        )
        onderwerpobject_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )

        klantcontact_url = f"http://testserver{klantcontact_url}"
        betrokkene_url = f"http://testserver{betrokkene_url}"
        onderwerpobject_url = f"http://testserver{onderwerpobject_url}"

        data = response.json()

        self.assertEqual(
            list(data.keys()), ["klantcontact", "betrokkene", "onderwerpobject"]
        )

        with self.subTest("Klantcontact is linked to Betrokkene"):
            self.assertEqual(
                data["klantcontact"]["gingOverOnderwerpobjecten"],
                [
                    {
                        "url": onderwerpobject_url,
                        "uuid": str(onderwerpobject.uuid),
                    }
                ],
            )

        with self.subTest("Onderwerpobject is linked to Klantcontact"):
            self.assertEqual(
                data["onderwerpobject"]["klantcontact"],
                {
                    "url": klantcontact_url,
                    "uuid": str(klantcontact.uuid),
                },
            )
            self.assertEqual(onderwerpobject.klantcontact, klantcontact)

    def test_create_onderwerpobject_with_was_klantcontact(self):
        existing_klantcontact = KlantcontactFactory.create()
        existing_klantcontact_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(existing_klantcontact.uuid)},
        )
        existing_klantcontact_url = f"http://testserver{existing_klantcontact_url}"
        post_data = {
            "klantcontact": KlantContactDataFactory.create(),
            "betrokkene": BetrokkeneDataFactory.create(),
            "onderwerpobject": OnderwerpObjectDataFactory.create(
                wasKlantcontact={"uuid": str(existing_klantcontact.uuid)}
            ),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        klantcontact = Klantcontact.objects.last()
        betrokkene = Betrokkene.objects.get()
        onderwerpobject = Onderwerpobject.objects.get()

        klantcontact_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        betrokkene_url = reverse(
            "klantinteracties:betrokkene-detail",
            kwargs={"uuid": str(betrokkene.uuid)},
        )
        onderwerpobject_url = reverse(
            "klantinteracties:onderwerpobject-detail",
            kwargs={"uuid": str(onderwerpobject.uuid)},
        )

        klantcontact_url = f"http://testserver{klantcontact_url}"
        betrokkene_url = f"http://testserver{betrokkene_url}"
        onderwerpobject_url = f"http://testserver{onderwerpobject_url}"

        data = response.json()

        self.assertEqual(
            list(data.keys()), ["klantcontact", "betrokkene", "onderwerpobject"]
        )

        with self.subTest("Klantcontact is linked to Betrokkene"):
            self.assertEqual(
                data["klantcontact"]["gingOverOnderwerpobjecten"],
                [
                    {
                        "url": onderwerpobject_url,
                        "uuid": str(onderwerpobject.uuid),
                    }
                ],
            )

        with self.subTest("Onderwerpobject is linked to Klantcontact"):
            self.assertEqual(
                data["onderwerpobject"]["klantcontact"],
                {
                    "url": klantcontact_url,
                    "uuid": str(klantcontact.uuid),
                },
            )
            self.assertEqual(
                data["onderwerpobject"]["wasKlantcontact"],
                {
                    "url": existing_klantcontact_url,
                    "uuid": str(existing_klantcontact.uuid),
                },
            )
            self.assertEqual(onderwerpobject.klantcontact, klantcontact)
            self.assertEqual(onderwerpobject.was_klantcontact, existing_klantcontact)

    def test_create_without_betrokkene_and_onderwerpobject(self):
        post_data = {
            "klantcontact": KlantContactDataFactory.create(),
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        klantcontact = Klantcontact.objects.get()

        self.assertFalse(Betrokkene.objects.exists())
        self.assertFalse(Onderwerpobject.objects.exists())

        klantcontact_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )

        klantcontact_url = f"http://testserver{klantcontact_url}"

        data = response.json()

        self.assertEqual(
            list(data.keys()), ["klantcontact", "betrokkene", "onderwerpobject"]
        )

        with self.subTest("Klantcontact response data is correct"):
            expected_klantcontact = {
                "uuid": str(klantcontact.uuid),
                "url": klantcontact_url,
                "gingOverOnderwerpobjecten": [],
                "hadBetrokkenActoren": [],
                "hadBetrokkenen": [],
                "indicatieContactGelukt": False,
                "inhoud": "changed",
                "kanaal": "changed",
                "leiddeTotInterneTaken": [],
                "nummer": "7948723947",
                "omvatteBijlagen": [],
                "onderwerp": "changed",
                "plaatsgevondenOp": "2020-08-24T14:15:22Z",
                "taal": "de",
                "vertrouwelijk": False,
            }
            self.assertEqual(data["klantcontact"], expected_klantcontact)

        with self.subTest("Betrokkene is None in response"):
            self.assertEqual(data["betrokkene"], None)

        with self.subTest("Onderwerpobject is None in response"):
            self.assertEqual(data["onderwerpobject"], None)
