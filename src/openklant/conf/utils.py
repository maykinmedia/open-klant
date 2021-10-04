import logging
import os
from shutil import which
from subprocess import CalledProcessError, check_output

from django.conf import settings

from decouple import Csv, config as _config, undefined
from sentry_sdk.integrations import DidNotEnable, django, redis

logger = logging.getLogger(__name__)


def config(option: str, default=undefined, *args, **kwargs):
    """
    Pull a config parameter from the environment.

    Read the config variable ``option``. If it's optional, use the ``default`` value.
    Input is automatically cast to the correct type, where the type is derived from the
    default value if possible.

    Pass ``split=True`` to split the comma-separated input into a list.
    """
    if "split" in kwargs:
        kwargs.pop("split")
        kwargs["cast"] = Csv()

    if default is not undefined and default is not None:
        kwargs.setdefault("cast", type(default))
    return _config(option, default=default, *args, **kwargs)


def get_sentry_integrations() -> list:
    """
    Determine which Sentry SDK integrations to enable.
    """
    default = [
        django.DjangoIntegration(),
        redis.RedisIntegration(),
    ]
    extra = []

    try:
        from sentry_sdk.integrations import celery
    except DidNotEnable:  # happens if the celery import fails by the integration
        pass
    else:
        extra.append(celery.CeleryIntegration())

    return [*default, *extra]


def _get_version_from_file():
    """
    Returns a commit hash from the project's .git/ dir if it exists
    """
    heads_dir = os.path.join(settings.BASE_DIR, ".git", "refs", "heads")

    try:
        heads = os.listdir(heads_dir)
    except FileNotFoundError:
        logging.warning("Unable to read commit hash from git files")
        return ""

    for filename in ("master", "main", "develop"):
        if filename in heads:
            try:
                with open(os.path.join(heads_dir, filename)) as file:
                    return file.read().strip()
            except OSError:
                logging.warning("Unable to read commit hash from file")

    return ""


def _get_version_from_git():
    """
    Returns the current tag or commit hash supplied by git
    """
    try:
        tags = check_output(
            ["git", "tag", "--points-at", "HEAD"], universal_newlines=True
        )
    except CalledProcessError:
        logger.warning("Unable to list tags")
        tags = None

    if tags:
        return next(version for version in tags.splitlines())

    try:
        commit = check_output(["git", "rev-parse", "HEAD"], universal_newlines=True)
    except CalledProcessError:
        logger.warning("Unable to list current commit hash")
        commit = None

    return commit or ""


def get_current_version():
    version = config("VERSION_TAG", default=None)

    if version:
        return version
    elif which("git"):
        return _get_version_from_git()

    return _get_version_from_file()
