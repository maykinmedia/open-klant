from vng_api_common.conf.api import *  # noqa - imports white-listed

# Remove the reference - we don't have a single API version.
del API_VERSION  # noqa

KLANTEN_API_VERSION = "1.0.0"
CONTACTMOMENTEN_API_VERSION = "1.0.0"

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK["PAGE_SIZE"] = 100
REST_FRAMEWORK[
    "DEFAULT_PAGINATION_CLASS"
] = "rest_framework.pagination.PageNumberPagination"

SECURITY_DEFINITION_NAME = "JWT-Claims"

SWAGGER_SETTINGS = BASE_SWAGGER_SETTINGS.copy()

SWAGGER_SETTINGS.update(
    {
        "DEFAULT_INFO": "openklant.components.klanten.api.schema.info",
        "SECURITY_DEFINITIONS": {
            SECURITY_DEFINITION_NAME: {
                # OAS 3.0
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                # not official...
                # 'scopes': {},  # TODO: set up registry that's filled in later...
                # Swagger 2.0
                # 'name': 'Authorization',
                # 'in': 'header'
                # 'type': 'apiKey',
            }
        },
        "DEFAULT_FIELD_INSPECTORS": (
            "vng_api_common.inspectors.fields.HyperlinkedIdentityFieldInspector",
            "vng_api_common.inspectors.fields.HyperlinkedRelatedFieldInspector",
        )
        + BASE_SWAGGER_SETTINGS["DEFAULT_FIELD_INSPECTORS"],
    }
)

GEMMA_URL_INFORMATIEMODEL_VERSIE = "1.0"

# SELF_REPO = "VNG-Realisatie/klanten-api"
# SELF_BRANCH = os.getenv("SELF_BRANCH") or KLANTEN_API_VERSION
# GITHUB_API_SPEC = f"https://raw.githubusercontent.com/{SELF_REPO}/{SELF_BRANCH}/src/openapi.yaml"  # noqa

zrc_repo = "vng-realisatie/zaken-api"
zrc_commit = "7b0a036e5f0e89afef6cb6df986549b1199d904e"
ZRC_API_SPEC = f"https://raw.githubusercontent.com/{zrc_repo}/{zrc_commit}/src/openapi.yaml"  # noqa
