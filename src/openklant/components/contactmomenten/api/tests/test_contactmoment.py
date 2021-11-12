from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from openklant.components.contactmomenten.datamodel.constants import InitiatiefNemer
from openklant.components.contactmomenten.datamodel.models import ContactMoment
from openklant.components.contactmomenten.datamodel.tests.factories import (
    ContactMomentFactory,
    KlantContactMomentFactory,
    MedewerkerFactory,
    ObjectContactMomentFactory,
)

KLANT = "http://klanten.nl/api/v1/klanten/12345"


class ContactMomentTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_contactmomenten(self):
        list_url = reverse(ContactMoment)
        ContactMomentFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_contactmoment(self):
        contactmoment = ContactMomentFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
        )
        detail_url = reverse(contactmoment)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "vorigContactmoment": None,
                "volgendContactmoment": None,
                "bronorganisatie": contactmoment.bronorganisatie,
                "registratiedatum": "2019-01-01T00:00:00Z",
                "kanaal": contactmoment.kanaal,
                "voorkeurskanaal": contactmoment.voorkeurskanaal,
                "voorkeurstaal": contactmoment.voorkeurstaal,
                "tekst": contactmoment.tekst,
                "onderwerpLinks": [],
                "initiatiefnemer": InitiatiefNemer.gemeente,
                "medewerker": contactmoment.medewerker,
                "medewerkerIdentificatie": None,
            },
        )

    def test_read_contactmoment_with_medewerker(self):
        contactmoment = ContactMomentFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
            medewerker="",
            voorkeurstaal="nld",
        )
        medewerker = MedewerkerFactory.create(contactmoment=contactmoment)
        detail_url = reverse(contactmoment)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "vorigContactmoment": None,
                "volgendContactmoment": None,
                "bronorganisatie": contactmoment.bronorganisatie,
                "registratiedatum": "2019-01-01T00:00:00Z",
                "kanaal": contactmoment.kanaal,
                "voorkeurskanaal": contactmoment.voorkeurskanaal,
                "voorkeurstaal": contactmoment.voorkeurstaal,
                "tekst": contactmoment.tekst,
                "onderwerpLinks": [],
                "initiatiefnemer": InitiatiefNemer.gemeente,
                "medewerker": "",
                "medewerkerIdentificatie": {
                    "identificatie": medewerker.identificatie,
                    "achternaam": medewerker.achternaam,
                    "voorletters": medewerker.voorletters,
                    "voorvoegselAchternaam": medewerker.voorvoegsel_achternaam,
                },
            },
        )

    def test_create_contactmoment(self):
        list_url = reverse(ContactMoment)
        data = {
            "bronorganisatie": "423182687",
            "kanaal": "telephone",
            "tekst": "some text",
            "onderwerpLinks": [],
            "initiatiefnemer": InitiatiefNemer.gemeente,
            "medewerker": "http://example.com/medewerker/1",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contactmoment = ContactMoment.objects.get()

        self.assertEqual(contactmoment.kanaal, "telephone")
        self.assertEqual(contactmoment.tekst, "some text")
        self.assertEqual(contactmoment.initiatiefnemer, InitiatiefNemer.gemeente)
        self.assertEqual(contactmoment.medewerker, "http://example.com/medewerker/1")

    def test_create_contactmoment_with_medewerker(self):
        list_url = reverse(ContactMoment)
        data = {
            "bronorganisatie": "423182687",
            "kanaal": "telephone",
            "tekst": "some text",
            "onderwerpLinks": [],
            "initiatiefnemer": InitiatiefNemer.gemeente,
            "medewerkerIdentificatie": {
                "identificatie": "12345",
                "achternaam": "Buurman",
                "voorletters": "B B",
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contactmoment = ContactMoment.objects.get()

        self.assertEqual(contactmoment.kanaal, "telephone")
        self.assertEqual(contactmoment.tekst, "some text")
        self.assertEqual(contactmoment.initiatiefnemer, InitiatiefNemer.gemeente)

        medewerker = contactmoment.medewerker_identificatie

        self.assertEqual(medewerker.identificatie, "12345")
        self.assertEqual(medewerker.achternaam, "Buurman")
        self.assertEqual(medewerker.voorletters, "B B")

    def test_create_contactmoment_fail_no_medewerker(self):
        list_url = reverse(ContactMoment)
        data = {
            "bronorganisatie": "423182687",
            "klant": KLANT,
            "kanaal": "telephone",
            "tekst": "some text",
            "initiatiefnemer": InitiatiefNemer.gemeente,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "invalid-medewerker")

    def test_create_contactmoment_vorig_contactmoment(self):
        vorig_cmc = ContactMomentFactory.create()
        list_url = reverse(ContactMoment)
        data = {
            "bronorganisatie": "423182687",
            "kanaal": "telephone",
            "tekst": "some text",
            "onderwerpLinks": [],
            "initiatiefnemer": InitiatiefNemer.gemeente,
            "medewerker": "http://example.com/medewerker/1",
            "vorigContactmoment": reverse(vorig_cmc),
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contactmoment = ContactMoment.objects.last()

        self.assertEqual(contactmoment.kanaal, "telephone")
        self.assertEqual(contactmoment.tekst, "some text")
        self.assertEqual(contactmoment.initiatiefnemer, InitiatiefNemer.gemeente)
        self.assertEqual(contactmoment.medewerker, "http://example.com/medewerker/1")
        self.assertEqual(contactmoment.vorig_contactmoment, vorig_cmc)

        # Check if volgendContactmoment is set correctly

        response = self.client.get(reverse(vorig_cmc))

        self.assertEqual(
            response.data["volgend_contactmoment"],
            f"http://testserver{reverse(contactmoment)}",
        )

        vorig_cmc.refresh_from_db()
        self.assertEqual(vorig_cmc.volgend_contactmoment, contactmoment)

    def test_update_contactmoment(self):
        contactmoment = ContactMomentFactory.create()
        detail_url = reverse(contactmoment)

        response = self.client.patch(detail_url, {"kanaal": "some-kanaal"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contactmoment.refresh_from_db()

        self.assertEqual(contactmoment.kanaal, "some-kanaal")

    def test_update_contactmoment_with_medewerker(self):
        contactmoment = ContactMomentFactory.create()
        detail_url = reverse(contactmoment)
        data = {
            "medewerker": "",
            "medewerkerIdentificatie": {
                "identificatie": "12345",
                "achternaam": "Buurman",
                "voorletters": "B B",
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contactmoment.refresh_from_db()

        self.assertEqual(contactmoment.medewerker, "")

        medewerker = contactmoment.medewerker_identificatie

        self.assertEqual(medewerker.identificatie, "12345")
        self.assertEqual(medewerker.achternaam, "Buurman")
        self.assertEqual(medewerker.voorletters, "B B")

    def test_update_contactmoment_override_vorig_contactmoment(self):
        vorig_cmc = ContactMomentFactory.create()
        contactmoment = ContactMomentFactory.create(vorig_contactmoment=vorig_cmc)

        new_vorig_cmc = ContactMomentFactory.create()

        detail_url = reverse(contactmoment)
        data = {"vorigContactmoment": reverse(new_vorig_cmc)}

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vorig_cmc.refresh_from_db()
        contactmoment.refresh_from_db()
        new_vorig_cmc.refresh_from_db()

        self.assertEqual(contactmoment.vorig_contactmoment, new_vorig_cmc)
        self.assertEqual(new_vorig_cmc.volgend_contactmoment, contactmoment)

    def test_destroy_contactmoment(self):
        contactmoment = ContactMomentFactory.create()
        detail_url = reverse(contactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactMoment.objects.count(), 0)

    def test_pagination_default(self):
        ContactMomentFactory.create_batch(2)
        url = reverse(ContactMoment)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        ContactMomentFactory.create_batch(2)
        url = reverse(ContactMoment)

        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])


class ContactMomentFilterTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True
    list_url = reverse(ContactMoment)

    def test_filter_voorkeurstaal(self):
        ContactMomentFactory.create(voorkeurstaal="nld")
        ContactMomentFactory.create(voorkeurstaal="eng")

        response = self.client.get(
            self.list_url,
            {"voorkeurstaal": "nld"},
            HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["voorkeurstaal"],
            "nld",
        )

    def test_filter_bronorganisatie(self):
        ContactMomentFactory.create(bronorganisatie="000000000")
        ContactMomentFactory.create(bronorganisatie="000099998")

        response = self.client.get(
            self.list_url,
            {"bronorganisatie": "000000000"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1, response.data)
        self.assertEqual(
            response.data["results"][0]["bronorganisatie"],
            "000000000",
        )

    def test_list_contactmomenten_filter_vorig_contactmoment(self):
        list_url = reverse(ContactMoment)
        cmc1, cmc2, cmc3 = ContactMomentFactory.create_batch(3)
        cmc3.vorig_contactmoment = cmc2
        cmc3.save()

        response = self.client.get(
            list_url,
            {"vorigContactmoment": f"http://testserver.com{reverse(cmc2)}"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["vorig_contactmoment"],
            f"http://testserver.com{reverse(cmc2)}",
        )

    def test_list_contactmomenten_filter_volgend_contactmoment(self):
        list_url = reverse(ContactMoment)
        cmc1, cmc2, cmc3 = ContactMomentFactory.create_batch(3)
        cmc3.vorig_contactmoment = cmc2
        cmc3.save()

        response = self.client.get(
            list_url,
            {"volgendContactmoment": f"http://testserver.com{reverse(cmc3)}"},
            HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["volgend_contactmoment"],
            f"http://testserver.com{reverse(cmc3)}",
        )

    def test_filter_registratiedatum(self):
        ContactMomentFactory.create(registratiedatum="2020-01-01T12:00:00Z")
        ContactMomentFactory.create(registratiedatum="2019-03-02T22:00:00Z")

        response = self.client.get(
            self.list_url,
            {"registratiedatum": "2020-01-01T12:00:00Z"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["registratiedatum"],
            "2020-01-01T12:00:00Z",
        )

    def test_filter_registratiedatum_gt(self):
        ContactMomentFactory.create(registratiedatum="2020-01-01T12:00:00Z")
        ContactMomentFactory.create(registratiedatum="2019-03-02T22:00:00Z")

        response = self.client.get(
            self.list_url,
            {"registratiedatum__gt": "2019-03-02T22:00:00Z"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["registratiedatum"],
            "2020-01-01T12:00:00Z",
        )

    def test_filter_registratiedatum_gte(self):
        ContactMomentFactory.create(registratiedatum="2020-01-01T12:00:00Z")
        ContactMomentFactory.create(registratiedatum="2019-03-02T22:00:00Z")

        response = self.client.get(
            self.list_url,
            {"registratiedatum__gte": "2020-01-01T12:00:00Z"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["registratiedatum"],
            "2020-01-01T12:00:00Z",
        )

    def test_filter_registratiedatum_lt(self):
        ContactMomentFactory.create(registratiedatum="2020-01-01T12:00:00Z")
        ContactMomentFactory.create(registratiedatum="2019-03-02T22:00:00Z")

        response = self.client.get(
            self.list_url,
            {"registratiedatum__lt": "2020-01-01T12:00:00Z"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["registratiedatum"],
            "2019-03-02T22:00:00Z",
        )

    def test_filter_registratiedatum_lte(self):
        ContactMomentFactory.create(registratiedatum="2020-01-01T12:00:00Z")
        ContactMomentFactory.create(registratiedatum="2019-03-02T22:00:00Z")

        response = self.client.get(
            self.list_url,
            {"registratiedatum__lte": "2019-03-02T22:00:00Z"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["registratiedatum"],
            "2019-03-02T22:00:00Z",
        )

    def test_filter_kanaal(self):
        ContactMomentFactory.create(kanaal="kanaal1")
        ContactMomentFactory.create(kanaal="kanaal2")

        response = self.client.get(
            self.list_url,
            {"kanaal": "kanaal1"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["kanaal"],
            "kanaal1",
        )

    def test_filter_voorkeurskanaal(self):
        ContactMomentFactory.create(voorkeurskanaal="kanaal1")
        ContactMomentFactory.create(voorkeurskanaal="kanaal2")

        response = self.client.get(
            self.list_url,
            {"voorkeurskanaal": "kanaal1"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["voorkeurskanaal"],
            "kanaal1",
        )

    def test_filter_initiatiefnemer(self):
        ContactMomentFactory.create(initiatiefnemer=InitiatiefNemer.gemeente)
        ContactMomentFactory.create(initiatiefnemer=InitiatiefNemer.klant)

        response = self.client.get(
            self.list_url,
            {"initiatiefnemer": InitiatiefNemer.gemeente},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["initiatiefnemer"],
            InitiatiefNemer.gemeente,
        )

    def test_filter_medewerker(self):
        ContactMomentFactory.create(medewerker="http://testserver.com/medewerker/1")
        ContactMomentFactory.create(medewerker="http://testserver.com/medewerker/2")

        response = self.client.get(
            self.list_url,
            {"medewerker": "http://testserver.com/medewerker/1"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["medewerker"],
            "http://testserver.com/medewerker/1",
        )

    def test_filter_ordering(self):
        ContactMomentFactory.create(kanaal="bcd")
        ContactMomentFactory.create(kanaal="abc")

        response = self.client.get(
            self.list_url,
            {"ordering": "kanaal"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0]["kanaal"],
            "abc",
        )

    def test_filter_object_url(self):
        cm1 = ContactMomentFactory.create(kanaal="telefoon")
        cm2 = ContactMomentFactory.create(kanaal="whatsapp")
        cm3 = ContactMomentFactory.create(kanaal="email")

        ObjectContactMomentFactory.create(
            contactmoment=cm1, object="http://example.com/api/v1/1"
        )
        ObjectContactMomentFactory.create(
            contactmoment=cm2, object="http://example.com/api/v1/2"
        )
        ObjectContactMomentFactory.create(
            contactmoment=cm3, object="http://example.com/api/v1/2"
        )

        response = self.client.get(
            self.list_url,
            {"object": "http://example.com/api/v1/2"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0]["kanaal"],
            "email",
        )
        self.assertEqual(
            response.data["results"][1]["kanaal"],
            "whatsapp",
        )

    def test_filter_object_url_multiple(self):
        cm1 = ContactMomentFactory.create(kanaal="telefoon")
        cm2 = ContactMomentFactory.create(kanaal="whatsapp")
        cm3 = ContactMomentFactory.create(kanaal="email")

        ObjectContactMomentFactory.create(
            contactmoment=cm1, object="http://example.com/api/v1/1"
        )
        ObjectContactMomentFactory.create(
            contactmoment=cm2, object="http://example.com/api/v1/2"
        )
        ObjectContactMomentFactory.create(
            contactmoment=cm3, object="http://example.com/api/v1/3"
        )

        response = self.client.get(
            self.list_url,
            {"object": "http://example.com/api/v1/2,http://example.com/api/v1/3"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0]["kanaal"],
            "email",
        )
        self.assertEqual(
            response.data["results"][1]["kanaal"],
            "whatsapp",
        )

    def test_filter_klant_url(self):
        cm1 = ContactMomentFactory.create(kanaal="telefoon")
        cm2 = ContactMomentFactory.create(kanaal="whatsapp")
        cm3 = ContactMomentFactory.create(kanaal="email")

        KlantContactMomentFactory.create(
            contactmoment=cm1, klant="http://example.com/api/v1/1"
        )
        KlantContactMomentFactory.create(
            contactmoment=cm2, klant="http://example.com/api/v1/2"
        )
        KlantContactMomentFactory.create(
            contactmoment=cm3, klant="http://example.com/api/v1/2"
        )

        response = self.client.get(
            self.list_url,
            {"klant": "http://example.com/api/v1/2"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0]["kanaal"],
            "email",
        )
        self.assertEqual(
            response.data["results"][1]["kanaal"],
            "whatsapp",
        )

    def test_filter_object_url_multiple(self):
        cm1 = ContactMomentFactory.create(kanaal="telefoon")
        cm2 = ContactMomentFactory.create(kanaal="whatsapp")
        cm3 = ContactMomentFactory.create(kanaal="email")

        KlantContactMomentFactory.create(
            contactmoment=cm1, klant="http://example.com/api/v1/1"
        )
        KlantContactMomentFactory.create(
            contactmoment=cm2, klant="http://example.com/api/v1/2"
        )
        KlantContactMomentFactory.create(
            contactmoment=cm3, klant="http://example.com/api/v1/3"
        )

        response = self.client.get(
            self.list_url,
            {"klant": "http://example.com/api/v1/2,http://example.com/api/v1/3"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0]["kanaal"],
            "email",
        )
        self.assertEqual(
            response.data["results"][1]["kanaal"],
            "whatsapp",
        )

    def test_filter_klant_url_and_object_url(self):
        cm1 = ContactMomentFactory.create(kanaal="telefoon")
        cm2 = ContactMomentFactory.create(kanaal="whatsapp")
        cm3 = ContactMomentFactory.create(kanaal="email")

        KlantContactMomentFactory.create(
            contactmoment=cm1, klant="http://example.com/api/v1/1"
        )
        KlantContactMomentFactory.create(
            contactmoment=cm2, klant="http://example.com/api/v1/2"
        )
        KlantContactMomentFactory.create(
            contactmoment=cm3, klant="http://example.com/api/v1/2"
        )
        ObjectContactMomentFactory.create(
            contactmoment=cm1, object="http://example.com/api/v1/1"
        )
        ObjectContactMomentFactory.create(
            contactmoment=cm2, object="http://example.com/api/v1/2"
        )
        ObjectContactMomentFactory.create(
            contactmoment=cm3, object="http://example.com/api/v1/3"
        )

        response = self.client.get(
            self.list_url,
            {
                "klant": "http://example.com/api/v1/2",
                "object": "http://example.com/api/v1/3",
            },
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["kanaal"],
            "email",
        )

    def test_filter_medewerker_identificatie_identificatie(self):
        cm1 = ContactMomentFactory.create(kanaal="telefoon")
        cm2 = ContactMomentFactory.create(kanaal="whatsapp")
        cm3 = ContactMomentFactory.create(kanaal="email")

        MedewerkerFactory.create(
            contactmoment=cm1,
            identificatie="1234",
            achternaam="foo",
            voorletters="b",
            voorvoegsel_achternaam="c",
        )
        MedewerkerFactory.create(
            contactmoment=cm2,
            identificatie="4321",
            achternaam="bar",
            voorletters="c",
            voorvoegsel_achternaam="a",
        )
        MedewerkerFactory.create(
            contactmoment=cm3,
            identificatie="5678",
            achternaam="baz",
            voorletters="a",
            voorvoegsel_achternaam="b",
        )

        filters = {
            "identificatie": "4321",
            "achternaam": "bar",
            "voorletters": "c",
            "voorvoegselAchternaam": "a",
        }

        for parameter, value in filters.items():
            with self.subTest(parameter=parameter):
                response = self.client.get(
                    self.list_url,
                    {f"medewerkerIdentificatie__{parameter}": value},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.data["results"]), 1)
                self.assertEqual(
                    response.data["results"][0]["kanaal"],
                    "whatsapp",
                )
