from datetime import date, timedelta
from uuid import uuid4

from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.constants import SoortDigitaalAdres
from openklant.components.klantinteracties.models import Klantcontrol, SoortPartij
from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    ActorKlantcontactFactory,
    BetrokkeneFactory,
    CategorieFactory,
    CategorieRelatieFactory,
    DigitaalAdresFactory,
    InterneTaakFactory,
    KlantcontactFactory,
    OnderwerpobjectFactory,
    PartijFactory,
    PartijIdentificatorFactory,
    VertegenwoordigdenFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class KlantcontactFilterSetTests(APITestCase):
    url = reverse("klantinteracties:klantcontact-list")

    def test_filter_partij_url(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)
        BetrokkeneFactory.create(klantcontact=klantcontact2, partij=partij2)

        with self.subTest("happy flow"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
            )
            full_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url,
                {"hadBetrokkene__wasPartij__url": full_partij_url},
            )
            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(klantcontact.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_party_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url,
                {"hadBetrokkene__wasPartij__url": fake_party_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"hadBetrokkene__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            partij_list_url = reverse("klantinteracties:partij-list")
            fake_party_url = "https://testserver.com" + partij_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"hadBetrokkene__wasPartij__url": fake_party_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_uuid(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)
        BetrokkeneFactory.create(klantcontact=klantcontact2, partij=partij2)

        response = self.client.get(
            self.url,
            {"hadBetrokkene__wasPartij__uuid": str(partij.uuid)},
        )
        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(klantcontact.uuid), data[0]["uuid"])

    def test_filter_partij_partij_identificator_code_objecttype(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_objecttype="natuurlijk_persoon"
        )
        PartijIdentificatorFactory.create(
            partij=partij2,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)
        BetrokkeneFactory.create(klantcontact=klantcontact2, partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {
                    "hadBetrokkene__wasPartij__partijIdentificator__codeObjecttype": "niet_natuurlijk_persoon"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(klantcontact2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "hadBetrokkene__wasPartij__partijIdentificator__codeObjecttype": "objecttype-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_partij_identificator_soort_object_id(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_soort_object_id="bsn"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_soort_object_id="kvk_nummer"
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)
        BetrokkeneFactory.create(klantcontact=klantcontact2, partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {
                    "hadBetrokkene__wasPartij__partijIdentificator__codeSoortObjectId": "bsn"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(klantcontact.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "hadBetrokkene__wasPartij__partijIdentificator__codeSoortObjectId": "soort-object-id-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_partij_identificator_object_id(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij,
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="296648875",
        )
        PartijIdentificatorFactory.create(
            partij=partij2,
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="111222333",
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)
        BetrokkeneFactory.create(klantcontact=klantcontact2, partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {
                    "hadBetrokkene__wasPartij__partijIdentificator__objectId": "296648875"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(klantcontact.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "hadBetrokkene__wasPartij__partijIdentificator__objectId": "object-id-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_partij_identificator_code_register(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_register="brp"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_register="hr"
        )
        BetrokkeneFactory.create(klantcontact=klantcontact, partij=partij)
        BetrokkeneFactory.create(klantcontact=klantcontact2, partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"hadBetrokkene__wasPartij__partijIdentificator__code_register": "hr"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(klantcontact2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "hadBetrokkene__wasPartij__partijIdentificator__codeRegister": "register-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_betrokkene_url(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        betrokkene = BetrokkeneFactory.create(klantcontact=klantcontact)
        BetrokkeneFactory.create(klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            betrokkene_detail_url = reverse(
                "klantinteracties:betrokkene-detail",
                kwargs={"uuid": str(betrokkene.uuid)},
            )
            full_betrokkene_url = "https://testserver.com" + betrokkene_detail_url

            response = self.client.get(
                self.url,
                {"hadBetrokkene__url": full_betrokkene_url},
            )
            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(klantcontact.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            betrokkene_detail_url = reverse(
                "klantinteracties:betrokkene-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_betrokkene_url = "https://testserver.com" + betrokkene_detail_url

            response = self.client.get(
                self.url,
                {"hadBetrokkene__url": fake_betrokkene_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"hadBetrokkene__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            betrokkene_list_url = reverse("klantinteracties:betrokkene-list")
            fake_betrokkene_url = (
                "https://testserver.com" + betrokkene_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"hadBetrokkene__url": fake_betrokkene_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_onderwerpobject__url(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        OnderwerpobjectFactory.create(klantcontact=klantcontact)
        onderwerpobject2 = OnderwerpobjectFactory.create(klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            onderwerpobject_detail_url = reverse(
                "klantinteracties:onderwerpobject-detail",
                kwargs={"uuid": str(onderwerpobject2.uuid)},
            )
            full_onderwerpobject_url = (
                "https://testserver.com" + onderwerpobject_detail_url
            )

            response = self.client.get(
                self.url,
                {"onderwerpobject__url": full_onderwerpobject_url},
            )
            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(klantcontact2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            onderwerpobject_detail_url = reverse(
                "klantinteracties:onderwerpobject-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_onderwerpobject_url = (
                "https://testserver.com" + onderwerpobject_detail_url
            )

            response = self.client.get(
                self.url,
                {"onderwerpobject__url": fake_onderwerpobject_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"onderwerpobject__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            onderwerpobject_list_url = reverse("klantinteracties:onderwerpobject-list")
            fake_onderwerpobject_url = (
                "https://testserver.com" + onderwerpobject_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"onderwerpobject__url": fake_onderwerpobject_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_onderwerpobject__url(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        OnderwerpobjectFactory.create(was_klantcontact=klantcontact)
        onderwerpobject2 = OnderwerpobjectFactory.create(was_klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            was_onderwerpobject_detail_url = reverse(
                "klantinteracties:onderwerpobject-detail",
                kwargs={"uuid": str(onderwerpobject2.uuid)},
            )
            full_was_onderwerpobject_url = (
                "https://testserver.com" + was_onderwerpobject_detail_url
            )

            response = self.client.get(
                self.url,
                {"wasOnderwerpobject__url": full_was_onderwerpobject_url},
            )
            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(klantcontact2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            was_onderwerpobject_detail_url = reverse(
                "klantinteracties:onderwerpobject-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_was_onderwerpobject_url = (
                "https://testserver.com" + was_onderwerpobject_detail_url
            )

            response = self.client.get(
                self.url,
                {"wasOnderwerpobject__url": fake_was_onderwerpobject_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"wasOnderwerpobject__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            was_onderwerpobject_list_url = reverse(
                "klantinteracties:onderwerpobject-list"
            )
            fake_was_onderwerpobject_url = (
                "https://testserver.com" + was_onderwerpobject_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"wasOnderwerpobject__url": fake_was_onderwerpobject_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class BetrokkeneFilterSetTests(APITestCase):
    url = reverse("klantinteracties:betrokkene-list")

    def test_filter_had_klantcontact_url(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        betrokkene = BetrokkeneFactory.create(klantcontact=klantcontact)
        BetrokkeneFactory.create(klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            klantcontact_detail_url = reverse(
                "klantinteracties:klantcontact-detail",
                kwargs={"uuid": str(klantcontact.uuid)},
            )
            full_klantcontact_url = "https://testserver.com" + klantcontact_detail_url

            response = self.client.get(
                self.url,
                {"hadKlantcontact__url": full_klantcontact_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            klantcontact_detail_url = reverse(
                "klantinteracties:klantcontact-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_klantcontact_url = "https://testserver.com" + klantcontact_detail_url

            response = self.client.get(
                self.url,
                {"hadKlantcontact__url": fake_klantcontact_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"hadKlantcontact__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            klantcontact_list_url = reverse("klantinteracties:klantcontact-list")
            fake_klantcontact_url = (
                "https://testserver.com" + klantcontact_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"hadKlantcontact__url": fake_klantcontact_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_had_klantcontact_uuid(self):
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        betrokkene = BetrokkeneFactory.create(klantcontact=klantcontact)
        BetrokkeneFactory.create(klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"hadKlantcontact__uuid": str(klantcontact.uuid)},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"hadKlantcontact__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"hadKlantcontact__uuid": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_had_klantcontact_nummer(self):
        klantcontact = KlantcontactFactory.create(nummer="6237172371")
        klantcontact2 = KlantcontactFactory.create(nummer="9999999999")
        betrokkene = BetrokkeneFactory.create(klantcontact=klantcontact)
        BetrokkeneFactory.create(klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"hadKlantcontact__nummer": str(6237172371)},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"hadKlantcontact__nummer": "8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrektedigitaal_adres_url(self):
        betrokkene = BetrokkeneFactory.create()
        betrokkene2 = BetrokkeneFactory.create()
        digitaal_adres = DigitaalAdresFactory.create(betrokkene=betrokkene)
        DigitaalAdresFactory.create(betrokkene=betrokkene2)

        with self.subTest("happy flow"):
            digitaal_adres_detail_url = reverse(
                "klantinteracties:digitaaladres-detail",
                kwargs={"uuid": str(digitaal_adres.uuid)},
            )
            full_digitaal_adres_url = (
                "https://testserver.com" + digitaal_adres_detail_url
            )

            response = self.client.get(
                self.url,
                {"verstrektedigitaalAdres__url": full_digitaal_adres_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            digitaal_adres_detail_url = reverse(
                "klantinteracties:digitaaladres-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_digitaal_adres_url = (
                "https://testserver.com" + digitaal_adres_detail_url
            )

            response = self.client.get(
                self.url,
                {"verstrektedigitaalAdres__url": fake_digitaal_adres_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"verstrektedigitaalAdres__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            digitaaladres_list_url = reverse("klantinteracties:digitaaladres-list")
            fake_digitaaladres_url = (
                "https://testserver.com" + digitaaladres_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"verstrektedigitaalAdres__url": fake_digitaaladres_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrektedigitaal_adres_uuid(self):
        betrokkene = BetrokkeneFactory.create()
        betrokkene2 = BetrokkeneFactory.create()
        digitaal_adres = DigitaalAdresFactory.create(betrokkene=betrokkene)
        DigitaalAdresFactory.create(betrokkene=betrokkene2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"verstrektedigitaalAdres__uuid": str(digitaal_adres.uuid)},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"verstrektedigitaalAdres__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"verstrektedigitaalAdres__uuid": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_verstrektedigitaal_adres_adres(self):
        betrokkene = BetrokkeneFactory.create()
        betrokkene2 = BetrokkeneFactory.create()
        DigitaalAdresFactory.create(betrokkene=betrokkene, adres="search_param_adres")
        DigitaalAdresFactory.create(betrokkene=betrokkene2, adres="whatever")

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"verstrektedigitaalAdres__adres": "search_param_adres"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"verstrektedigitaalAdres__adres": "none_existing_adres"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_url(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create(partij=partij)
        BetrokkeneFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
            )
            full_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url,
                {"wasPartij__url": full_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(self.url, {"wasPartij__url": fake_partij_url})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"wasPartij__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            partij_list_url = reverse("klantinteracties:partij-list")
            fake_partij_url = "https://testserver.com" + partij_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"wasPartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_uuid(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        betrokkene = BetrokkeneFactory.create(partij=partij)
        BetrokkeneFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"wasPartij__uuid": str(partij.uuid)},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"wasPartij__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"wasPartij__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_was_partij_nummer(self):
        partij = PartijFactory.create(nummer="8123973457")
        partij2 = PartijFactory.create(nummer="9999999999")
        betrokkene = BetrokkeneFactory.create(partij=partij)
        BetrokkeneFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"wasPartij__nummer": "8123973457"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"wasPartij__nummer": "2348238482"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_partij_identificator_code_objecttype(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_objecttype="natuurlijk_persoon"
        )
        PartijIdentificatorFactory.create(
            partij=partij2,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
        )
        BetrokkeneFactory.create(partij=partij)
        betrokkene = BetrokkeneFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {
                    "wasPartij__partijIdentificator__codeObjecttype": "niet_natuurlijk_persoon"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "wasPartij__partijIdentificator__codeObjecttype": "objecttype-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_partij_identificator_soort_object_id(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_soort_object_id="bsn"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_soort_object_id="kvk_nummer"
        )
        betrokkene = BetrokkeneFactory.create(partij=partij)
        BetrokkeneFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"wasPartij__partijIdentificator__codeSoortObjectId": "bsn"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "wasPartij__partijIdentificator__codeSoortObjectId": "soort-object-id-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_partij_identificator_object_id(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij,
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="296648875",
        )
        PartijIdentificatorFactory.create(
            partij=partij2,
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="111222333",
        )
        betrokkene = BetrokkeneFactory.create(partij=partij)
        BetrokkeneFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"wasPartij__partijIdentificator__objectId": "296648875"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"wasPartij__partijIdentificator__objectId": "object-id-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_partij_identificator_code_register(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_register="brp"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_register="hr"
        )
        BetrokkeneFactory.create(partij=partij)
        betrokkene = BetrokkeneFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"wasPartij__partijIdentificator__code_register": "hr"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"wasPartij__partijIdentificator__codeRegister": "register-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_digitale_adressen_inclusion_param(self):
        betrokkene = BetrokkeneFactory.create()
        response = self.client.get(self.url, data={"expand": "digitaleAdressen"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["_expand"], {"digitaleAdressen": []})

        digitaal_adres = DigitaalAdresFactory(
            betrokkene=betrokkene,
            adres="test",
            soort_digitaal_adres="email",
        )

        response = self.client.get(self.url, data={"expand": "digitaleAdressen"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        digitaal_adressen = results[0]["_expand"]["digitaleAdressen"]
        self.assertEqual(len(digitaal_adressen), 1)
        self.assertEqual(digitaal_adressen[0]["uuid"], str(digitaal_adres.uuid))
        self.assertEqual(
            digitaal_adressen[0]["verstrektDoorBetrokkene"]["uuid"],
            str(betrokkene.uuid),
        )


class PartijFilterSetTests(APITestCase):
    url = reverse("klantinteracties:partij-list")

    def test_filter_vertegenwoordigde_partij_url(self):
        partij, partij2, partij3, partij4 = PartijFactory.create_batch(4)
        VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij, vertegenwoordigde_partij=partij3
        )
        VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij2, vertegenwoordigde_partij=partij4
        )

        with self.subTest("happy flow"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
            )
            full_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url, {"vertegenwoordigdePartij__url": full_partij_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(partij3.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url,
                {"vertegenwoordigdePartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"vertegenwoordigdePartij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            partij_list_url = reverse("klantinteracties:partij-list")
            fake_partij_url = "https://testserver.com" + partij_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"vertegenwoordigdePartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_identificator_code_objecttype(self):
        partij, partij2 = PartijFactory.create_batch(2)
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_objecttype="natuurlijk_persoon"
        )
        PartijIdentificatorFactory.create(
            partij=partij2,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
        )

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__codeObjecttype": "niet_natuurlijk_persoon"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(partij2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__codeObjecttype": "objecttype-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_identificator_soort_object_id(self):
        partij, partij2 = PartijFactory.create_batch(2)
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_soort_object_id="bsn"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_soort_object_id="kvk_nummer"
        )

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__codeSoortObjectId": "bsn"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(partij.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "partijIdentificator__codeSoortObjectId": "soort-object-id-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_identificator_object_id(self):
        partij, partij2 = PartijFactory.create_batch(2)
        PartijIdentificatorFactory.create(
            partij=partij,
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="296648875",
        )
        PartijIdentificatorFactory.create(
            partij=partij2,
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="111222333",
        )

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__objectId": "296648875"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(partij.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__objectId": "object-id-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_identificator_code_register(self):
        partij, partij2 = PartijFactory.create_batch(2)
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_register="brp"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_register="hr"
        )

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__code_register": "hr"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(partij2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__codeRegister": "register-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_categorie_relaties_categorie_naam(self):
        partij, partij2 = PartijFactory.create_batch(2)
        categorie = CategorieFactory.create(naam="one")
        categorie2 = CategorieFactory.create(naam="two")
        CategorieRelatieFactory.create(partij=partij, categorie=categorie)
        CategorieRelatieFactory.create(partij=partij2, categorie=categorie2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"categorierelatie__categorie__naam": "two"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(partij2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"categorierelatie__categorie__naam": "zes"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("search_based_on_multiple_categorie_namen"):
            response = self.client.get(
                self.url,
                {"categorierelatie__categorie__naam": "one,two"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(2, len(data))
            self.assertEqual(str(partij2.uuid), data[0]["uuid"])
            self.assertEqual(str(partij.uuid), data[1]["uuid"])


class CategorieRelatieFiltersetTests(APITestCase):
    url = reverse("klantinteracties:categorierelatie-list")

    def test_filter_partij_url(self):
        partij, partij2 = PartijFactory.create_batch(2)
        CategorieRelatieFactory.create(partij=partij)
        categorie_relatie2 = CategorieRelatieFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij2.uuid)}
            )
            full_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(self.url, {"partij__url": full_partij_url})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(categorie_relatie2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url,
                {"partij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"partij__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            partij_list_url = reverse("klantinteracties:partij-list")
            fake_partij_url = "https://testserver.com" + partij_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"partij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_uuid(self):
        partij, partij2 = PartijFactory.create_batch(2)
        categorie_relatie = CategorieRelatieFactory.create(partij=partij)
        CategorieRelatieFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partij__uuid": str(partij.uuid)},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(categorie_relatie.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partij__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"partij__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_partij_nummer(self):
        partij = PartijFactory.create(nummer="1111111111")
        partij2 = PartijFactory.create(nummer="2222222222")
        categorie_relatie = CategorieRelatieFactory.create(partij=partij)
        CategorieRelatieFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partij__nummer": "1111111111"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(categorie_relatie.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partij__nummer": "8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_categorie_url(self):
        categorie = CategorieFactory.create()
        categorie2 = CategorieFactory.create()
        categorie_relatie = CategorieRelatieFactory.create(categorie=categorie)
        CategorieRelatieFactory.create(categorie=categorie2)

        with self.subTest("happy flow"):
            categorie_detail_url = reverse(
                "klantinteracties:categorie-detail",
                kwargs={"uuid": str(categorie.uuid)},
            )
            full_categorie_url = "https://testserver.com" + categorie_detail_url

            response = self.client.get(self.url, {"categorie__url": full_categorie_url})

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(categorie_relatie.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            categorie_detail_url = reverse(
                "klantinteracties:categorie-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_categorie_url = "https://testserver.com" + categorie_detail_url

            response = self.client.get(
                self.url,
                {"categorie__url": fake_categorie_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"categorie__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            categorie_list_url = reverse("klantinteracties:categorie-list")
            fake_categorie_url = (
                "https://testserver.com" + categorie_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"categorie__url": fake_categorie_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_categorie_uuid(self):
        categorie = CategorieFactory.create()
        categorie2 = CategorieFactory.create()
        categorie_relatie = CategorieRelatieFactory.create(categorie=categorie)
        CategorieRelatieFactory.create(categorie=categorie2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"categorie__uuid": str(categorie.uuid)},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(categorie_relatie.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"categorie__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"categorie__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_categorie_naam(self):
        categorie = CategorieFactory.create(naam="one")
        categorie2 = CategorieFactory.create(naam="two")
        CategorieRelatieFactory.create(categorie=categorie)
        categorie_relatie2 = CategorieRelatieFactory.create(categorie=categorie2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"categorie__naam": "two"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(categorie_relatie2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"categorie__naam": "zes"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class ActorKlantcontactFilterSetTests(APITestCase):
    url = reverse("klantinteracties:actorklantcontact-list")

    def test_filter_klantcontact_url(self):
        actor = ActorFactory.create()
        actor2 = ActorFactory.create()
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        actor_klantcontact = ActorKlantcontactFactory.create(
            actor=actor, klantcontact=klantcontact
        )
        ActorKlantcontactFactory.create(actor=actor2, klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            klantcontact_detail_url = reverse(
                "klantinteracties:klantcontact-detail",
                kwargs={"uuid": str(klantcontact.uuid)},
            )
            full_klantcontact_url = "https://testserver.com" + klantcontact_detail_url

            response = self.client.get(
                self.url, {"klantcontact__url": full_klantcontact_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(actor_klantcontact.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            klantcontact_detail_url = reverse(
                "klantinteracties:klantcontact-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_klantcontact_url = "https://testserver.com" + klantcontact_detail_url

            response = self.client.get(
                self.url,
                {"klantcontact__url": fake_klantcontact_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"klantcontact__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            klantcontact_list_url = reverse("klantinteracties:klantcontact-list")
            fake_klantcontact_url = (
                "https://testserver.com" + klantcontact_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"klantcontact__url": fake_klantcontact_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_actor_url(self):
        actor = ActorFactory.create()
        actor2 = ActorFactory.create()
        klantcontact = KlantcontactFactory.create()
        klantcontact2 = KlantcontactFactory.create()
        actor_klantcontact = ActorKlantcontactFactory.create(
            actor=actor, klantcontact=klantcontact
        )
        ActorKlantcontactFactory.create(actor=actor2, klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            actor_detail_url = reverse(
                "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
            )
            full_actor_url = "https://testserver.com" + actor_detail_url

            response = self.client.get(self.url, {"actor__url": full_actor_url})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(actor_klantcontact.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            actor_detail_url = reverse(
                "klantinteracties:actor-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_actor_url = "https://testserver.com" + actor_detail_url

            response = self.client.get(
                self.url,
                {"actor__url": fake_actor_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(self.url, {"actor__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            actor_list_url = reverse("klantinteracties:actor-list")
            fake_actor_url = "https://testserver.com" + actor_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"actor__url": fake_actor_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class VertegenwoordigdenFiltersetTests(APITestCase):
    url = reverse("klantinteracties:vertegenwoordigden-list")

    def test_filter_vertegenwoordigende_partij_url(self):
        partij, partij2, partij3, partij4 = PartijFactory.create_batch(4)

        vertegenwoordigden = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij, vertegenwoordigde_partij=partij3
        )
        VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij2, vertegenwoordigde_partij=partij4
        )

        with self.subTest("happy flow"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
            )
            full_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url, {"vertegenwoordigendePartij__url": full_partij_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(vertegenwoordigden.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url,
                {"vertegenwoordigendePartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"vertegenwoordigendePartij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            partij_list_url = reverse("klantinteracties:partij-list")
            fake_partij_url = "https://testserver.com" + partij_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"vertegenwoordigendePartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_vertegenwoordigde_partij_url(self):
        partij, partij2, partij3, partij4 = PartijFactory.create_batch(4)
        vertegenwoordigden = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij, vertegenwoordigde_partij=partij3
        )
        VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=partij2, vertegenwoordigde_partij=partij4
        )

        with self.subTest("happy flow"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij3.uuid)}
            )
            full_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url, {"vertegenwoordigdePartij__url": full_partij_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(vertegenwoordigden.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url,
                {"vertegenwoordigdePartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"vertegenwoordigdePartij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            partij_list_url = reverse("klantinteracties:partij-list")
            fake_partij_url = "https://testserver.com" + partij_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"vertegenwoordigdePartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class InterneTaakFilterSetTests(APITestCase):
    url = reverse("klantinteracties:internetaak-list")

    def test_filter_toegewezen_aan_actor_url(self):
        actor, actor2 = ActorFactory.create_batch(2)
        internetaak = InterneTaakFactory.create(actoren=[actor])
        InterneTaakFactory.create(actoren=[actor2])

        with self.subTest("happy flow"):
            actor_detail_url = reverse(
                "klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}
            )
            full_actor_url = "https://testserver.com" + actor_detail_url

            response = self.client.get(
                self.url, {"toegewezenAanActor__url": full_actor_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(internetaak.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            actor_detail_url = reverse(
                "klantinteracties:actor-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_actor_url = "https://testserver.com" + actor_detail_url

            response = self.client.get(
                self.url, {"toegewezenAanActor__url": fake_actor_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"toegewezenAanActor__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            actor_list_url = reverse("klantinteracties:actor-list")
            fake_actor_url = "https://testserver.com" + actor_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"toegewezenAanActor__url": fake_actor_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_aanleidinggevend_klantcontact_url(self):
        klantcontact, klantcontact2 = KlantcontactFactory.create_batch(2)
        internetaak = InterneTaakFactory.create(klantcontact=klantcontact)
        InterneTaakFactory.create(klantcontact=klantcontact2)

        with self.subTest("happy flow"):
            klantcontact_detail_url = reverse(
                "klantinteracties:klantcontact-detail",
                kwargs={"uuid": str(klantcontact.uuid)},
            )
            full_klantcontact_url = "https://testserver.com" + klantcontact_detail_url

            response = self.client.get(
                self.url, {"aanleidinggevendKlantcontact__url": full_klantcontact_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(internetaak.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            klantcontact_detail_url = reverse(
                "klantinteracties:klantcontact-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_klantcontact_url = "https://testserver.com" + klantcontact_detail_url

            response = self.client.get(
                self.url,
                {"aanleidinggevendKlantcontact__url": fake_klantcontact_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"aanleidinggevendKlantcontact__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            klantcontact_list_url = reverse("klantinteracties:klantcontact-list")
            fake_klantcontact_url = (
                "https://testserver.com" + klantcontact_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"aanleidinggevendKlantcontact__url": fake_klantcontact_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class DigitaalAdresFilterSetTests(APITestCase):
    url = reverse("klantinteracties:digitaaladres-list")

    def test_filter_verstrekt_door_betrokkene_url(self):
        betrokkene, betrokkene2 = BetrokkeneFactory.create_batch(2)
        DigitaalAdresFactory.create(betrokkene=betrokkene)
        digitaal_adres2 = DigitaalAdresFactory.create(betrokkene=betrokkene2)

        with self.subTest("happy flow"):
            betrokkene_detail_url = reverse(
                "klantinteracties:betrokkene-detail",
                kwargs={"uuid": str(betrokkene2.uuid)},
            )
            full_betrokkene_url = "https://testserver.com" + betrokkene_detail_url

            response = self.client.get(
                self.url, {"verstrektDoorBetrokkene__url": full_betrokkene_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(digitaal_adres2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            betrokkene_detail_url = reverse(
                "klantinteracties:betrokkene-detail",
                kwargs={"uuid": str(uuid4())},
            )
            fake_betrokkene_url = "https://testserver.com" + betrokkene_detail_url

            response = self.client.get(
                self.url,
                {"verstrektDoorBetrokkene__url": fake_betrokkene_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"verstrektDoorBetrokkene__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            betrokkene_list_url = reverse("klantinteracties:betrokkene-list")
            fake_betrokkene_url = (
                "https://testserver.com" + betrokkene_list_url + "/not-a-uuid"
            )

            response = self.client.get(
                self.url,
                {"verstrektDoorBetrokkene__url": fake_betrokkene_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrekt_door_partij_url(self):
        partij, partij2 = PartijFactory.create_batch(2)

        DigitaalAdresFactory.create(partij=partij)
        digitaal_adres2 = DigitaalAdresFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij2.uuid)}
            )
            full_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url, {"verstrektDoorPartij__url": full_partij_url}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(digitaal_adres2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            partij_detail_url = reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(uuid4())}
            )
            fake_partij_url = "https://testserver.com" + partij_detail_url

            response = self.client.get(
                self.url,
                {"verstrektDoorPartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("no url as value restults in 400"):
            response = self.client.get(
                self.url, {"verstrektDoorPartij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest("invalid_uuid_results_nothing"):
            partij_list_url = reverse("klantinteracties:partij-list")
            fake_partij_url = "https://testserver.com" + partij_list_url + "/not-a-uuid"

            response = self.client.get(
                self.url,
                {"verstrektDoorPartij__url": fake_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_verstrekt_door_partij__soort_partij(self):
        partij = PartijFactory(soort_partij=SoortPartij.persoon)
        partij2 = PartijFactory(soort_partij=SoortPartij.organisatie)
        DigitaalAdresFactory.create(partij=partij)
        DigitaalAdresFactory.create(partij=partij2)

        response = self.client.get(
            self.url, {"verstrektDoorPartij__soortPartij": "persoon"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["verstrektDoorPartij"]["uuid"], partij.uuid)

    def test_filter_verstrekt_door_partij_partij_identificator_code_objecttype(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_objecttype="natuurlijk_persoon"
        )
        PartijIdentificatorFactory.create(
            partij=partij2,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
        )
        DigitaalAdresFactory.create(partij=partij)
        digitaal_adres2 = DigitaalAdresFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {
                    "verstrektDoorPartij__partijIdentificator__codeObjecttype": "niet_natuurlijk_persoon"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(digitaal_adres2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "verstrektDoorPartij__partijIdentificator__codeObjecttype": "objecttype-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrekt_door_partij_partij_identificator_soort_object_id(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_soort_object_id="bsn"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_soort_object_id="kvk_nummer"
        )
        digitaal_adres = DigitaalAdresFactory.create(partij=partij)
        DigitaalAdresFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"verstrektDoorPartij__partijIdentificator__codeSoortObjectId": "bsn"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(digitaal_adres.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "verstrektDoorPartij__partijIdentificator__codeSoortObjectId": "soort-object-id-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrekt_door_partij_partij_identificator_object_id(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij,
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="296648875",
        )
        PartijIdentificatorFactory.create(
            partij=partij2,
            partij_identificator_code_soort_object_id="bsn",
            partij_identificator_object_id="111222333",
        )
        digitaal_adres = DigitaalAdresFactory.create(partij=partij)
        DigitaalAdresFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"verstrektDoorPartij__partijIdentificator__objectId": "296648875"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(digitaal_adres.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "verstrektDoorPartij__partijIdentificator__objectId": "object-id-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrekt_door_partij_partij_identificator_code_register(self):
        partij = PartijFactory.create()
        partij2 = PartijFactory.create()
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_register="brp"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_register="hr"
        )
        DigitaalAdresFactory.create(partij=partij)
        digitaal_adres2 = DigitaalAdresFactory.create(partij=partij2)

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"verstrektDoorPartij__partijIdentificator__code_register": "hr"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(1, len(data))
            self.assertEqual(str(digitaal_adres2.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "verstrektDoorPartij__partijIdentificator__codeRegister": "register-8584395394"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_verstrekt_door_betrokkene__rol(self):
        betrokkene = BetrokkeneFactory(rol=Klantcontrol.klant)
        betrokkene2 = BetrokkeneFactory(rol=Klantcontrol.vertegenwoordiger)
        DigitaalAdresFactory.create(betrokkene=betrokkene)
        DigitaalAdresFactory.create(betrokkene=betrokkene2)

        response = self.client.get(self.url, {"verstrektDoorBetrokkene__rol": "klant"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(
            data["results"][0]["verstrektDoorBetrokkene"]["uuid"], betrokkene.uuid
        )

    def test_filter_adres_exact_parameter(self):
        betrokkene, betrokkene2 = BetrokkeneFactory.create_batch(2)
        DigitaalAdresFactory.create(betrokkene=betrokkene, adres="adres_1234")
        DigitaalAdresFactory.create(betrokkene=betrokkene2, adres="adres_5678")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

        response = self.client.get(self.url, {"adres": "adres_1234"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["adres"], "adres_1234")

    def test_filter_adres_icontains_parameter(self):
        betrokkene, betrokkene2 = BetrokkeneFactory.create_batch(2)
        DigitaalAdresFactory.create(betrokkene=betrokkene, adres="adres_1234")
        DigitaalAdresFactory.create(betrokkene=betrokkene2, adres="adres_5678")

        response = self.client.get(self.url, {"adres__icontains": "adres_1234"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["adres"], "adres_1234")

        response = self.client.get(self.url, {"adres__icontains": "adres_5678"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["adres"], "adres_5678")

        response = self.client.get(self.url, {"adres__icontains": "adres"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

    def test_filter_soort_digitaal_adres(self):
        DigitaalAdresFactory.create(soort_digitaal_adres=SoortDigitaalAdres.email)
        DigitaalAdresFactory.create(
            soort_digitaal_adres=SoortDigitaalAdres.telefoonnummer
        )

        response = self.client.get(self.url, {"soortDigitaalAdres": "email"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["soortDigitaalAdres"], "email")

    def test_filter_is_standaard_adres(self):
        DigitaalAdresFactory.create(is_standaard_adres=True)
        DigitaalAdresFactory.create(is_standaard_adres=False)

        response = self.client.get(self.url, {"isStandaardAdres": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["isStandaardAdres"], True)

    def test_filter_referentie_exact_parameter(self):
        DigitaalAdresFactory.create(referentie="referentie-1234")
        DigitaalAdresFactory.create(referentie="referentie-5678")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

        response = self.client.get(self.url, {"referentie": "referentie-1234"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["referentie"], "referentie-1234")

        response = self.client.get(self.url, {"referentie": "referentie-9999"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 0)

        response = self.client.get(self.url, {"referentie": ""})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

    def test_filter_verificatie_datum(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        digitaal_adres_yesterday = DigitaalAdresFactory.create(
            verificatie_datum=yesterday
        )
        digitaal_adres_today = DigitaalAdresFactory.create(verificatie_datum=today)
        digitaal_adres_tomorrow = DigitaalAdresFactory.create(
            verificatie_datum=tomorrow
        )
        DigitaalAdresFactory.create(verificatie_datum=None)

        with self.subTest("exact"):
            response = self.client.get(
                self.url, {"verificatieDatum": today.isoformat()}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(data["results"][0]["uuid"], str(digitaal_adres_today.uuid))

        with self.subTest("gt"):
            response = self.client.get(
                self.url, {"verificatieDatum__gt": today.isoformat()}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(
                data["results"][0]["uuid"], str(digitaal_adres_tomorrow.uuid)
            )

        with self.subTest("gte"):
            response = self.client.get(
                self.url, {"verificatieDatum__gte": today.isoformat()}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 2)
            self.assertEqual(
                data["results"][0]["uuid"], str(digitaal_adres_tomorrow.uuid)
            )
            self.assertEqual(data["results"][1]["uuid"], str(digitaal_adres_today.uuid))

        with self.subTest("lt"):
            response = self.client.get(
                self.url, {"verificatieDatum__lt": today.isoformat()}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(
                data["results"][0]["uuid"], str(digitaal_adres_yesterday.uuid)
            )

        with self.subTest("lte"):
            response = self.client.get(
                self.url, {"verificatieDatum__lte": today.isoformat()}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 2)
            self.assertEqual(data["results"][0]["uuid"], str(digitaal_adres_today.uuid))
            self.assertEqual(
                data["results"][1]["uuid"], str(digitaal_adres_yesterday.uuid)
            )

    def test_filter_is_geverifieerd(self):
        today = date.today()
        yesterday = today - timedelta(days=1)

        digitaal_adres_yesterday = DigitaalAdresFactory.create(
            verificatie_datum=yesterday
        )
        digitaal_adres_today = DigitaalAdresFactory.create(verificatie_datum=today)
        digitaal_adres_not_verified = DigitaalAdresFactory.create(
            verificatie_datum=None
        )

        with self.subTest("isGeverifieerd=true"):
            response = self.client.get(self.url, {"isGeverifieerd": True})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 2)
            self.assertEqual(data["results"][0]["uuid"], str(digitaal_adres_today.uuid))
            self.assertEqual(
                data["results"][1]["uuid"], str(digitaal_adres_yesterday.uuid)
            )

        with self.subTest("isGeverifieerd=false"):
            response = self.client.get(self.url, {"isGeverifieerd": False})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(
                data["results"][0]["uuid"], str(digitaal_adres_not_verified.uuid)
            )
