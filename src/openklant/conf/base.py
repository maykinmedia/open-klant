from open_api_framework.conf.base import *  # noqa

from .api import *  # noqa

init_sentry()

#
# APPLICATIONS enabled for this project
#
# FIXME implement 2fa
INSTALLED_APPS.pop(INSTALLED_APPS.index("maykin_2fa"))
INSTALLED_APPS = INSTALLED_APPS + [
    # Project applications.
    "openklant.accounts",
    "openklant.utils",
    "openklant.components.token",
    "openklant.components.klantinteracties",
    "openklant.components.contactgegevens",
]

# FIXME should these be part of OAf?
MIDDLEWARE.insert(
    MIDDLEWARE.index("django.contrib.auth.middleware.AuthenticationMiddleware") + 1,
    "vng_api_common.middleware.AuthMiddleware",
)
MIDDLEWARE = MIDDLEWARE + ["openklant.utils.middleware.APIVersionHeaderMiddleware"]

#
# SECURITY settings
#
CSRF_FAILURE_VIEW = "openklant.accounts.views.csrf_failure"

#
# Custom settings
#
PROJECT_NAME = "Open Klant"
SITE_TITLE = "API dashboard"

##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

#
# Django-Admin-Index
#
ADMIN_INDEX_SHOW_REMAINING_APPS_TO_SUPERUSERS = True
