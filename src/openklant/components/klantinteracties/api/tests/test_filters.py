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
            was_klantcontact=self.klantcontact5,
            onderwerpobjectidentificator_code_objecttype="1",
            onderwerpobjectidentificator_code_soort_object_id="1",
            onderwerpobjectidentificator_object_id="1",
            onderwerpobjectidentificator_code_register="1",
        )
        self.onderwerpobject2 = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact2,
            was_klantcontact=self.klantcontact,
            onderwerpobjectidentificator_code_objecttype="2",
            onderwerpobjectidentificator_code_soort_object_id="2",
            onderwerpobjectidentificator_object_id="2",
            onderwerpobjectidentificator_code_register="2",
        )
        self.onderwerpobject3 = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact3,
            was_klantcontact=self.klantcontact2,
            onderwerpobjectidentificator_code_objecttype="3",
            onderwerpobjectidentificator_code_soort_object_id="3",
            onderwerpobjectidentificator_object_id="3",
            onderwerpobjectidentificator_code_register="3",
        )
        self.onderwerpobject4 = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact4,
            was_klantcontact=self.klantcontact3,
            onderwerpobjectidentificator_code_objecttype="4",
            onderwerpobjectidentificator_code_soort_object_id="4",
            onderwerpobjectidentificator_object_id="4",
            onderwerpobjectidentificator_code_register="4",
        )
        self.onderwerpobject5 = OnderwerpobjectFactory.create(
            klantcontact=self.klantcontact5,
            was_klantcontact=self.klantcontact4,
            onderwerpobjectidentificator_code_objecttype="5",
            onderwerpobjectidentificator_code_soort_object_id="5",
            onderwerpobjectidentificator_object_id="5",
            onderwerpobjectidentificator_code_register="5",
        )

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

    def test_filter_was_onderwerpobject__url(self):
        url = f"http://testserver/klantinteracties/api/v1/onderwerpobjecten/{self.onderwerpobject5.uuid}"
        response = self.client.get(
            self.url,
            {"was_onderwerpobject__url": url},
        )
        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.klantcontact4.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            url = f"http://testserver/klantinteracties/api/v1/onderwerpobjecten/{str(uuid4())}"
            response = self.client.get(
                self.url,
                {"was_onderwerpobject__url": url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"was_onderwerpobject__url": "ValueError"}
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
        self.partij2 = PartijFactory.create(nummer="2222222222")
        self.partij3 = PartijFactory.create(nummer="3333333333")
        self.partij4 = PartijFactory.create(nummer="4444444444")
        self.partij5 = PartijFactory.create(nummer="5555555555")

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


class ActorKlantcontactFilterSetTests(APITestCase):
    url = reverse("klantinteracties:actorklantcontact-list")

    def setUp(self):
        super().setUp()
        (
            self.actor,
            self.actor2,
            self.actor3,
            self.actor4,
            self.actor5,
        ) = ActorFactory.create_batch(5)
        (
            self.klantcontact,
            self.klantcontact2,
            self.klantcontact3,
            self.klantcontact4,
            self.klantcontact5,
        ) = KlantcontactFactory.create_batch(5)

        self.actor_klantcontact = ActorKlantcontactFactory.create(
            actor=self.actor, klantcontact=self.klantcontact
        )
        self.actor_klantcontact2 = ActorKlantcontactFactory.create(
            actor=self.actor2, klantcontact=self.klantcontact2
        )
        self.actor_klantcontact3 = ActorKlantcontactFactory.create(
            actor=self.actor3, klantcontact=self.klantcontact3
        )
        self.actor_klantcontact4 = ActorKlantcontactFactory.create(
            actor=self.actor4, klantcontact=self.klantcontact4
        )
        self.actor_klantcontact5 = ActorKlantcontactFactory.create(
            actor=self.actor5, klantcontact=self.klantcontact5
        )

    def test_filter_klantcontact_url(self):
        klantcontact_url = f"http://testserver/klantinteracties/api/v1/klantcontacten/{str(self.klantcontact5.uuid)}"
        response = self.client.get(
            self.url,
            {"klantcontact__url": klantcontact_url},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.actor_klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "klantcontact__url": f"http://testserver/klantinteracties/api/v1/klantcontacten/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"klantcontact__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_actor_url(self):
        actor_url = (
            f"http://testserver/klantinteracties/api/v1/actoren/{str(self.actor5.uuid)}"
        )
        response = self.client.get(
            self.url,
            {"actor__url": actor_url},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.actor_klantcontact5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            response = self.client.get(
                self.url,
                {
                    "actor__url": f"http://testserver/klantinteracties/api/v1/klantcontacten/{str(uuid4())}"
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(self.url, {"actor__url": "ValueError"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)


class VertegenwoordigdenFiltersetTests(APITestCase):
    url = reverse("klantinteracties:vertegenwoordigden-list")

    def setUp(self):
        super().setUp()
        self.partij = PartijFactory.create(nummer="1111111111")
        self.partij2 = PartijFactory.create(nummer="2222222222")
        self.partij3 = PartijFactory.create(nummer="3333333333")
        self.partij4 = PartijFactory.create(nummer="4444444444")
        self.partij5 = PartijFactory.create(nummer="5555555555")

        self.vertegenwoordigde = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=self.partij,
            vertegenwoordigde_partij=self.partij2,
        )
        self.vertegenwoordigde2 = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=self.partij2,
            vertegenwoordigde_partij=self.partij3,
        )
        self.vertegenwoordigde3 = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=self.partij3,
            vertegenwoordigde_partij=self.partij4,
        )
        self.vertegenwoordigde4 = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=self.partij4,
            vertegenwoordigde_partij=self.partij5,
        )
        self.vertegenwoordigde5 = VertegenwoordigdenFactory.create(
            vertegenwoordigende_partij=self.partij5,
            vertegenwoordigde_partij=self.partij,
        )

    def test_filter_vertegenwoordigende_partij_url(self):
        partij_url = f"http://testserver/klantinteracties/api/v1/partijen/{str(self.partij5.uuid)}"
        response = self.client.get(
            self.url,
            {"vertegenwoordigende_partij__url": partij_url},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.vertegenwoordigde5.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            vertegenwoordigde_partij_url = (
                f"http://testserver/klantinteracties/api/v1/partijen/{str(uuid4())}"
            )
            response = self.client.get(
                self.url,
                {"vertegenwoordigende_partij__url": vertegenwoordigde_partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"vertegenwoordigende_partij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

    def test_filter_vertegenwoordigde_partij_url(self):
        partij_url = f"http://testserver/klantinteracties/api/v1/partijen/{str(self.partij5.uuid)}"
        response = self.client.get(
            self.url,
            {"vertegenwoordigde_partij__url": partij_url},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]

        self.assertEqual(1, len(data))
        self.assertEqual(str(self.vertegenwoordigde4.uuid), data[0]["uuid"])

        with self.subTest("no_matches_found_return_nothing"):
            partij_url = (
                f"http://testserver/klantinteracties/api/v1/partijen/{str(uuid4())}"
            )
            response = self.client.get(
                self.url,
                {"vertegenwoordigde_partij__url": partij_url},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)

        with self.subTest("invalid_value_returns_empty_query"):
            response = self.client.get(
                self.url, {"vertegenwoordigde_partij__url": "ValueError"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.json()["count"], 0)
