from django.utils.translation import gettext_lazy as _

from notifications_api_common.settings import *  # noqa
from open_api_framework.conf.base import *  # noqa
from open_api_framework.conf.utils import config  # noqa

from .api import *  # noqa

#
# APPLICATIONS enabled for this project
#
INSTALLED_APPS = INSTALLED_APPS + [
    # External applications.
    "vng_api_common.notifications",
    # Project applications.
    "openklant.accounts",
    "openklant.utils",
    "openklant.components.token",
    "openklant.components.klantinteracties",
    "openklant.components.contactgegevens",
    # Django libraries
    "localflavor",
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
    "zgw_consumers.contrib.setup_configuration.steps.ServiceConfigurationStep",
    "notifications_api_common.contrib.setup_configuration.steps.NotificationConfigurationStep",
    "openklant.setup_configuration.steps.TokenAuthConfigurationStep",
    "mozilla_django_oidc_db.setup_configuration.steps.AdminOIDCConfigurationStep",
)

#
# Celery
#

# Add (by default) 5 (soft), 15 (hard) minute timeouts to all Celery tasks.
CELERY_TASK_TIME_LIMIT = config(
    "CELERY_TASK_HARD_TIME_LIMIT",
    default=15 * 60,
    help_text=(
        "Defaults to: ``900`` seconds. "
        "If a celery task exceeds this time limit, the worker processing the task will "
        "be killed and replaced with a new one."
    ),
    group="Celery",
)  # hard
CELERY_TASK_SOFT_TIME_LIMIT = config(
    "CELERY_TASK_SOFT_TIME_LIMIT",
    default=5 * 60,
    help_text=(
        "Defaults to: ``300`` seconds. "
        "If a celery task exceeds this time limit, the ``SoftTimeLimitExceeded`` exception will be raised."
    ),
    group="Celery",
)  # soft

# Notifications
NOTIFICATIONS_DISABLED = config(
    "NOTIFICATIONS_DISABLED",
    default=True,
    help_text=(
        "Indicates whether or not notifications should be sent to the Notificaties API "
        "for operations on the API endpoints."
    ),
)

SITE_DOMAIN = config(
    "SITE_DOMAIN",
    default="example.com",
    help_text=("Defines the primary domain where the application is hosted."),
)

FORCE_TRANSLATION_STRINGS = [
    _("A page number within the paginated result set."),
    _("Number of results to return per page."),
]
