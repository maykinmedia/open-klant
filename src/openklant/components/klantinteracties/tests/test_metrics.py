from unittest.mock import MagicMock, patch

from vng_api_common.tests import reverse

from openklant.components.klantinteracties.models.tests.factories import (
    ActorFactory,
    BetrokkeneFactory,
    DigitaalAdresFactory,
    InterneTaakFactory,
    KlantcontactFactory,
    PartijFactory,
)
from openklant.components.token.tests.api_testcase import APITestCase

from ..metrics import (
    actoren_create_counter,
    actoren_delete_counter,
    actoren_update_counter,
    betrokkenen_create_counter,
    betrokkenen_delete_counter,
    betrokkenen_update_counter,
    digitale_adressen_create_counter,
    digitale_adressen_delete_counter,
    digitale_adressen_update_counter,
    interne_taken_create_counter,
    interne_taken_delete_counter,
    interne_taken_update_counter,
    klantcontacten_create_counter,
    klantcontacten_delete_counter,
    klantcontacten_update_counter,
    partijen_create_counter,
    partijen_delete_counter,
    partijen_update_counter,
)


class KlantcontactTests(APITestCase):
    @patch.object(
        klantcontacten_create_counter, "add", wraps=klantcontacten_create_counter.add
    )
    def test_klantcontacten_create_counter(self, mock_add: MagicMock):
        self.client.post(
            reverse("klantinteracties:klantcontact-list"),
            {
                "nummer": "1234567890",
                "kanaal": "kanaal",
                "onderwerp": "onderwerp",
                "taal": "ndl",
                "vertrouwelijk": True,
            },
        )
        mock_add.assert_called_once_with(1)

    @patch.object(
        klantcontacten_update_counter, "add", wraps=klantcontacten_update_counter.add
    )
    def test_klantcontacten_update_counter(self, mock_add: MagicMock):
        klantcontact = KlantcontactFactory.create()
        self.client.patch(
            reverse(
                "klantinteracties:klantcontact-detail",
                kwargs={"uuid": str(klantcontact.uuid)},
            ),
            {},
        )
        mock_add.assert_called_once_with(1)

    @patch.object(
        klantcontacten_delete_counter, "add", wraps=klantcontacten_delete_counter.add
    )
    def test_klantcontacten_delete_counter(self, mock_add: MagicMock):
        klantcontact = KlantcontactFactory.create()
        self.client.delete(
            reverse(
                "klantinteracties:klantcontact-detail",
                kwargs={"uuid": str(klantcontact.uuid)},
            ),
            {},
        )
        mock_add.assert_called_once_with(1)


class BetrokkeneTests(APITestCase):
    @patch.object(
        betrokkenen_create_counter, "add", wraps=betrokkenen_create_counter.add
    )
    def test_betrokkenen_create_counter(self, mock_add: MagicMock):
        klantcontact = KlantcontactFactory.create()
        self.client.post(
            reverse("klantinteracties:betrokkene-list"),
            {
                "hadKlantcontact": {"uuid": str(klantcontact.uuid)},
                "rol": "vertegenwoordiger",
                "initiator": True,
            },
        )
        mock_add.assert_called_once_with(1)

    @patch.object(
        betrokkenen_update_counter, "add", wraps=betrokkenen_update_counter.add
    )
    def test_betrokkenen_update_counter(self, mock_add: MagicMock):
        betrokkene = BetrokkeneFactory.create()
        self.client.patch(
            reverse(
                "klantinteracties:betrokkene-detail",
                kwargs={"uuid": str(betrokkene.uuid)},
            ),
            {},
        )
        mock_add.assert_called_once_with(1)

    @patch.object(
        betrokkenen_delete_counter, "add", wraps=betrokkenen_delete_counter.add
    )
    def test_betrokkenen_delete_counter(self, mock_add: MagicMock):
        betrokkene = BetrokkeneFactory.create()
        self.client.delete(
            reverse(
                "klantinteracties:betrokkene-detail",
                kwargs={"uuid": str(betrokkene.uuid)},
            ),
            {},
        )
        mock_add.assert_called_once_with(1)


class PartijTests(APITestCase):
    @patch.object(partijen_create_counter, "add", wraps=partijen_create_counter.add)
    def test_partijen_create_counter(self, mock_add: MagicMock):
        self.client.post(
            reverse("klantinteracties:partij-list"),
            {
                "soortPartij": "organisatie",
                "indicatieActief": True,
            },
        )
        mock_add.assert_called_once_with(1)

    @patch.object(partijen_update_counter, "add", wraps=partijen_update_counter.add)
    def test_partijen_update_counter(self, mock_add: MagicMock):
        partij = PartijFactory.create()
        self.client.patch(
            reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
            ),
            {},
        )
        mock_add.assert_called_once_with(1)

    @patch.object(partijen_delete_counter, "add", wraps=partijen_delete_counter.add)
    def test_partijen_delete_counter(self, mock_add: MagicMock):
        partij = PartijFactory.create()
        self.client.delete(
            reverse(
                "klantinteracties:partij-detail", kwargs={"uuid": str(partij.uuid)}
            ),
            {},
        )
        mock_add.assert_called_once_with(1)


class ActorTests(APITestCase):
    @patch.object(actoren_create_counter, "add", wraps=actoren_create_counter.add)
    def test_actoren_create_counter(self, mock_add: MagicMock):
        self.client.post(
            reverse("klantinteracties:actor-list"),
            {
                "naam": "Phil",
                "soortActor": "medewerker",
            },
        )
        mock_add.assert_called_once_with(1)

    @patch.object(actoren_update_counter, "add", wraps=actoren_update_counter.add)
    def test_actoren_update_counter(self, mock_add: MagicMock):
        actor = ActorFactory.create()
        self.client.patch(
            reverse("klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}),
            {},
        )
        mock_add.assert_called_once_with(1)

    @patch.object(actoren_delete_counter, "add", wraps=actoren_delete_counter.add)
    def test_actoren_delete_counter(self, mock_add: MagicMock):
        actor = ActorFactory.create()
        self.client.delete(
            reverse("klantinteracties:actor-detail", kwargs={"uuid": str(actor.uuid)}),
            {},
        )
        mock_add.assert_called_once_with(1)


class DigitaalAdresTests(APITestCase):
    @patch.object(
        digitale_adressen_create_counter,
        "add",
        wraps=digitale_adressen_create_counter.add,
    )
    def test_digitale_adressen_create_counter(self, mock_add: MagicMock):
        partij = PartijFactory.create()
        self.client.post(
            reverse("klantinteracties:digitaaladres-list"),
            {
                "soortDigitaalAdres": "email",
                "adres": "foobar@example.com",
                "verstrektDoorPartij": {"uuid": str(partij.uuid)},
            },
        )
        mock_add.assert_called_once_with(1)

    @patch.object(
        digitale_adressen_update_counter,
        "add",
        wraps=digitale_adressen_update_counter.add,
    )
    def test_digitale_adressen_update_counter(self, mock_add: MagicMock):
        digitaal_adres = DigitaalAdresFactory.create()
        self.client.patch(
            reverse(
                "klantinteracties:digitaaladres-detail",
                kwargs={"uuid": str(digitaal_adres.uuid)},
            ),
            {},
        )

        mock_add.assert_called_once_with(1)

    @patch.object(
        digitale_adressen_delete_counter,
        "add",
        wraps=digitale_adressen_delete_counter.add,
    )
    def test_digitale_adressen_delete_counter(self, mock_add: MagicMock):
        digitaal_adres = DigitaalAdresFactory.create()
        self.client.delete(
            reverse(
                "klantinteracties:digitaaladres-detail",
                kwargs={"uuid": str(digitaal_adres.uuid)},
            ),
            {},
        )

        mock_add.assert_called_once_with(1)


class InterneTaakTests(APITestCase):
    @patch.object(
        interne_taken_create_counter, "add", wraps=interne_taken_create_counter.add
    )
    def test_interne_taken_create_counter(self, mock_add: MagicMock):
        actor = ActorFactory.create()
        klantcontact = KlantcontactFactory.create()
        self.client.post(
            reverse("klantinteracties:internetaak-list"),
            {
                "toegewezenAanActor": {"uuid": str(actor.uuid)},
                "aanleidinggevendKlantcontact": {"uuid": str(klantcontact.uuid)},
                "nummer": "1312312312",
                "gevraagdeHandeling": "gevraagdeHandeling",
                "toelichting": "toelichting",
                "status": "verwerkt",
            },
        )
        mock_add.assert_called_once_with(1)

    @patch.object(
        interne_taken_update_counter, "add", wraps=interne_taken_update_counter.add
    )
    def test_interne_taken_update_counter(self, mock_add: MagicMock):
        internetaak = InterneTaakFactory.create()
        self.client.patch(
            reverse(
                "klantinteracties:internetaak-detail",
                kwargs={"uuid": str(internetaak.uuid)},
            ),
            {},
        )
        mock_add.assert_called_once_with(1)

    @patch.object(
        interne_taken_delete_counter, "add", wraps=interne_taken_delete_counter.add
    )
    def test_interne_taken_delete_counter(self, mock_add: MagicMock):
        internetaak = InterneTaakFactory.create()
        self.client.delete(
            reverse(
                "klantinteracties:internetaak-detail",
                kwargs={"uuid": str(internetaak.uuid)},
            ),
            {},
        )
        mock_add.assert_called_once_with(1)
