from open_api_framework.conf.base import *  # noqa

from .api import *  # noqa

init_sentry()

#
# APPLICATIONS enabled for this project
#
INSTALLED_APPS = INSTALLED_APPS + [
    # Project applications.
    "openklant.accounts",
    "openklant.utils",
    "openklant.components.token",
    "openklant.components.klantinteracties",
    "openklant.components.contactgegevens",
]
# `django.contrib.sites` is installed by Open API Framework by default
# but we don't want to rely on it anymore (e.g. when generating the label for 2FA)
INSTALLED_APPS.remove("django.contrib.sites")

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

#
# Django setup configuration
#
SETUP_CONFIGURATION_STEPS = (
    "openklant.setup_configuration.steps.TokenAuthConfigurationStep",
    "mozilla_django_oidc_db.setup_configuration.steps.AdminOIDCConfigurationStep",
)
