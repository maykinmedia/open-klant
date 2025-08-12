from djangorestframework_camel_case.settings import api_settings
from vng_api_common.conf.api import *  # noqa - imports white-listed

# Remove the reference - we don't have a single API version.
del API_VERSION  # noqa

KLANTINTERACTIES_API_VERSION = "0.3.0"
CONTACTGEGEVENS_API_VERSION = "1.1.1"

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK["PAGE_SIZE"] = 100
REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"] = (
    "vng_api_common.pagination.DynamicPageSizePagination"
)
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "openklant.components.utils.schema.AutoSchema"

SPECTACULAR_SETTINGS = {
    "REDOC_DIST": "SIDECAR",
    "SERVE_INCLUDE_SCHEMA": False,
    "CAMELIZE_NAMES": True,
    "SCHEMA_PATH_PREFIX": r"/v[0-9]+",
    "SCHEMA_PATH_PREFIX_TRIM": True,
    "ENUM_GENERATE_CHOICE_DESCRIPTION": False,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
        "maykin_common.drf_spectacular.hooks.remove_invalid_url_defaults",
    ],
    "CONTACT": {
        "email": "standaarden.ondersteuning@vng.nl",
        "url": "https://zaakgerichtwerken.vng.cloud",
    },
    "LICENSE": {
        "name": "EUPL 1.2",
        "url": "https://opensource.org/licenses/EUPL-1.2",
    },
}

VNG_COMPONENTS_BRANCH = "master"

GEMMA_URL_INFORMATIEMODEL_VERSIE = "1.0"

# SELF_REPO = "VNG-Realisatie/klanten-api"
# SELF_BRANCH = os.getenv("SELF_BRANCH") or KLANTEN_API_VERSION
# GITHUB_API_SPEC = f"https://raw.githubusercontent.com/{SELF_REPO}/{SELF_BRANCH}/src/openapi.yaml"  # noqa

zrc_repo = "vng-realisatie/zaken-api"
zrc_commit = "7b0a036e5f0e89afef6cb6df986549b1199d904e"
ZRC_API_SPEC = (
    f"https://raw.githubusercontent.com/{zrc_repo}/{zrc_commit}/src/openapi.yaml"  # noqa
)

api_settings.JSON_UNDERSCOREIZE["ignore_keys"] = ("_expand",)
