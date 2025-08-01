from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    ActorKlantcontactFactory,
    BetrokkeneFactory,
    BijlageFactory,
    DigitaalAdresFactory,
    InterneTaakFactory,
    KlantcontactFactory,
    OnderwerpobjectFactory,
    PartijFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class ExpandTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.actor = ActorFactory.create()
        self.klantcontact = KlantcontactFactory.create()
        self.actorklantcontact = ActorKlantcontactFactory.create(
            actor=self.actor, klantcontact=self.klantcontact
        )
        self.internetaak = InterneTaakFactory.create(klantcontact=self.klantcontact)
        self.onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact, was_klantcontact=None
        )
        self.bijlage = BijlageFactory.create(klantcontact=self.klantcontact)

        self.partij = PartijFactory.create(voorkeurs_digitaal_adres=None)
        self.digitaal_adres = DigitaalAdresFactory.create(
            partij=self.partij, betrokkene=None
        )
        self.betrokkene = BetrokkeneFactory.create(
            klantcontact=self.klantcontact, partij=self.partij
        )

    def test_list_single_expansion(self):
        list_url = reverse("klantinteracties:klantcontact-list")
        response = self.client.get(list_url, {"expand": "hadBetrokkenen"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)
        klantcontact = data["results"][0]

        self.assertEqual(
            klantcontact["hadBetrokkenen"][0]["uuid"], str(self.betrokkene.uuid)
        )
        self.assertTrue(klantcontact["_expand"])
        expand = klantcontact["_expand"]["hadBetrokkenen"][0]

        self.assertEqual(
            expand["bezoekadres"],
            {
                "nummeraanduidingId": self.betrokkene.bezoekadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.bezoekadres_straatnaam,
                "huisnummer": self.betrokkene.bezoekadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.bezoekadres_huisnummertoevoeging,
                "postcode": self.betrokkene.bezoekadres_postcode,
                "stad": self.betrokkene.bezoekadres_stad,
                "adresregel1": self.betrokkene.bezoekadres_adresregel1,
                "adresregel2": self.betrokkene.bezoekadres_adresregel2,
                "adresregel3": self.betrokkene.bezoekadres_adresregel3,
                "land": self.betrokkene.bezoekadres_land,
            },
        )
        self.assertEqual(
            expand["correspondentieadres"],
            {
                "nummeraanduidingId": self.betrokkene.correspondentieadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.betrokkene.correspondentieadres_adresregel1,
                "adresregel2": self.betrokkene.correspondentieadres_adresregel2,
                "adresregel3": self.betrokkene.correspondentieadres_adresregel3,
                "land": self.betrokkene.correspondentieadres_land,
            },
        )
        self.assertEqual(
            expand["contactnaam"],
            {
                "voorletters": self.betrokkene.contactnaam_voorletters,
                "voornaam": self.betrokkene.contactnaam_voornaam,
                "voorvoegselAchternaam": self.betrokkene.contactnaam_voorvoegsel_achternaam,
                "achternaam": self.betrokkene.contactnaam_achternaam,
            },
        )
        self.assertEqual(expand["rol"], self.betrokkene.rol)
        self.assertEqual(expand["organisatienaam"], self.betrokkene.organisatienaam)
        self.assertEqual(expand["initiator"], self.betrokkene.initiator)
        self.assertEqual(expand["wasPartij"]["uuid"], str(self.partij.uuid))

    def test_list_multiple_level_expansion(self):
        list_url = reverse("klantinteracties:klantcontact-list")
        response = self.client.get(
            list_url, {"expand": "hadBetrokkenen,hadBetrokkenen.wasPartij"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)
        klantcontact = data["results"][0]

        self.assertEqual(
            klantcontact["hadBetrokkenen"][0]["uuid"], str(self.betrokkene.uuid)
        )
        self.assertTrue(klantcontact["_expand"])
        expand = klantcontact["_expand"]["hadBetrokkenen"][0]

        self.assertEqual(
            expand["bezoekadres"],
            {
                "nummeraanduidingId": self.betrokkene.bezoekadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.bezoekadres_straatnaam,
                "huisnummer": self.betrokkene.bezoekadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.bezoekadres_huisnummertoevoeging,
                "postcode": self.betrokkene.bezoekadres_postcode,
                "stad": self.betrokkene.bezoekadres_stad,
                "adresregel1": self.betrokkene.bezoekadres_adresregel1,
                "adresregel2": self.betrokkene.bezoekadres_adresregel2,
                "adresregel3": self.betrokkene.bezoekadres_adresregel3,
                "land": self.betrokkene.bezoekadres_land,
            },
        )
        self.assertEqual(
            expand["correspondentieadres"],
            {
                "nummeraanduidingId": self.betrokkene.correspondentieadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.betrokkene.correspondentieadres_adresregel1,
                "adresregel2": self.betrokkene.correspondentieadres_adresregel2,
                "adresregel3": self.betrokkene.correspondentieadres_adresregel3,
                "land": self.betrokkene.correspondentieadres_land,
            },
        )
        self.assertEqual(
            expand["contactnaam"],
            {
                "voorletters": self.betrokkene.contactnaam_voorletters,
                "voornaam": self.betrokkene.contactnaam_voornaam,
                "voorvoegselAchternaam": self.betrokkene.contactnaam_voorvoegsel_achternaam,
                "achternaam": self.betrokkene.contactnaam_achternaam,
            },
        )
        self.assertEqual(expand["rol"], self.betrokkene.rol)
        self.assertEqual(expand["organisatienaam"], self.betrokkene.organisatienaam)
        self.assertEqual(expand["initiator"], self.betrokkene.initiator)
        self.assertEqual(expand["wasPartij"]["uuid"], str(self.partij.uuid))
        self.assertTrue(expand["_expand"])

        # second expand
        expand = expand["_expand"]["wasPartij"]

        self.assertEqual(expand["nummer"], self.partij.nummer)
        self.assertEqual(expand["interneNotitie"], self.partij.interne_notitie)
        self.assertEqual(
            expand["digitaleAdressen"][0]["uuid"], str(self.digitaal_adres.uuid)
        )
        self.assertEqual(expand["soortPartij"], self.partij.soort_partij)
        self.assertEqual(
            expand["indicatieGeheimhouding"], self.partij.indicatie_geheimhouding
        )
        self.assertEqual(expand["voorkeurstaal"], self.partij.voorkeurstaal)
        self.assertEqual(expand["indicatieActief"], self.partij.indicatie_actief)
        self.assertEqual(
            expand["bezoekadres"],
            {
                "nummeraanduidingId": self.partij.bezoekadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.partij.bezoekadres_adresregel1,
                "adresregel2": self.partij.bezoekadres_adresregel2,
                "adresregel3": self.partij.bezoekadres_adresregel3,
                "land": self.partij.bezoekadres_land,
            },
        )
        self.assertEqual(
            expand["correspondentieadres"],
            {
                "nummeraanduidingId": self.partij.correspondentieadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.partij.correspondentieadres_adresregel1,
                "adresregel2": self.partij.correspondentieadres_adresregel2,
                "adresregel3": self.partij.correspondentieadres_adresregel3,
                "land": self.partij.correspondentieadres_land,
            },
        )

    def test_detail_empty_expansion(self):
        klantcontact = KlantcontactFactory.create()
        self.assertEqual(klantcontact.betrokkene_set.count(), 0)
        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(klantcontact.uuid)},
        )
        response = self.client.get(detail_url, {"expand": "hadBetrokkenen"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["_expand"], {"hadBetrokkenen": []})

    def test_detail_single_expansion(self):
        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(self.klantcontact.uuid)},
        )
        response = self.client.get(detail_url, {"expand": "hadBetrokkenen"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["hadBetrokkenen"][0]["uuid"], str(self.betrokkene.uuid))
        self.assertTrue(data["_expand"])
        expand = data["_expand"]["hadBetrokkenen"][0]

        self.assertEqual(
            expand["bezoekadres"],
            {
                "nummeraanduidingId": self.betrokkene.bezoekadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.betrokkene.bezoekadres_adresregel1,
                "adresregel2": self.betrokkene.bezoekadres_adresregel2,
                "adresregel3": self.betrokkene.bezoekadres_adresregel3,
                "land": self.betrokkene.bezoekadres_land,
            },
        )
        self.assertEqual(
            expand["correspondentieadres"],
            {
                "nummeraanduidingId": self.betrokkene.correspondentieadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.betrokkene.correspondentieadres_adresregel1,
                "adresregel2": self.betrokkene.correspondentieadres_adresregel2,
                "adresregel3": self.betrokkene.correspondentieadres_adresregel3,
                "land": self.betrokkene.correspondentieadres_land,
            },
        )
        self.assertEqual(
            expand["contactnaam"],
            {
                "voorletters": self.betrokkene.contactnaam_voorletters,
                "voornaam": self.betrokkene.contactnaam_voornaam,
                "voorvoegselAchternaam": self.betrokkene.contactnaam_voorvoegsel_achternaam,
                "achternaam": self.betrokkene.contactnaam_achternaam,
            },
        )
        self.assertEqual(expand["rol"], self.betrokkene.rol)
        self.assertEqual(expand["organisatienaam"], self.betrokkene.organisatienaam)
        self.assertEqual(expand["initiator"], self.betrokkene.initiator)
        self.assertEqual(expand["wasPartij"]["uuid"], str(self.partij.uuid))

    def test_detail_multiple_level_expansion(self):
        detail_url = reverse(
            "klantinteracties:klantcontact-detail",
            kwargs={"uuid": str(self.klantcontact.uuid)},
        )
        response = self.client.get(
            detail_url, {"expand": "hadBetrokkenen,hadBetrokkenen.wasPartij"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["hadBetrokkenen"][0]["uuid"], str(self.betrokkene.uuid))
        self.assertTrue(data["_expand"])
        expand = data["_expand"]["hadBetrokkenen"][0]

        self.assertEqual(
            expand["bezoekadres"],
            {
                "nummeraanduidingId": self.betrokkene.bezoekadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.betrokkene.bezoekadres_adresregel1,
                "adresregel2": self.betrokkene.bezoekadres_adresregel2,
                "adresregel3": self.betrokkene.bezoekadres_adresregel3,
                "land": self.betrokkene.bezoekadres_land,
            },
        )
        self.assertEqual(
            expand["correspondentieadres"],
            {
                "nummeraanduidingId": self.betrokkene.correspondentieadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.betrokkene.correspondentieadres_adresregel1,
                "adresregel2": self.betrokkene.correspondentieadres_adresregel2,
                "adresregel3": self.betrokkene.correspondentieadres_adresregel3,
                "land": self.betrokkene.correspondentieadres_land,
            },
        )
        self.assertEqual(
            expand["contactnaam"],
            {
                "voorletters": self.betrokkene.contactnaam_voorletters,
                "voornaam": self.betrokkene.contactnaam_voornaam,
                "voorvoegselAchternaam": self.betrokkene.contactnaam_voorvoegsel_achternaam,
                "achternaam": self.betrokkene.contactnaam_achternaam,
            },
        )
        self.assertEqual(expand["rol"], self.betrokkene.rol)
        self.assertEqual(expand["organisatienaam"], self.betrokkene.organisatienaam)
        self.assertEqual(expand["initiator"], self.betrokkene.initiator)
        self.assertEqual(expand["wasPartij"]["uuid"], str(self.partij.uuid))
        self.assertTrue(expand["_expand"])

        # second expand
        expand = expand["_expand"]["wasPartij"]

        self.assertEqual(expand["nummer"], self.partij.nummer)
        self.assertEqual(expand["interneNotitie"], self.partij.interne_notitie)
        self.assertEqual(
            expand["digitaleAdressen"][0]["uuid"], str(self.digitaal_adres.uuid)
        )
        self.assertEqual(expand["soortPartij"], self.partij.soort_partij)
        self.assertEqual(
            expand["indicatieGeheimhouding"], self.partij.indicatie_geheimhouding
        )
        self.assertEqual(expand["voorkeurstaal"], self.partij.voorkeurstaal)
        self.assertEqual(expand["indicatieActief"], self.partij.indicatie_actief)
        self.assertEqual(
            expand["bezoekadres"],
            {
                "nummeraanduidingId": self.partij.bezoekadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.partij.bezoekadres_adresregel1,
                "adresregel2": self.partij.bezoekadres_adresregel2,
                "adresregel3": self.partij.bezoekadres_adresregel3,
                "land": self.partij.bezoekadres_land,
            },
        )
        self.assertEqual(
            expand["correspondentieadres"],
            {
                "nummeraanduidingId": self.partij.correspondentieadres_nummeraanduiding_id,
                "straatnaam": self.betrokkene.correspondentieadres_straatnaam,
                "huisnummer": self.betrokkene.correspondentieadres_huisnummer,
                "huisnummertoevoeging": self.betrokkene.correspondentieadres_huisnummertoevoeging,
                "postcode": self.betrokkene.correspondentieadres_postcode,
                "stad": self.betrokkene.correspondentieadres_stad,
                "adresregel1": self.partij.correspondentieadres_adresregel1,
                "adresregel2": self.partij.correspondentieadres_adresregel2,
                "adresregel3": self.partij.correspondentieadres_adresregel3,
                "land": self.partij.correspondentieadres_land,
            },
        )
