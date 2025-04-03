from rest_framework import status
from vng_api_common.tests import get_validation_errors, reverse, reverse_lazy

from openklant.components.klantinteracties.models.partijen import PartijIdentificator
from openklant.components.klantinteracties.models.tests.factories.partijen import (
    BsnPartijIdentificatorFactory,
    KvkNummerPartijIdentificatorFactory,
    PartijFactory,
    PartijIdentificatorFactory,
    VestigingsnummerPartijIdentificatorFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase


class PartijIdentificatorTests(APITestCase):

    def test_list(self):
        list_url = reverse("klantinteracties:partijidentificator-list")
        partij = PartijFactory.create()
        BsnPartijIdentificatorFactory.create(partij=partij)
        PartijIdentificator.objects.create(
            partij=partij,
            partij_identificator_code_objecttype="niet_natuurlijk_persoon",
            partij_identificator_code_soort_object_id="rsin",
            partij_identificator_object_id="296648875",
            partij_identificator_code_register="hr",
        )
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read(self):
        partij_identificator = PartijIdentificatorFactory.create()
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["url"], "http://testserver" + detail_url)

    def test_create(self):
        list_url = reverse("klantinteracties:partijidentificator-list")
        partij = PartijFactory.create()
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "anderePartijIdentificator")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )

    def test_update(self):
        partij, partij2 = PartijFactory.create_batch(2)
        partij_identificator = BsnPartijIdentificatorFactory.create(
            partij=partij,
            andere_partij_identificator="anderePartijIdentificator",
        )

        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "anderePartijIdentificator")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )

        data = {
            "identificeerdePartij": {"uuid": str(partij2.uuid)},
            "anderePartijIdentificator": "changed",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij2.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "changed")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )

    def test_update_partial(self):
        partij = PartijFactory.create()
        partij_identificator = BsnPartijIdentificatorFactory.create(
            partij=partij,
            andere_partij_identificator="anderePartijIdentificator",
        )

        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.get(detail_url)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "anderePartijIdentificator")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )

        data = {
            "anderePartijIdentificator": "changed",
        }

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "changed")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )

    def test_update_only_required(self):
        # partij_identificator is required
        partij = PartijFactory.create()
        partij_identificator = BsnPartijIdentificatorFactory.create(
            partij=partij,
            andere_partij_identificator="anderePartijIdentificator",
        )

        data = {
            "andere_partij_identificator": "test",
        }
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "partijIdentificator")
        self.assertEqual(error["code"], "required")
        self.assertEqual(error["reason"], "Dit veld is vereist.")

        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "changed",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "123456782",
                "codeRegister": "brp",
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "changed")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "123456782",
                "codeRegister": "brp",
            },
        )

    def test_destroy(self):
        partij_identificator = PartijIdentificatorFactory.create()
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("klantinteracties:partijidentificator-list")
        response = self.client.get(list_url)
        data = response.json()
        self.assertEqual(data["count"], 0)

    def test_invalid_choices_partij_identificator(self):
        url = reverse("klantinteracties:partijidentificator-list")
        partij = PartijFactory.create()
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "codeObjecttype": "test",
                "codeSoortObjectId": "test",
                "objectId": "",
                "codeRegister": "test",
            },
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "invalid")
        self.assertEqual(response.data["title"], "Invalid input.")
        self.assertEqual(len(response.data["invalid_params"]), 3)
        self.assertEqual(
            {item["name"] for item in response.data["invalid_params"]},
            {
                "partijIdentificator.codeObjecttype",
                "partijIdentificator.codeRegister",
                "partijIdentificator.codeSoortObjectId",
            },
        )

    def test_invalid_validation_partij_identificator_code_objecttype(self):
        url = reverse("klantinteracties:partijidentificator-list")
        partij = PartijFactory.create()
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "codeObjecttype": "niet_natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "partijIdentificatorCodeObjecttype")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "voor `codeRegister` brp zijn alleen deze waarden toegestaan: ['natuurlijk_persoon']",
        )

    def test_invalid_validation_partij_identificator_code_soort_object_id(self):
        url = reverse("klantinteracties:partijidentificator-list")
        partij = PartijFactory.create()
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "kvk_nummer",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "partijIdentificatorCodeSoortObjectId")
        self.assertEqual(error["code"], "invalid")

        self.assertEqual(
            error["reason"],
            "voor `codeObjecttype` natuurlijk_persoon zijn alleen deze waarden toegestaan: ['bsn', 'overig']",
        )

    def test_invalid_validation_partij_identificator_object_id(self):
        url = reverse("klantinteracties:partijidentificator-list")
        partij = PartijFactory.create()
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "12",
                "codeRegister": "brp",
            },
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "partijIdentificatorObjectId")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "Deze waarde is ongeldig, reden: Waarde moet 9 tekens lang zijn",
        )

    def test_invalid_create_empty_partij_identificator(self):
        # all partij_identificator fields required
        partij = PartijFactory.create()
        list_url = reverse("klantinteracties:partijidentificator-list")
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {},
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data["invalid_params"]), 4)
        get_validation_errors(response, "partijIdentificator.objectId")
        get_validation_errors(response, "partijIdentificator.codeSoortObjectId")
        get_validation_errors(response, "partijIdentificator.codeObjecttype")
        get_validation_errors(response, "partijIdentificator.codeRegister")

    def test_invalid_create_partial_partij_identificator(self):
        # all partij_identificator fields required
        partij = PartijFactory.create()
        list_url = reverse("klantinteracties:partijidentificator-list")
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "codeRegister": "brp",
            },
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "partijIdentificator.objectId")
        self.assertEqual(error["code"], "required")
        self.assertEqual(error["reason"], "Dit veld is vereist.")
        self.assertEqual(PartijIdentificator.objects.all().count(), 0)

    def test_invalid_update_partial_partij_identificator(self):
        # all partij_identificator values are required
        partij = PartijFactory.create()
        partij_identificator = BsnPartijIdentificatorFactory.create(partij=partij)
        data = {
            "identificeerdePartij": None,
            "partijIdentificator": {},
        }
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "partijIdentificator.objectId")
        self.assertEqual(error["code"], "required")
        self.assertEqual(error["reason"], "Dit veld is vereist.")
        self.assertEqual(PartijIdentificator.objects.all().count(), 1)

        data = {
            "identificeerdePartij": None,
            "partijIdentificator": {
                "codeObjecttype": "niet_natuurlijk_persoon",
                "codeSoortObjectId": "rsin",
                "codeRegister": "brp",
            },
        }
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "partijIdentificator.objectId")
        self.assertEqual(error["code"], "required")
        self.assertEqual(error["reason"], "Dit veld is vereist.")
        self.assertEqual(PartijIdentificator.objects.all().count(), 1)


class PartijIdentificatorUniquenessTests(APITestCase):
    list_url = reverse_lazy("klantinteracties:partijidentificator-list")

    def setUp(self):
        self.partij = PartijFactory.create()
        super().setUp()

    def test_valid_create(self):
        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "anderePartijIdentificator": "anderePartijIdentificator",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PartijIdentificator.objects.all().count(), 1)

    def test_valid_create_with_sub_identificator_van(self):
        partij_identificator = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )
        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "sub_identificator_van": {"uuid": str(partij_identificator.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)

    def test_invalid_create_duplicate_code_soort_object_id_for_partij(self):
        BsnPartijIdentificatorFactory.create(partij=self.partij)

        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "123456782",
                "codeRegister": "brp",
            },
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "__all__")
        self.assertEqual(error["code"], "unique_together")
        self.assertEqual(
            error["reason"],
            "Partij identificator met deze Partij en Soort object ID bestaat al.",
        )

    def test_valid_update_partij(self):
        partij_identificator = BsnPartijIdentificatorFactory.create(
            partij=PartijFactory.create()
        )
        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
        }
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        # check if this partij_identificator can be assigned to self.partij
        self.assertEqual(self.partij.partijidentificator_set.count(), 0)

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["identificeerdePartij"]["uuid"], str(self.partij.uuid))

    def test_invalid_update_partij(self):
        new_partij = PartijFactory.create()
        BsnPartijIdentificatorFactory.create(
            partij=new_partij,
            partij_identificator_object_id="123456782",
        )
        partij_identificator = BsnPartijIdentificatorFactory.create(partij=self.partij)
        data = {
            "identificeerdePartij": {"uuid": str(new_partij.uuid)},
        }
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        # check if this partij_identificator can be assigned to self.partij
        self.assertEqual(new_partij.partijidentificator_set.count(), 1)
        self.assertEqual(
            new_partij.partijidentificator_set.filter(
                partij_identificator_code_soort_object_id="bsn"
            ).count(),
            1,
        )

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "__all__")
        self.assertEqual(error["code"], "unique_together")
        self.assertEqual(
            error["reason"],
            "Partij identificator met deze Partij en Soort object ID bestaat al.",
        )
        self.assertEqual(new_partij.partijidentificator_set.count(), 1)
        self.assertEqual(
            new_partij.partijidentificator_set.filter(
                partij_identificator_code_soort_object_id="bsn"
            ).count(),
            1,
        )

    def test_valid_update_check_uniqueness_values(self):
        partij_identificator = BsnPartijIdentificatorFactory.create(partij=self.partij)
        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "anderePartijIdentificator": "changed",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "123456782",
                "codeRegister": "brp",
            },
        }
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["identificeerdePartij"]["uuid"], str(self.partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "changed")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "123456782",
                "codeRegister": "brp",
            },
        )

    def test_invalid_update_check_uniqueness_exists(self):
        partij_identificator_a = BsnPartijIdentificatorFactory.create(
            partij=self.partij,
            partij_identificator_object_id="123456782",
        )
        partij_identificator_b = BsnPartijIdentificatorFactory.create(
            partij=PartijFactory.create(),
        )
        # update partij_identificator_a with partij_identificator_b data
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator_a.uuid)},
        )

        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "anderePartijIdentificator": "changed",
            "partijIdentificator": {
                "codeObjecttype": partij_identificator_b.partij_identificator_code_objecttype,
                "codeSoortObjectId": partij_identificator_b.partij_identificator_code_soort_object_id,
                "objectId": partij_identificator_b.partij_identificator_object_id,
                "codeRegister": partij_identificator_b.partij_identificator_code_register,
            },
        }
        # partij_identificator already exists
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "__all__")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie.",
        )

    def test_valid_check_uniqueness_sub_identificator_van(self):
        BsnPartijIdentificatorFactory.create(partij=self.partij)
        # Same values, but sub_identifier_van is set
        partij = PartijFactory.create()
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=partij
        )
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)
        data = {
            "identificeerdePartij": {"uuid": str(partij.uuid)},
            "sub_identificator_van": {"uuid": str(sub_identificator_van.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PartijIdentificator.objects.all().count(), 3)

    def test_invalid_check_uniqueness_sub_identificator_van(self):
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )
        BsnPartijIdentificatorFactory.create(
            partij=self.partij, sub_identificator_van=sub_identificator_van
        )
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)
        # Same values and same sub_identificator_van
        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "sub_identificator_van": {"uuid": str(sub_identificator_van.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "__all__")
        self.assertEqual(error["code"], "unique_together")
        self.assertEqual(
            error["reason"],
            "Partij identificator met deze Partij en Soort object ID bestaat al.",
        )
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)

    def test_vestigingsnummer_valid_create(self):
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )

        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "sub_identificator_van": {"uuid": str(sub_identificator_van.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "vestiging",
                "codeSoortObjectId": "vestigingsnummer",
                "objectId": "296648875154",
                "codeRegister": "hr",
            },
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        partij_identificatoren = PartijIdentificator.objects.all()
        self.assertEqual(partij_identificatoren.count(), 2)

    def test_vestigingsnummer_invalid_create_without_sub_identificator_van(self):
        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "vestiging",
                "codeSoortObjectId": "vestigingsnummer",
                "objectId": "296648875154",
                "codeRegister": "hr",
            },
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "subIdentificatorVan")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "Voor een PartijIdentificator met codeSoortObjectId = `vestigingsnummer` "
                "is het verplicht om een `sub_identifier_van` met codeSoortObjectId = "
                "`kvk_nummer` te kiezen."
            ),
        )

    def test_vestigingsnummer_valid_create_external_partij(self):
        partij = PartijFactory.create()
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=partij
        )

        # sub_identificator_van partij is different from vestigingsnummer partij
        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "sub_identificator_van": {"uuid": str(sub_identificator_van.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "vestiging",
                "codeSoortObjectId": "vestigingsnummer",
                "objectId": "296648875154",
                "codeRegister": "hr",
            },
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)

    def test_vestigingsnummer_invalid_create_invalid_sub_identificator_van(self):
        sub_identificator_van = BsnPartijIdentificatorFactory.create(partij=self.partij)

        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "sub_identificator_van": {"uuid": str(sub_identificator_van.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "vestiging",
                "codeSoortObjectId": "vestigingsnummer",
                "objectId": "296648875154",
                "codeRegister": "hr",
            },
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "subIdentificatorVan")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            "Het is alleen mogelijk om een subIdentifierVan te selecteren met codeSoortObjectId = `kvk_nummer`.",
        )

    def test_vestigingsnummer_valid_update(self):
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )
        partij_identificator = VestigingsnummerPartijIdentificatorFactory.create(
            partij=self.partij,
            sub_identificator_van=sub_identificator_van,
        )

        self.assertEqual(PartijIdentificator.objects.count(), 2)

        data = {
            "anderePartijIdentificator": "changed",
        }
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["identificeerdePartij"]["uuid"], str(self.partij.uuid))
        self.assertEqual(data["anderePartijIdentificator"], "changed")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "vestiging",
                "codeSoortObjectId": "vestigingsnummer",
                "objectId": "296648875154",
                "codeRegister": "hr",
            },
        )

    def test_vestigingsnummer_invalid_update_set_sub_identificator_van_null(self):
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )
        partij_identificator = VestigingsnummerPartijIdentificatorFactory.create(
            partij=self.partij, sub_identificator_van=sub_identificator_van
        )

        self.assertEqual(PartijIdentificator.objects.count(), 2)

        data = {
            "sub_identificator_van": None,
        }
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "subIdentificatorVan")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "Voor een PartijIdentificator met codeSoortObjectId = `vestigingsnummer` is het verplicht om"
                " een `sub_identifier_van` met codeSoortObjectId = `kvk_nummer` te kiezen."
            ),
        )

    def test_invalid_vestigingsnummer_and_kvk_nummer_combination_unique(self):
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )
        VestigingsnummerPartijIdentificatorFactory.create(
            partij=self.partij,
            sub_identificator_van=sub_identificator_van,
        )
        # Same sub_identificator_van and same data_values
        data = {
            "identificeerdePartij": {"uuid": str(self.partij.uuid)},
            "sub_identificator_van": {"uuid": str(sub_identificator_van.uuid)},
            "partijIdentificator": {
                "codeObjecttype": "vestiging",
                "codeSoortObjectId": "vestigingsnummer",
                "objectId": "296648875154",
                "codeRegister": "hr",
            },
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data["invalid_params"]), 2)
        self.assertEqual(response.data["invalid_params"][0]["code"], "unique_together")
        self.assertEqual(
            response.data["invalid_params"][0]["reason"],
            "Partij identificator met deze Partij en Soort object ID bestaat al.",
        )
        self.assertEqual(response.data["invalid_params"][1]["code"], "invalid")
        self.assertEqual(
            response.data["invalid_params"][1]["reason"],
            "`PartijIdentificator` moet uniek zijn, er bestaat er al een met deze gegevenscombinatie.",
        )

    def test_valid_protect_delete(self):
        partij_identificator = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )
        self.assertEqual(PartijIdentificator.objects.all().count(), 1)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PartijIdentificator.objects.all().count(), 0)

    def test_invalid_protect_delete(self):
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )
        VestigingsnummerPartijIdentificatorFactory.create(
            partij=self.partij,
            sub_identificator_van=sub_identificator_van,
        )
        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(sub_identificator_van.uuid)},
        )
        self.assertEqual(PartijIdentificator.objects.all().count(), 2)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "Cannot delete some instances of model 'PartijIdentificator' because they are"
                " referenced through protected foreign keys: 'PartijIdentificator.sub_identificator_van'."
            ),
        )

        self.assertEqual(PartijIdentificator.objects.all().count(), 2)

    def test_create_partij_identificator_without_partij(self):
        with self.subTest("with identificeerdePartij not explicitly specified"):
            list_url = reverse("klantinteracties:partijidentificator-list")
            data = {
                "anderePartijIdentificator": "anderePartijIdentificator",
                "partijIdentificator": {
                    "codeObjecttype": "natuurlijk_persoon",
                    "codeSoortObjectId": "bsn",
                    "objectId": "296648875",
                    "codeRegister": "brp",
                },
            }

            response = self.client.post(list_url, data)
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, response.data
            )
            data = response.json()

            self.assertEqual(data["identificeerdePartij"], None)
            self.assertEqual(
                data["anderePartijIdentificator"], "anderePartijIdentificator"
            )
            self.assertEqual(
                data["partijIdentificator"],
                {
                    "codeObjecttype": "natuurlijk_persoon",
                    "codeSoortObjectId": "bsn",
                    "objectId": "296648875",
                    "codeRegister": "brp",
                },
            )

        with self.subTest("with identificeerdePartij explicitly set to null"):
            list_url = reverse("klantinteracties:partijidentificator-list")
            data = {
                "identificeerdePartij": None,
                "anderePartijIdentificator": "anderePartijIdentificator",
                "partijIdentificator": {
                    "codeObjecttype": "natuurlijk_persoon",
                    "codeSoortObjectId": "bsn",
                    "objectId": "111222333",
                    "codeRegister": "brp",
                },
            }

            response = self.client.post(list_url, data)
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, response.data
            )
            data = response.json()

            self.assertEqual(data["identificeerdePartij"], None)
            self.assertEqual(
                data["anderePartijIdentificator"], "anderePartijIdentificator"
            )
            self.assertEqual(
                data["partijIdentificator"],
                {
                    "codeObjecttype": "natuurlijk_persoon",
                    "codeSoortObjectId": "bsn",
                    "objectId": "111222333",
                    "codeRegister": "brp",
                },
            )

    def test_update_partij_identificator_with_partij_null(self):
        partij = PartijFactory.create()
        partij_identificator = BsnPartijIdentificatorFactory.create(partij=partij)

        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(partij_identificator.uuid)},
        )

        data = {
            "identificeerdePartij": None,
            "anderePartijIdentificator": "changed",
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["identificeerdePartij"], None)
        self.assertEqual(data["anderePartijIdentificator"], "changed")
        self.assertEqual(
            data["partijIdentificator"],
            {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        )

    def test_invalid_update_code_soort_object_id_parent(self):
        sub_identificator_van = KvkNummerPartijIdentificatorFactory.create(
            partij=self.partij
        )
        VestigingsnummerPartijIdentificatorFactory.create(
            partij=self.partij,
            sub_identificator_van=sub_identificator_van,
        )

        PartijIdentificator.objects.get(
            partij_identificator_code_soort_object_id="kvk_nummer"
        )
        PartijIdentificator.objects.get(
            partij_identificator_code_soort_object_id="vestigingsnummer"
        )

        detail_url = reverse(
            "klantinteracties:partijidentificator-detail",
            kwargs={"uuid": str(sub_identificator_van.uuid)},
        )
        # Update kvk_nummer with bsn
        data = {
            "partijIdentificator": {
                "codeObjecttype": "natuurlijk_persoon",
                "codeSoortObjectId": "bsn",
                "objectId": "296648875",
                "codeRegister": "brp",
            },
        }

        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "partijIdentificatorCodeSoortObjectId")
        self.assertEqual(error["code"], "invalid")
        self.assertEqual(
            error["reason"],
            (
                "Het is niet mogelijk om de codeSoortObjectId van deze PartijIdentificator te wijzigen, "
                "omdat er andere PartijIdentificatoren aan gekoppeld zijn."
            ),
        )
        PartijIdentificator.objects.get(
            partij_identificator_code_soort_object_id="kvk_nummer"
        )
        PartijIdentificator.objects.get(
            partij_identificator_code_soort_object_id="vestigingsnummer"
        )
