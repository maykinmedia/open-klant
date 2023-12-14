from uuid import uuid4

from rest_framework import status
from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories.digitaal_adres import (
    DigitaalAdresFactory,
)
from openklant.components.klantinteracties.models.tests.factories.klantcontacten import (
    BetrokkeneFactory,
    KlantcontactFactory,
)
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    PartijFactory,
    PartijIdentificatorFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class KlantcontactFilterTests(APITestCase):
    url = reverse("klantinteracties:klantcontact-list")

    def setUp(self):
        super().setUp()
        (
            klantcontact,
            klantcontact2,
            klantcontact3,
            klantcontact4,
            self.klantcontact5,
        ) = KlantcontactFactory.create_batch(5)
        for betrokkene_klantcontact in [
            klantcontact,
            klantcontact2,
            klantcontact3,
            klantcontact4,
            self.klantcontact5,
        ]:
            self.betrokkene = BetrokkeneFactory.create(
                klantcontact=betrokkene_klantcontact
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


class BetrokkeneFilterTests(APITestCase):
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


class TestPartijFilterset(APITestCase):
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
