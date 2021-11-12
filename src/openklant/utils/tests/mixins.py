from vng_api_common.tests import JWTAuthMixin


class JWTAuthTransactionMixin(JWTAuthMixin):
    def setUp(self):
        # FIXME setUpTestData() doesn't work with APITransactionTestCase
        applicatie, autorisatie = self._create_credentials(
            self.client_id,
            self.secret,
            heeft_alle_autorisaties=self.heeft_alle_autorisaties,
            scopes=self.scopes,
            zaaktype=self.zaaktype,
            informatieobjecttype=self.informatieobjecttype,
            besluittype=self.besluittype,
            max_vertrouwelijkheidaanduiding=self.max_vertrouwelijkheidaanduiding,
        )
        self.applicatie = applicatie
        self.autorisatie = autorisatie

        super().setUp()
