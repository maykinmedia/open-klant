import os
import warnings

os.environ.setdefault("DEBUG", "no")
os.environ.setdefault("ENVIRONMENT", "jenkins")
os.environ.setdefault("SECRET_KEY", "for-testing-purposes-only")
os.environ.setdefault("IS_HTTPS", "no")
os.environ.setdefault("ALLOWED_HOSTS", "")

os.environ.setdefault("DB_USER", "jenkins")
os.environ.setdefault("DB_PASSWORD", "jenkins")
# PostgreSQL 9.6: 5432 (default for Jenkins)
os.environ.setdefault("DB_PORT", "5432")

from .base import *  # noqa isort:skip


def get_db_name(prefix):
    """
    get a reasonable name below Postgres' 63 char name limit
    """
    job = os.getenv("JOB_NAME", default="").lower().rsplit("/", 1)[-1]
    build = os.getenv("BUILD_NUMBER", default="0")
    lim = 63 - 2 - len(prefix) - len(build)
    return "{}_{}_{}".format(prefix, job[:lim], build)


DATABASES["default"]["TEST"] = {"NAME": get_db_name("test_openklant")}

LOGGING["loggers"].update(
    {
        "django": {
            "handlers": ["django"],
            "level": "WARNING",
            "propagate": True,
        },
    }
)

#
# Django-axes
#
AXES_BEHIND_REVERSE_PROXY = (
    False  # Required to allow FakeRequest and the like to work correctly.
)

# in memory cache and django-axes don't get along.
# https://django-axes.readthedocs.io/en/latest/configuration.html#known-configuration-problems
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
    "axes": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "oidc": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

ELASTIC_APM["DEBUG"] = True

#
# Jenkins settings
#
INSTALLED_APPS += [
    "django_jenkins",
]
PROJECT_APPS = [app for app in INSTALLED_APPS if app.startswith("openklant.")]
JENKINS_TASKS = (
    # 'django_jenkins.tasks.run_pylint',  # Pylint < 2.0 does not run on Python 3.7+
    "django_jenkins.tasks.run_pep8",
)

# THOU SHALT NOT USE NAIVE DATETIMES
warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)

NOTIFICATIONS_DISABLED = True
