import requests_mock
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from openklant.components.klanten.datamodel.constants import KlantType, SoortRechtsvorm
from openklant.components.klanten.datamodel.models import Klant
from openklant.components.klanten.datamodel.tests.factories import (
    KlantAdresFactory,
    KlantFactory,
    NatuurlijkPersoonFactory,
    NietNatuurlijkPersoonFactory,
    SubVerblijfBuitenlandFactory,
    VerblijfsAdresFactory,
    VestigingFactory,
)

SUBJECT = "http://example.com/subject/1"


class KlantTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True
    maxDiff = None

    def test_list_klanten(self):
        list_url = reverse(Klant)
        KlantFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_klant_url(self):
        klant = KlantFactory.create(
            subject=SUBJECT, subject_type=KlantType.natuurlijk_persoon
        )
        KlantAdresFactory.create(klant=klant)
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": klant.bronorganisatie,
                "klantnummer": klant.klantnummer,
                "bedrijfsnaam": klant.bedrijfsnaam,
                "functie": klant.functie,
                "websiteUrl": klant.website_url,
                "voornaam": klant.voornaam,
                "voorvoegselAchternaam": klant.voorvoegsel_achternaam,
                "achternaam": klant.achternaam,
                "telefoonnummer": klant.telefoonnummer,
                "emailadres": klant.emailadres,
                "adres": {
                    "straatnaam": klant.adres.straatnaam,
                    "huisnummer": klant.adres.huisnummer,
                    "huisletter": klant.adres.huisletter,
                    "huisnummertoevoeging": klant.adres.huisnummertoevoeging,
                    "postcode": klant.adres.postcode,
                    "woonplaatsnaam": klant.adres.woonplaats_naam,
                    "landcode": klant.adres.landcode,
                },
                "subject": SUBJECT,
                "subjectType": KlantType.natuurlijk_persoon,
                "subjectIdentificatie": None,
            },
        )

    def test_read_klant_natuurlijkpersoon(self):
        klant = KlantFactory.create(
            subject=SUBJECT, subject_type=KlantType.natuurlijk_persoon
        )
        KlantAdresFactory.create(klant=klant)
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = VerblijfsAdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(
            natuurlijkpersoon=natuurlijkpersoon
        )
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": klant.bronorganisatie,
                "klantnummer": klant.klantnummer,
                "bedrijfsnaam": klant.bedrijfsnaam,
                "functie": klant.functie,
                "websiteUrl": klant.website_url,
                "voornaam": klant.voornaam,
                "voorvoegselAchternaam": klant.voorvoegsel_achternaam,
                "achternaam": klant.achternaam,
                "telefoonnummer": klant.telefoonnummer,
                "emailadres": klant.emailadres,
                "adres": {
                    "straatnaam": klant.adres.straatnaam,
                    "huisnummer": klant.adres.huisnummer,
                    "huisletter": klant.adres.huisletter,
                    "huisnummertoevoeging": klant.adres.huisnummertoevoeging,
                    "postcode": klant.adres.postcode,
                    "woonplaatsnaam": klant.adres.woonplaats_naam,
                    "landcode": klant.adres.landcode,
                },
                "subject": SUBJECT,
                "subjectType": KlantType.natuurlijk_persoon,
                "subjectIdentificatie": {
                    "inpBsn": natuurlijkpersoon.inp_bsn,
                    "anpIdentificatie": natuurlijkpersoon.anp_identificatie,
                    "inpANummer": natuurlijkpersoon.inp_a_nummer,
                    "geslachtsnaam": natuurlijkpersoon.geslachtsnaam,
                    "voorvoegselGeslachtsnaam": natuurlijkpersoon.voorvoegsel_geslachtsnaam,
                    "voorletters": natuurlijkpersoon.voorletters,
                    "voornamen": natuurlijkpersoon.voornamen,
                    "geslachtsaanduiding": natuurlijkpersoon.geslachtsaanduiding,
                    "geboortedatum": natuurlijkpersoon.geboortedatum,
                    "verblijfsadres": {
                        "aoaIdentificatie": adres.aoa_identificatie,
                        "wplWoonplaatsNaam": adres.woonplaats_naam,
                        "gorOpenbareRuimteNaam": adres.gor_openbare_ruimte_naam,
                        "aoaPostcode": adres.postcode,
                        "aoaHuisnummer": adres.huisnummer,
                        "aoaHuisletter": adres.huisletter,
                        "aoaHuisnummertoevoeging": adres.huisnummertoevoeging,
                        "inpLocatiebeschrijving": adres.inp_locatiebeschrijving,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": buitenland.lnd_landcode,
                        "lndLandnaam": buitenland.lnd_landnaam,
                        "subAdresBuitenland1": buitenland.sub_adres_buitenland_1,
                        "subAdresBuitenland2": buitenland.sub_adres_buitenland_2,
                        "subAdresBuitenland3": buitenland.sub_adres_buitenland_3,
                    },
                },
            },
        )

    def test_read_klant_nietnatuurlijkpersoon(self):
        klant = KlantFactory.create(
            subject=SUBJECT, subject_type=KlantType.niet_natuurlijk_persoon
        )
        KlantAdresFactory.create(klant=klant)
        nietnatuurlijkpersoon = NietNatuurlijkPersoonFactory.create(klant=klant)
        buitenland = SubVerblijfBuitenlandFactory.create(
            nietnatuurlijkpersoon=nietnatuurlijkpersoon
        )
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": klant.bronorganisatie,
                "klantnummer": klant.klantnummer,
                "bedrijfsnaam": klant.bedrijfsnaam,
                "functie": klant.functie,
                "websiteUrl": klant.website_url,
                "voornaam": klant.voornaam,
                "voorvoegselAchternaam": klant.voorvoegsel_achternaam,
                "achternaam": klant.achternaam,
                "telefoonnummer": klant.telefoonnummer,
                "emailadres": klant.emailadres,
                "adres": {
                    "straatnaam": klant.adres.straatnaam,
                    "huisnummer": klant.adres.huisnummer,
                    "huisletter": klant.adres.huisletter,
                    "huisnummertoevoeging": klant.adres.huisnummertoevoeging,
                    "postcode": klant.adres.postcode,
                    "woonplaatsnaam": klant.adres.woonplaats_naam,
                    "landcode": klant.adres.landcode,
                },
                "subject": SUBJECT,
                "subjectType": KlantType.niet_natuurlijk_persoon,
                "subjectIdentificatie": {
                    "innNnpId": nietnatuurlijkpersoon.inn_nnp_id,
                    "annIdentificatie": nietnatuurlijkpersoon.ann_identificatie,
                    "statutaireNaam": nietnatuurlijkpersoon.statutaire_naam,
                    "innRechtsvorm": nietnatuurlijkpersoon.inn_rechtsvorm,
                    "bezoekadres": nietnatuurlijkpersoon.bezoekadres,
                    "subVerblijfBuitenland": {
                        "lndLandcode": buitenland.lnd_landcode,
                        "lndLandnaam": buitenland.lnd_landnaam,
                        "subAdresBuitenland1": buitenland.sub_adres_buitenland_1,
                        "subAdresBuitenland2": buitenland.sub_adres_buitenland_2,
                        "subAdresBuitenland3": buitenland.sub_adres_buitenland_3,
                    },
                },
            },
        )

    def test_read_klant_vestiging(self):
        klant = KlantFactory.create(subject=SUBJECT, subject_type=KlantType.vestiging)
        KlantAdresFactory.create(klant=klant)
        vestiging = VestigingFactory.create(klant=klant)
        adres = VerblijfsAdresFactory.create(vestiging=vestiging)
        buitenland = SubVerblijfBuitenlandFactory.create(vestiging=vestiging)
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": klant.bronorganisatie,
                "klantnummer": klant.klantnummer,
                "bedrijfsnaam": klant.bedrijfsnaam,
                "functie": klant.functie,
                "websiteUrl": klant.website_url,
                "voornaam": klant.voornaam,
                "voorvoegselAchternaam": klant.voorvoegsel_achternaam,
                "achternaam": klant.achternaam,
                "telefoonnummer": klant.telefoonnummer,
                "emailadres": klant.emailadres,
                "adres": {
                    "straatnaam": klant.adres.straatnaam,
                    "huisnummer": klant.adres.huisnummer,
                    "huisletter": klant.adres.huisletter,
                    "huisnummertoevoeging": klant.adres.huisnummertoevoeging,
                    "postcode": klant.adres.postcode,
                    "woonplaatsnaam": klant.adres.woonplaats_naam,
                    "landcode": klant.adres.landcode,
                },
                "subject": SUBJECT,
                "subjectType": KlantType.vestiging,
                "subjectIdentificatie": {
                    "vestigingsNummer": vestiging.vestigings_nummer,
                    "handelsnaam": vestiging.handelsnaam,
                    "verblijfsadres": {
                        "aoaIdentificatie": adres.aoa_identificatie,
                        "wplWoonplaatsNaam": adres.woonplaats_naam,
                        "gorOpenbareRuimteNaam": adres.gor_openbare_ruimte_naam,
                        "aoaPostcode": adres.postcode,
                        "aoaHuisnummer": adres.huisnummer,
                        "aoaHuisletter": adres.huisletter,
                        "aoaHuisnummertoevoeging": adres.huisnummertoevoeging,
                        "inpLocatiebeschrijving": adres.inp_locatiebeschrijving,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": buitenland.lnd_landcode,
                        "lndLandnaam": buitenland.lnd_landnaam,
                        "subAdresBuitenland1": buitenland.sub_adres_buitenland_1,
                        "subAdresBuitenland2": buitenland.sub_adres_buitenland_2,
                        "subAdresBuitenland3": buitenland.sub_adres_buitenland_3,
                    },
                },
            },
        )

    def test_create_klant_url(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Xavier",
            "achternaam": "Jackson",
            "emailadres": "test@gmail.com",
            "adres": {
                "straatnaam": "Keizersgracht",
                "huisnummer": "117",
                "huisletter": "A",
                "postcode": "1015CJ",
                "woonplaatsnaam": "test",
                "landcode": "1234",
            },
            "subjectType": KlantType.natuurlijk_persoon,
            "subject": SUBJECT,
        }

        with requests_mock.Mocker() as m:
            m.get(SUBJECT, json={})
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.bronorganisatie, "950428139")
        self.assertEqual(klant.klantnummer, "1111")
        self.assertEqual(klant.website_url, "http://some.website.com")
        self.assertEqual(klant.voornaam, "Xavier")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "test@gmail.com")
        self.assertEqual(klant.subject, SUBJECT)
        self.assertEqual(klant.adres.straatnaam, "Keizersgracht")

    def test_create_klant_natuurlijkpersoon(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Samuel",
            "achternaam": "Jackson",
            "emailadres": "samuel@jackson.com",
            "adres": {
                "straatnaam": "Keizersgracht",
                "huisnummer": 117,
                "huisletter": "A",
                "postcode": "1015CJ",
                "woonplaatsnaam": "test",
                "landcode": "1234",
            },
            "subjectType": KlantType.natuurlijk_persoon,
            "subjectIdentificatie": {
                "anpIdentificatie": "123",
                "geslachtsnaam": "Jackson2",
                "voornamen": "Samuel2",
                "geboortedatum": "1962-06-28",
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "East Meaganchester",
                    "gorOpenbareRuimteNaam": "New Amsterdam",
                    "aoaHuisnummer": 21,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "ABCD",
                    "lndLandnaam": "Hollywood",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.bronorganisatie, "950428139")
        self.assertEqual(klant.klantnummer, "1111")
        self.assertEqual(klant.website_url, "http://some.website.com")
        self.assertEqual(klant.voornaam, "Samuel")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "samuel@jackson.com")
        self.assertEqual(klant.subject, "")
        self.assertEqual(klant.subject_type, KlantType.natuurlijk_persoon)

        klantadres = klant.adres

        self.assertEqual(klantadres.straatnaam, "Keizersgracht")
        self.assertEqual(klantadres.huisnummer, 117)
        self.assertEqual(klantadres.huisletter, "A")
        self.assertEqual(klantadres.postcode, "1015CJ")
        self.assertEqual(klantadres.woonplaats_naam, "test")
        self.assertEqual(klantadres.landcode, "1234")

        natuurlijkpersoon = klant.natuurlijk_persoon

        self.assertEqual(natuurlijkpersoon.anp_identificatie, "123")
        self.assertEqual(natuurlijkpersoon.geslachtsnaam, "Jackson2")
        self.assertEqual(natuurlijkpersoon.voornamen, "Samuel2")
        self.assertEqual(natuurlijkpersoon.geboortedatum, "1962-06-28")

        verblijfsadres = natuurlijkpersoon.verblijfsadres

        self.assertEqual(verblijfsadres.aoa_identificatie, "1234")
        self.assertEqual(verblijfsadres.woonplaats_naam, "East Meaganchester")
        self.assertEqual(verblijfsadres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(verblijfsadres.huisnummer, 21)

        buitenland = natuurlijkpersoon.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_create_klant_nietnatuurlijkpersoon(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Samuel",
            "achternaam": "Jackson",
            "emailadres": "samuel@jackson.com",
            "subjectType": KlantType.niet_natuurlijk_persoon,
            "subjectIdentificatie": {
                "innNnpId": "314273268",
                "annIdentificatie": "",
                "statutaireNaam": "ACME",
                "innRechtsvorm": SoortRechtsvorm.europese_naamloze_vennootschap,
                "bezoekadres": "Somewhere",
                "subVerblijfBuitenland": {
                    "lndLandcode": "ABCD",
                    "lndLandnaam": "Hollywood",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.bronorganisatie, "950428139")
        self.assertEqual(klant.klantnummer, "1111")
        self.assertEqual(klant.website_url, "http://some.website.com")
        self.assertEqual(klant.voornaam, "Samuel")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "samuel@jackson.com")
        self.assertEqual(klant.subject, "")
        self.assertEqual(klant.subject_type, KlantType.niet_natuurlijk_persoon)

        nietnatuurlijkpersoon = klant.niet_natuurlijk_persoon

        self.assertEqual(nietnatuurlijkpersoon.inn_nnp_id, "314273268")
        self.assertEqual(nietnatuurlijkpersoon.ann_identificatie, "")
        self.assertEqual(nietnatuurlijkpersoon.statutaire_naam, "ACME")
        self.assertEqual(
            nietnatuurlijkpersoon.inn_rechtsvorm,
            SoortRechtsvorm.europese_naamloze_vennootschap,
        )
        self.assertEqual(nietnatuurlijkpersoon.bezoekadres, "Somewhere")

        buitenland = nietnatuurlijkpersoon.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_create_klant_vestiging(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Samuel",
            "achternaam": "Jackson",
            "emailadres": "samuel@jackson.com",
            "subjectType": KlantType.vestiging,
            "subjectIdentificatie": {
                "vestigingsNummer": "123",
                "handelsnaam": ["WB"],
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "East Meaganchester",
                    "gorOpenbareRuimteNaam": "New Amsterdam",
                    "aoaHuisnummer": 21,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "ABCD",
                    "lndLandnaam": "Hollywood",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.bronorganisatie, "950428139")
        self.assertEqual(klant.klantnummer, "1111")
        self.assertEqual(klant.website_url, "http://some.website.com")
        self.assertEqual(klant.voornaam, "Samuel")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "samuel@jackson.com")
        self.assertEqual(klant.subject, "")
        self.assertEqual(klant.subject_type, KlantType.vestiging)

        vestiging = klant.vestiging

        self.assertEqual(vestiging.vestigings_nummer, "123")
        self.assertEqual(vestiging.handelsnaam, ["WB"])

        adres = vestiging.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.huisnummer, 21)

        buitenland = vestiging.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_partial_update_klant_url(self):
        klant = KlantFactory.create(subject=SUBJECT, voornaam="old name")
        detail_url = reverse(klant)

        response = self.client.patch(detail_url, {"voornaam": "new name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.voornaam, "new name")

    def test_partial_update_klant_naturlijkpersoon(self):
        klant = KlantFactory.create(
            subject_type=KlantType.natuurlijk_persoon, subject=SUBJECT
        )
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = VerblijfsAdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(
            natuurlijkpersoon=natuurlijkpersoon
        )
        detail_url = reverse(klant)

        data = {
            "voornaam": "New name",
            "subject": "",
            "subjectIdentificatie": {
                "geslachtsnaam": "New name2",
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "New place",
                    "gorOpenbareRuimteNaam": "New place2",
                    "aoaHuisnummer": 1,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "XXXX",
                    "lndLandnaam": "New land",
                },
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()
        self.assertEqual(klant.voornaam, "New name")
        self.assertEqual(klant.subject, "")

        natuurlijkpersoon.refresh_from_db()
        self.assertEqual(natuurlijkpersoon.geslachtsnaam, "New name2")

        adres.refresh_from_db()
        self.assertEqual(adres.woonplaats_naam, "New place")

        buitenland.refresh_from_db()
        self.assertEqual(buitenland.lnd_landnaam, "New land")

    def test_partial_update_klant_vestiging(self):
        klant = KlantFactory.create(subject_type=KlantType.vestiging)
        detail_url = reverse(klant)

        response = self.client.patch(
            detail_url,
            {
                "subject": "",
                "subjectIdentificatie": {
                    "vestigingsNummer": "123",
                    "handelsnaam": ["WB"],
                    "verblijfsadres": {
                        "aoaIdentificatie": "1234",
                        "wplWoonplaatsNaam": "East Meaganchester",
                        "gorOpenbareRuimteNaam": "New Amsterdam",
                        "aoaHuisnummer": 21,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": "ABCD",
                        "lndLandnaam": "Hollywood",
                    },
                },
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.subject, "")

        vestiging = klant.vestiging

        self.assertEqual(vestiging.vestigings_nummer, "123")
        self.assertEqual(vestiging.handelsnaam, ["WB"])

        adres = vestiging.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.huisnummer, 21)

        buitenland = vestiging.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_partial_update_klant_subject_type_fail(self):
        klant = KlantFactory.create(
            subject=SUBJECT, subject_type=KlantType.natuurlijk_persoon
        )
        detail_url = reverse(klant)

        response = self.client.patch(detail_url, {"subjectType": KlantType.vestiging})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        validation_error = get_validation_errors(response, "subjectType")
        self.assertEqual(validation_error["code"], "wijzigen-niet-toegelaten")

    def test_update_klant_url(self):
        klant = KlantFactory.create(subject=SUBJECT, voornaam="old name")
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        del data["subjectIdentificatie"]
        data["voornaam"] = "new name"

        with requests_mock.Mocker() as m:
            m.get(SUBJECT, json={})
            response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.voornaam, "new name")

    def test_update_klant_naturlijkpersoon(self):
        klant = KlantFactory.create(
            subject_type=KlantType.natuurlijk_persoon, subject=SUBJECT
        )
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = VerblijfsAdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(
            natuurlijkpersoon=natuurlijkpersoon
        )
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        data.update(
            {
                "voornaam": "New name",
                "subject": "",
                "subjectIdentificatie": {
                    "geslachtsnaam": "New name2",
                    "verblijfsadres": {
                        "aoaIdentificatie": "1234",
                        "wplWoonplaatsNaam": "New place",
                        "gorOpenbareRuimteNaam": "New place2",
                        "aoaHuisnummer": 1,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": "XXXX",
                        "lndLandnaam": "New land",
                    },
                },
            }
        )

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()
        self.assertEqual(klant.voornaam, "New name")
        self.assertEqual(klant.subject, "")

        natuurlijkpersoon.refresh_from_db()
        self.assertEqual(natuurlijkpersoon.geslachtsnaam, "New name2")

        adres.refresh_from_db()
        self.assertEqual(adres.woonplaats_naam, "New place")

        buitenland.refresh_from_db()
        self.assertEqual(buitenland.lnd_landnaam, "New land")

    def test_update_klant_nietnaturlijkpersoon(self):
        klant = KlantFactory.create(
            subject_type=KlantType.niet_natuurlijk_persoon, subject=SUBJECT
        )
        nietnatuurlijkpersoon = NietNatuurlijkPersoonFactory.create(klant=klant)
        buitenland = SubVerblijfBuitenlandFactory.create(
            nietnatuurlijkpersoon=nietnatuurlijkpersoon
        )
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        data.update(
            {
                "voornaam": "New name",
                "subject": "",
                "subjectIdentificatie": {
                    "statutaireNaam": "New name2",
                    "subVerblijfBuitenland": {
                        "lndLandcode": "XXXX",
                        "lndLandnaam": "New land",
                    },
                },
            }
        )

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()
        self.assertEqual(klant.voornaam, "New name")
        self.assertEqual(klant.subject, "")

        nietnatuurlijkpersoon.refresh_from_db()
        self.assertEqual(nietnatuurlijkpersoon.statutaire_naam, "New name2")

        buitenland.refresh_from_db()
        self.assertEqual(buitenland.lnd_landnaam, "New land")

    def test_update_klant_vestiging(self):
        klant = KlantFactory.create(subject_type=KlantType.vestiging)
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        data.update(
            {
                "subject": "",
                "subjectIdentificatie": {
                    "vestigingsNummer": "123",
                    "handelsnaam": ["WB"],
                    "verblijfsadres": {
                        "aoaIdentificatie": "1234",
                        "wplWoonplaatsNaam": "East Meaganchester",
                        "gorOpenbareRuimteNaam": "New Amsterdam",
                        "aoaHuisnummer": 21,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": "ABCD",
                        "lndLandnaam": "Hollywood",
                    },
                },
            }
        )

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.subject, "")

        vestiging = klant.vestiging

        self.assertEqual(vestiging.vestigings_nummer, "123")
        self.assertEqual(vestiging.handelsnaam, ["WB"])

        adres = vestiging.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.huisnummer, 21)

        buitenland = vestiging.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_destroy_klant(self):
        klant = KlantFactory.create()
        detail_url = reverse(klant)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Klant.objects.count(), 0)

    def test_pagination_default(self):
        KlantFactory.create_batch(2)
        url = reverse(Klant)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        KlantFactory.create_batch(2)
        url = reverse(Klant)

        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])


class KlantFilterTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True
    maxDiff = None

    def test_filter_bronorganisatie(self):
        KlantFactory.create(bronorganisatie="000000000")
        KlantFactory.create(bronorganisatie="123456782")
        url = reverse(Klant)

        response = self.client.get(url, {"bronorganisatie": "000000000"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["bronorganisatie"], "000000000")

    def test_filter_klantnummer(self):
        KlantFactory.create(klantnummer="123")
        KlantFactory.create(klantnummer="321")
        url = reverse(Klant)

        response = self.client.get(url, {"klantnummer": "321"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["klantnummer"], "321")

    def test_filter_bedrijfsnaam(self):
        KlantFactory.create(bedrijfsnaam="123")
        KlantFactory.create(bedrijfsnaam="321")
        url = reverse(Klant)

        response = self.client.get(url, {"bedrijfsnaam": "321"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["bedrijfsnaam"], "321")

    def test_filter_functie(self):
        KlantFactory.create(functie="123")
        KlantFactory.create(functie="321")
        url = reverse(Klant)

        response = self.client.get(url, {"functie": "321"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["functie"], "321")

    def test_filter_achternaam(self):
        KlantFactory.create(achternaam="123")
        KlantFactory.create(achternaam="321")
        url = reverse(Klant)

        response = self.client.get(url, {"achternaam": "321"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["achternaam"], "321")

    def test_filter_telefoonnummer(self):
        KlantFactory.create(telefoonnummer="123")
        KlantFactory.create(telefoonnummer="321")
        url = reverse(Klant)

        response = self.client.get(url, {"telefoonnummer": "321"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["telefoonnummer"], "321")

    def test_filter_adres__straatnaam(self):
        KlantAdresFactory.create(straatnaam="naam1")
        KlantAdresFactory.create(straatnaam="naam2")

        url = reverse(Klant)

        response = self.client.get(url, {"adres__straatnaam": "naam2"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["adres"]["straatnaam"], "naam2")

    def test_filter_adres__postcode(self):
        KlantAdresFactory.create(postcode="1000AC")
        KlantAdresFactory.create(postcode="1000WR")

        url = reverse(Klant)

        response = self.client.get(url, {"adres__postcode": "1000WR"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["adres"]["postcode"], "1000WR")

    def test_filter_adres__woonplaats_naam(self):
        KlantAdresFactory.create(woonplaats_naam="haarlem")
        KlantAdresFactory.create(woonplaats_naam="maastricht")

        url = reverse(Klant)

        response = self.client.get(url, {"adres__woonplaats_naam": "maastricht"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["adres"]["woonplaatsnaam"], "maastricht")

    def test_filter_adres__landcode(self):
        KlantAdresFactory.create(landcode="9036")
        KlantAdresFactory.create(landcode="7009")

        url = reverse(Klant)

        response = self.client.get(url, {"adres__landcode": "7009"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["adres"]["landcode"], "7009")

    def test_filter_subject(self):
        KlantFactory.create(subject="https://example.com/1")
        KlantFactory.create(subject="https://example.com/2")

        url = reverse(Klant)

        response = self.client.get(url, {"subject": "https://example.com/2"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["subject"], "https://example.com/2")

    def test_filter_subject_type(self):
        KlantFactory.create(subject_type=KlantType.natuurlijk_persoon)
        KlantFactory.create(subject_type=KlantType.niet_natuurlijk_persoon)

        url = reverse(Klant)

        response = self.client.get(
            url, {"subject_type": KlantType.niet_natuurlijk_persoon}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["subjectType"], KlantType.niet_natuurlijk_persoon)

    def test_filter_subject_natuurlijk_persoon__inp_bsn(self):
        klant1, klant2 = KlantFactory.create_batch(
            2, subject="", subject_type=KlantType.natuurlijk_persoon
        )
        NatuurlijkPersoonFactory.create(inp_bsn="123", klant=klant1)
        NatuurlijkPersoonFactory.create(inp_bsn="321", klant=klant2)

        url = reverse(Klant)

        response = self.client.get(url, {"subject_natuurlijkPersoon__inpBsn": "123"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["subjectIdentificatie"]["inpBsn"], "123")

    def test_filter_subject_natuurlijk_persoon_anp_identificatie(self):
        klant1, klant2 = KlantFactory.create_batch(
            2, subject="", subject_type=KlantType.natuurlijk_persoon
        )
        NatuurlijkPersoonFactory.create(anp_identificatie="123", klant=klant1)
        NatuurlijkPersoonFactory.create(anp_identificatie="321", klant=klant2)

        url = reverse(Klant)

        response = self.client.get(
            url, {"subject_natuurlijkPersoon__anpIdentificatie": "123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["subjectIdentificatie"]["anpIdentificatie"], "123")

    def test_filter_subject_natuurlijk_persoon_inp_a_nummer(self):
        klant1, klant2 = KlantFactory.create_batch(
            2, subject="", subject_type=KlantType.natuurlijk_persoon
        )
        NatuurlijkPersoonFactory.create(inp_a_nummer="123", klant=klant1)
        NatuurlijkPersoonFactory.create(inp_a_nummer="321", klant=klant2)

        url = reverse(Klant)

        response = self.client.get(
            url, {"subject_natuurlijkPersoon__inpANummer": "123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["subjectIdentificatie"]["inpANummer"], "123")

    def test_filter_subject_niet_natuurlijk_persoon__inn_nnp_id(self):
        klant1, klant2 = KlantFactory.create_batch(
            2, subject="", subject_type=KlantType.niet_natuurlijk_persoon
        )
        NietNatuurlijkPersoonFactory.create(inn_nnp_id="123", klant=klant1)
        NietNatuurlijkPersoonFactory.create(inn_nnp_id="321", klant=klant2)

        url = reverse(Klant)

        response = self.client.get(
            url, {"subject_nietNatuurlijkPersoon__innNnpId": "123"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["subjectIdentificatie"]["innNnpId"], "123")

    def test_filter_subject_niet_natuurlijk_persoon_anp_identificatie(self):
        klant1, klant2 = KlantFactory.create_batch(
            2, subject="", subject_type=KlantType.niet_natuurlijk_persoon
        )
        NietNatuurlijkPersoonFactory.create(ann_identificatie="123", klant=klant1)
        NietNatuurlijkPersoonFactory.create(ann_identificatie="321", klant=klant2)

        url = reverse(Klant)

        response = self.client.get(
            url, {"subject_nietNatuurlijkPersoon__annIdentificatie": "123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["subjectIdentificatie"]["annIdentificatie"], "123")

    def test_filter_subject_vestiging_vestigings_nummer(self):
        klant1, klant2 = KlantFactory.create_batch(
            2, subject="", subject_type=KlantType.vestiging
        )
        VestigingFactory.create(vestigings_nummer="123", klant=klant1)
        VestigingFactory.create(vestigings_nummer="321", klant=klant2)

        url = reverse(Klant)

        response = self.client.get(url, {"subject_vestiging__vestigingsNummer": "123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["subjectIdentificatie"]["vestigingsNummer"], "123")

    def test_create_klant_subject_url_invalid(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Xavier",
            "achternaam": "Jackson",
            "emailadres": "test@gmail.com",
            "adres": {
                "straatnaam": "Keizersgracht",
                "huisnummer": "117",
                "huisletter": "A",
                "postcode": "1015CJ",
                "woonplaatsnaam": "test",
                "landcode": "1234",
            },
            "subjectType": KlantType.natuurlijk_persoon,
            "subject": "https://example.com/404",
        }

        with requests_mock.Mocker() as m:
            m.get("https://example.com/404", status_code=404)
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Klant.objects.count(), 0)

        error = get_validation_errors(response, "subject")
        self.assertEqual(error["code"], "bad-url")

    def test_update_klant_subject_url_invalid(self):
        klant = KlantFactory.create(subject=SUBJECT, voornaam="old name")
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        del data["subjectIdentificatie"]
        data["subject"] = "https://example.com/404"

        with requests_mock.Mocker() as m:
            m.get("https://example.com/404", status_code=404)
            response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "subject")
        self.assertEqual(error["code"], "bad-url")

    def test_partial_update_klant_subject_url_invalid(self):
        klant = KlantFactory.create(subject=SUBJECT, voornaam="old name")
        detail_url = reverse(klant)

        with requests_mock.Mocker() as m:
            m.get("https://example.com/404", status_code=404)
            response = self.client.patch(
                detail_url, {"subject": "https://example.com/404"}
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "subject")
        self.assertEqual(error["code"], "bad-url")
