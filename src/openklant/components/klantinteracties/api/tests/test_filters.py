from uuid import uuid4

from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories.actoren import (
    ActorFactory,
    ActorKlantcontactFactory,
)
from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.internetaken import (
    InterneTaakFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
    KlantcontactFactory,
    OnderwerpobjectFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    CategorieFactory,
    CategorieRelatieFactory,
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
            url = f"https://testserver.com/klantinteracties/api/v1/klantcontact/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"hadBetrokkene__wasPartij__url": url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"hadBetrokkene__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            response = self.client.get(
                self.url,
                {
                    "hadBetrokkene__url": f"https://testserver.com/klantinteracties/api/v1/klantcontact/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"hadBetrokkene__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            url = f"https://testserver.com/klantinteracties/api/v1/onderwerpobjecten/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"onderwerpobject__url": url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"onderwerpobject__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            url = f"https://testserver.com/klantinteracties/api/v1/onderwerpobjecten/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"wasOnderwerpobject__url": url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"wasOnderwerpobject__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
            url = f"https://testserver.com/klantinteracties/api/v1/klantcontact/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"hadKlantcontact__url": url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"hadKlantcontact__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        with self.subTest("invalid_url_results_in_400"):
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
            none_existing_url = f"https://testserver.com/klantinteracties/api/v1/digitaal_adres/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"verstrektedigitaalAdres__url": none_existing_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"verstrektedigitaalAdres__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        with self.subTest("invalid_url_results_in_400"):
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
            response = self.client.get(
                self.url,
                {
                    "wasPartij__url": f"https://testserver.com/klantinteracties/api/v1/partij/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"wasPartij__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        with self.subTest("invalid_url_results_in_400"):
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
            partij_url = f"https://testserver.com/klantinteracties/api/v1/partijen/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"vertegenwoordigdePartij__url": partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"vertegenwoordigdePartij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_partij_identificator_code_objecttype(self):
        partij, partij2 = PartijFactory.create_batch(2)
        PartijIdentificatorFactory.create(
            partij=partij, partij_identificator_code_objecttype="one"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_objecttype="two"
        )

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__codeObjecttype": "two"},
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
            partij=partij, partij_identificator_code_soort_object_id="one"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_soort_object_id="two"
        )

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__codeSoortObjectId": "one"},
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
            partij=partij, partij_identificator_object_id="one"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_object_id="two"
        )

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__objectId": "one"},
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
            partij=partij, partij_identificator_code_register="one"
        )
        PartijIdentificatorFactory.create(
            partij=partij2, partij_identificator_code_register="two"
        )

        with self.subTest("happy flow"):
            response = self.client.get(
                self.url,
                {"partijIdentificator__code_register": "two"},
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
            response = self.client.get(
                self.url,
                {
                    "partij__url": f"https://testserver.com/klantinteracties/api/v1/partijen/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"partij__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        with self.subTest("invalid_url_results_in_400"):
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
            response = self.client.get(
                self.url,
                {
                    "categorie__url": f"https://testserver.com/klantinteracties/api/v1/categorieen/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"categorie__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        with self.subTest("invalid_url_results_in_400"):
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
            url = f"https://testserver.com/klantinteracties/api/v1/klantcontacten/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"klantcontact__url": url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"klantcontact__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            response = self.client.get(
                self.url,
                {
                    "actor__url": f"https://testserver.com/klantinteracties/api/v1/klantcontacten/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(self.url, {"actor__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
            vertegenwoordigde_partij_url = f"https://testserver.com/klantinteracties/api/v1/partijen/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"vertegenwoordigendePartij__url": vertegenwoordigde_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"vertegenwoordigendePartij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            partij_url = f"https://testserver.com/klantinteracties/api/v1/partijen/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"vertegenwoordigdePartij__url": partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"vertegenwoordigdePartij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
            response = self.client.get(
                self.url,
                {
                    "toegewezenAanActor__url": f"https://testserver.com/klantinteracties/api/v1/actoren/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"toegewezenAanActor__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            klantcontacten_url = f"https://testserver.com/klantinteracties/api/v1/klantcontacten/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"aanleidinggevendKlantcontact__url": klantcontacten_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"aanleidinggevendKlantcontact__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
            betrokkene_url = f"https://testserver.com/klantinteracties/api/v1/betrokkenen/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"verstrektDoorBetrokkene__url": betrokkene_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"verstrektDoorBetrokkene__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            url = f"https://testserver.com/klantinteracties/api/v1/partijen/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"verstrektDoorPartij__url": url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_url_results_in_400"):
            response = self.client.get(
                self.url, {"verstrektDoorPartij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
