import os

from notifications_api_common.settings import *  # noqa

os.environ["_USE_STRUCTLOG"] = "True"

from open_api_framework.conf.base import *  # noqa
from open_api_framework.conf.utils import config  # noqa
from upgrade_check import UpgradeCheck, VersionRange
from upgrade_check.constraints import UpgradePaths
from maykin_common.health_checks import default_health_check_apps
from .api import *  # noqa

#
# APPLICATIONS enabled for this project
#
INSTALLED_APPS = INSTALLED_APPS + [
    "capture_tag",
    "maykin_common",
    # External applications.
    "vng_api_common.notifications",
    # health check + plugins
    *default_health_check_apps,
    "maykin_common.health_checks.celery",
    # Project applications.
    "openklant.accounts",
    "openklant.utils",
    "openklant.components.token",
    "openklant.components.klantinteracties",
    "openklant.components.contactgegevens",
    "openklant.config",
    # Django libraries
    "localflavor",
]

MIDDLEWARE += ["openklant.utils.middleware.APIVersionHeaderMiddleware"]

ENABLE_CLOUD_EVENTS = config(
    "ENABLE_CLOUD_EVENTS",
    default=False,
    cast=bool,
    help_text="**EXPERIMENTAL**: indicates whether or not cloud events should be sent to the configured endpoint for specific operations via the API (not ready for use in production)",
)

NOTIFICATIONS_SOURCE = config(
    "NOTIFICATIONS_SOURCE",
    default="",
    help_text="**EXPERIMENTAL**: the identifier of this application to use as the source in notifications and cloudevents",
)

#
# SECURITY settings
#
CSRF_FAILURE_VIEW = "maykin_common.views.csrf_failure"

# This setting is used by the csrf_failure view (accounts app).
# You can specify any path that should match the request.path
# Note: the LOGIN_URL Django setting is not used because you could have
# multiple login urls defined.
LOGIN_URLS = [reverse_lazy("admin:login")]

#
# Custom settings
#
PROJECT_NAME = "Open Klant"
SITE_TITLE = "API dashboard"

# Default (connection timeout, read timeout) for the requests library (in seconds)
REQUESTS_DEFAULT_TIMEOUT = (10, 30)

##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

#
# Django-Admin-Index
#
ADMIN_INDEX_SHOW_REMAINING_APPS_TO_SUPERUSERS = True
ADMIN_INDEX_DISPLAY_DROP_DOWN_MENU_CONDITION_FUNCTION = (
    "maykin_common.django_two_factor_auth.should_display_dropdown_menu"
)
#
# Django setup configuration
#
SETUP_CONFIGURATION_STEPS = (
    "zgw_consumers.contrib.setup_configuration.steps.ServiceConfigurationStep",
    "notifications_api_common.contrib.setup_configuration.steps.NotificationConfigurationStep",
    "openklant.setup_configuration.steps.TokenAuthConfigurationStep",
    "mozilla_django_oidc_db.setup_configuration.steps.AdminOIDCConfigurationStep",
    "openklant.setup_configuration.steps.ReferentielijstenConfigurationStep",
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

#
# CELERY-ONCE
#
CELERY_ONCE_REDIS_URL = config(
    "CELERY_ONCE_REDIS_URL",
    default=CELERY_BROKER_URL,
    group="Celery",
)
CELERY_ONCE = {
    "backend": "celery_once.backends.Redis",
    "settings": {
        "url": CELERY_ONCE_REDIS_URL,
        "default_timeout": 60 * 60,  # one hour
    },
}

#
# Notifications
#
# Override the default to be `True`, to make notifications opt-in
NOTIFICATIONS_DISABLED = config(
    "NOTIFICATIONS_DISABLED",
    default=True,
    help_text=(
        "Indicates whether or not notifications should be sent to the Notificaties API "
        "for operations on the API endpoints."
    ),
)

#
# django-upgrade-check
#

UPGRADE_CHECK_PATHS: UpgradePaths = {
    "2.6.0": UpgradeCheck(VersionRange(minimum="2.5.0")),
}

UPGRADE_CHECK_STRICT = False

#
# MAYKIN-COMMON health checks
#
MKN_HEALTH_CHECKS_WORKER_EVENT_LOOP_LIVENESS_FILE = (
    BASE_DIR / "tmp" / "celery_worker_event_loop.live"
)
MKN_HEALTH_CHECKS_WORKER_READINESS_FILE = BASE_DIR / "tmp" / "celery_worker.ready"
