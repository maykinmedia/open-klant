from uuid import uuid4

from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
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
)
from openklant.components.token.tests.api_testcase import APITestCase


class KlantcontactFilterSetTests(APITestCase):
    url = reverse("klantinteracties:klantcontact-list")

    def setUp(self):
        super().setUp()
        (
            self.klantcontact,
            self.klantcontact2,
            self.klantcontact3,
            self.klantcontact4,
            self.klantcontact5,
        ) = KlantcontactFactory.create_batch(5)
        for betrokkene_klantcontact in [
            self.klantcontact,
            self.klantcontact2,
            self.klantcontact3,
            self.klantcontact4,
            self.klantcontact5,
        ]:
            self.betrokkene = BetrokkeneFactory.create(
                klantcontact=betrokkene_klantcontact
            )

        self.onderwerpobject = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact,
            objectidentificator_objecttype="1",
            objectidentificator_soort_object_id="1",
            objectidentificator_object_id="1",
            objectidentificator_register="1",
        )
        self.onderwerpobject2 = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact2,
            objectidentificator_objecttype="2",
            objectidentificator_soort_object_id="2",
            objectidentificator_object_id="2",
            objectidentificator_register="2",
        )
        self.onderwerpobject3 = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact3,
            objectidentificator_objecttype="3",
            objectidentificator_soort_object_id="3",
            objectidentificator_object_id="3",
            objectidentificator_register="3",
        )
        self.onderwerpobject4 = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact4,
            objectidentificator_objecttype="4",
            objectidentificator_soort_object_id="4",
            objectidentificator_object_id="4",
            objectidentificator_register="4",
        )
        self.onderwerpobject5 = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact5,
            objectidentificator_objecttype="5",
            objectidentificator_soort_object_id="5",
            objectidentificator_object_id="5",
            objectidentificator_register="5",
        )

    def test_filter_betrokkene_uuid(self):
        response = self.client.get(
            self.url, {"had_betrokkene__uuid": f"{self.betrokkene.uuid}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_empty_query"):
            response = self.client.get(self.url, {"had_betrokkene__uuid": str(uuid4())})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"had_betrokkene__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_betrokkene_url(self):
        response = self.client.get(
            self.url,
            {
                "had_betrokkene__url": f"http://testserver/klantinteracties/api/v1/klantcontact/{self.betrokkene.uuid}"
            },
        )
        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "had_betrokkene__url": f"http://testserver/klantinteracties/api/v1/klantcontact/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"had_betrokkene__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_onderwerpobject_uuid(self):
        response = self.client.get(
            self.url, {"onderwerpobject__uuid": f"{self.onderwerpobject5.uuid}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_empty_query"):
            response = self.client.get(
                self.url, {"onderwerpobject__uuid": str(uuid4())}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"onderwerpobject__uuid": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_onderwerpobject__url(self):
        url = f"http://testserver/klantinteracties/api/v1/onderwerpobjecten/{self.onderwerpobject5.uuid}"
        response = self.client.get(
            self.url,
            {"onderwerpobject__url": url},
        )
        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            url = f"http://testserver/klantinteracties/api/v1/onderwerpobjecten/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"onderwerpobject__url": url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"onderwerpobject__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_onderwerpobject_objectidentificator_objecttype(self):
        response = self.client.get(
            self.url,
            {"onderwerpobject__objectidentificator_objecttype": "5"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"onderwerpobject__objectidentificator_objecttype": "lorum impsum"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_onderwerpobject_objectidentificator_soort_object_id(self):
        response = self.client.get(
            self.url,
            {"onderwerpobject__objectidentificator_soort_object_id": "5"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "onderwerpobject__objectidentificator_soort_object_id": "lorum impsum"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_objectidentificator_object_id(self):
        response = self.client.get(
            self.url,
            {"onderwerpobject__objectidentificator_object_id": "5"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"onderwerpobject__objectidentificator_object_id": "lorum impsum"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_objectidentificator_register(self):
        response = self.client.get(
            self.url,
            {"onderwerpobject__objectidentificator_register": "5"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"onderwerpobject__objectidentificator_register": "lorum impsum"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class BetrokkeneFilterSetTests(APITestCase):
    url = reverse("klantinteracties:betrokkene-list")

    def setUp(self):
        super().setUp()
        self.klantcontact = KlantcontactFactory.create(nummer="6237172371")
        self.partij = PartijFactory.create(nummer="8123973457")
        self.betrokkene = BetrokkeneFactory.create(
            partij=self.partij, klantcontact=self.klantcontact
        )
        self.digitaal_adres = DigitaalAdresFactory.create(
            betrokkene=self.betrokkene, adres="search_param_adres"
        )

        partij2 = PartijFactory.create()
        betrokkene2 = BetrokkeneFactory.create(partij=partij2)
        DigitaalAdresFactory.create(betrokkene=betrokkene2)

        partij3 = PartijFactory.create()
        betrokkene3 = BetrokkeneFactory.create(partij=partij3)
        DigitaalAdresFactory.create(betrokkene=betrokkene3)

        partij4 = PartijFactory.create()
        betrokkene4 = BetrokkeneFactory.create(partij=partij4)
        DigitaalAdresFactory.create(betrokkene=betrokkene4)

        partij5 = PartijFactory.create()
        betrokkene5 = BetrokkeneFactory.create(partij=partij5)
        DigitaalAdresFactory.create(betrokkene=betrokkene5)

    def test_filter_klantcontact_url(self):
        response = self.client.get(
            self.url,
            {
                "klantcontact__url": f"http://testserver/klantinteracties/api/v1/klantcontact/{self.klantcontact.uuid}"
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "klantcontact__url": f"http://testserver/klantinteracties/api/v1/klantcontact/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"klantcontact__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_klantcontact_uuid(self):
        response = self.client.get(
            self.url,
            {"klantcontact__uuid": str(self.klantcontact.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"klantcontact__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"klantcontact__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_klantcontact_nummer(self):
        response = self.client.get(
            self.url,
            {"klantcontact__nummer": str(6237172371)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"klantcontact__nummer": "8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrektedigitaal_adres_url(self):
        digitaal_adres_url = f"http://testserver/klantinteracties/api/v1/digitaal_adres/{self.digitaal_adres.uuid}"
        response = self.client.get(
            self.url,
            {"verstrektedigitaal_adres__url": digitaal_adres_url},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            none_existing_url = f"http://testserver/klantinteracties/api/v1/digitaal_adres/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"verstrektedigitaal_adres__url": none_existing_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"verstrektedigitaal_adres__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrektedigitaal_adres_uuid(self):
        response = self.client.get(
            self.url,
            {"verstrektedigitaal_adres__uuid": str(self.digitaal_adres.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"verstrektedigitaal_adres__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"verstrektedigitaal_adres__uuid": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_verstrektedigitaal_adres_adres(self):
        response = self.client.get(
            self.url,
            {"verstrektedigitaal_adres__adres": "search_param_adres"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"verstrektedigitaal_adres__adres": "none_existing_adres"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_url(self):
        response = self.client.get(
            self.url,
            {
                "was_partij__url": f"http://testserver/klantinteracties/api/v1/partij/{self.partij.uuid}"
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "was_partij__url": f"http://testserver/klantinteracties/api/v1/partij/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"was_partij__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_uuid(self):
        response = self.client.get(
            self.url,
            {"was_partij__uuid": str(self.partij.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"was_partij__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"was_partij__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_was_partij_nummer(self):
        response = self.client.get(
            self.url,
            {"was_partij__nummer": "8123973457"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.betrokkene.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"was_partij__nummer": "2348238482"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class PartijFilterSetTests(APITestCase):
    url = reverse("klantinteracties:partij-list")

    def setUp(self):
        super().setUp()
        self.partij = PartijFactory.create(nummer="1111111111")
        self.partij2 = PartijFactory.create(
            vertegenwoordigde=(self.partij,), nummer="2222222222"
        )
        self.partij3 = PartijFactory.create(
            vertegenwoordigde=(self.partij2,), nummer="3333333333"
        )
        self.partij4 = PartijFactory.create(
            vertegenwoordigde=(self.partij3,), nummer="4444444444"
        )
        self.partij5 = PartijFactory.create(
            vertegenwoordigde=(self.partij4,), nummer="5555555555"
        )

        for partij_obj in [
            self.partij,
            self.partij2,
            self.partij3,
            self.partij4,
            self.partij5,
        ]:
            self.partij_identificator = PartijIdentificatorFactory.create(
                partij=partij_obj,
                partij_identificator_objecttype=f"objecttype-{partij_obj.nummer}",
                partij_identificator_soort_object_id=f"soort-object-id-{partij_obj.nummer}",
                partij_identificator_object_id=f"object-id-{partij_obj.nummer}",
                partij_identificator_register=f"register-{partij_obj.nummer}",
            )

        self.categorie = CategorieFactory.create(naam="een")
        self.categorie2 = CategorieFactory.create(naam="twee")
        self.categorie3 = CategorieFactory.create(naam="drie")
        self.categorie4 = CategorieFactory.create(naam="vier")
        self.categorie5 = CategorieFactory.create(naam="vijf")

        self.categorie_relatie = CategorieRelatieFactory.create(
            partij=self.partij, categorie=self.categorie
        )
        self.categorie_relatie2 = CategorieRelatieFactory.create(
            partij=self.partij2, categorie=self.categorie2
        )
        self.categorie_relatie3 = CategorieRelatieFactory.create(
            partij=self.partij3, categorie=self.categorie3
        )
        self.categorie_relatie4 = CategorieRelatieFactory.create(
            partij=self.partij4, categorie=self.categorie4
        )
        self.categorie_relatie5 = CategorieRelatieFactory.create(
            partij=self.partij5, categorie=self.categorie5
        )

    def test_filter_werkt_voor_partij_url(self):
        werkt_voor_partij_url = f"http://testserver/klantinteracties/api/v1/partijen/{str(self.partij4.uuid)}"
        response = self.client.get(
            self.url,
            {"werkt_voor_partij__url": werkt_voor_partij_url},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(2, len(data))
        self.assertEqual(str(self.partij5.uuid), data[0]["uuid"])
        self.assertEqual(str(self.partij3.uuid), data[1]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "werkt_voor_partij__url": f"http://testserver/klantinteracties/api/v1/partijen/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"werkt_voor_partij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_werkt_voor_partij_uuid(self):
        response = self.client.get(
            self.url,
            {"werkt_voor_partij__uuid": str(self.partij4.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(2, len(data))
        self.assertEqual(str(self.partij5.uuid), data[0]["uuid"])
        self.assertEqual(str(self.partij3.uuid), data[1]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"werkt_voor_partij__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"werkt_voor_partij__uuid": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_werkt_voor_partij_nummer(self):
        response = self.client.get(
            self.url,
            {"werkt_voor_partij__nummer": "4444444444"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(2, len(data))
        self.assertEqual(str(self.partij5.uuid), data[0]["uuid"])
        self.assertEqual(str(self.partij3.uuid), data[1]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"werkt_voor_partij__nummer": "8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_identificator_nummer(self):
        response = self.client.get(
            self.url,
            {"partij_identificator__objecttype": f"objecttype-{self.partij5.nummer}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.partij5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partij_identificator__objecttype": "objecttype-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_identificator_soort_object_id(self):
        response = self.client.get(
            self.url,
            {
                "partij_identificator__soort_object_id": f"soort-object-id-{self.partij5.nummer}"
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.partij5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partij_identificator__soort_object_id": "soort-object-id-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_identificator_object_id(self):
        response = self.client.get(
            self.url,
            {"partij_identificator__object_id": f"object-id-{self.partij5.nummer}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.partij5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partij_identificator__soort_object_id": "object-id-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_identificator_register(self):
        response = self.client.get(
            self.url,
            {"partij_identificator__register": f"register-{self.partij5.nummer}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.partij5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partij_identificator__register": "register-8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_categorie_relaties_categorie_naam(self):
        response = self.client.get(
            self.url,
            {"categorierelatie__categorie__naam": self.categorie5.naam},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.partij5.uuid), data[0]["uuid"])

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
                {
                    "categorierelatie__categorie__naam": f"{self.categorie.naam},{self.categorie2.naam}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()["results"]

            self.assertEqual(2, len(data))
            self.assertEqual(str(self.partij2.uuid), data[0]["uuid"])
            self.assertEqual(str(self.partij.uuid), data[1]["uuid"])


class CategorieRelatieFiltersetTests(APITestCase):
    url = reverse("klantinteracties:categorierelatie-list")

    def setUp(self):
        super().setUp()
        self.partij = PartijFactory.create(nummer="1111111111")
        self.partij2 = PartijFactory.create(nummer="2222222222")
        self.partij3 = PartijFactory.create(nummer="3333333333")
        self.partij4 = PartijFactory.create(nummer="4444444444")
        self.partij5 = PartijFactory.create(nummer="5555555555")

        self.categorie = CategorieFactory.create(naam="een")
        self.categorie2 = CategorieFactory.create(naam="twee")
        self.categorie3 = CategorieFactory.create(naam="drie")
        self.categorie4 = CategorieFactory.create(naam="vier")
        self.categorie5 = CategorieFactory.create(naam="vijf")

        self.categorie_relatie = CategorieRelatieFactory.create(
            partij=self.partij, categorie=self.categorie
        )
        self.categorie_relatie2 = CategorieRelatieFactory.create(
            partij=self.partij2, categorie=self.categorie2
        )
        self.categorie_relatie3 = CategorieRelatieFactory.create(
            partij=self.partij3, categorie=self.categorie3
        )
        self.categorie_relatie4 = CategorieRelatieFactory.create(
            partij=self.partij4, categorie=self.categorie4
        )
        self.categorie_relatie5 = CategorieRelatieFactory.create(
            partij=self.partij5, categorie=self.categorie5
        )

    def test_filter_partij_url(self):
        partij_url = f"http://testserver/klantinteracties/api/v1/partijen/{str(self.partij5.uuid)}"
        response = self.client.get(
            self.url,
            {"partij__url": partij_url},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.categorie_relatie5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "partij__url": f"http://testserver/klantinteracties/api/v1/partijen/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"partij__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_uuid(self):
        response = self.client.get(
            self.url,
            {"partij__uuid": str(self.partij5.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.categorie_relatie5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partij__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"partij__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_partij_nummer(self):
        response = self.client.get(
            self.url,
            {"partij__nummer": "5555555555"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.categorie_relatie5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"partij__nummer": "8584395394"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_categorie_url(self):
        categorie_url = f"http://testserver/klantinteracties/api/v1/categorieen/{str(self.categorie5.uuid)}"
        response = self.client.get(
            self.url,
            {"categorie__url": categorie_url},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.categorie_relatie5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "categorie__url": f"http://testserver/klantinteracties/api/v1/categorieen/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"categorie__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_categorie_uuid(self):
        response = self.client.get(
            self.url,
            {"categorie__uuid": str(self.categorie5.uuid)},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.categorie_relatie5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"categorie__uuid": str(uuid4())},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"categorie__uuid": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_categorie_naam(self):
        response = self.client.get(
            self.url,
            {"categorie__naam": "vijf"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.categorie_relatie5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {"categorie__naam": "zes"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)
