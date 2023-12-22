"""
Bootstrap the environment.

Load the secrets from the .env file and store them in the environment, so
they are available for Django settings initialization.

.. warning::

    do NOT import anything Django related here, as this file needs to be loaded
    before Django is initialized.
"""
import os
import re

from dotenv import load_dotenv


def setup_env():
    # load the environment variables containing the secrets/config
    dotenv_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, ".env")
    load_dotenv(dotenv_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openklant.conf.dev")

    monkeypatch_drf_camel_case()


def monkeypatch_drf_camel_case() -> None:
    """
    Revert the camelize_re back to the old behaviour.

    drf-camel-case had a camelize_re that excluded numbers, which was used while the
    standard was created. When upgrading drf-camel-case, we had to revert this regex
    back to the old one to stay compliant with the schema from the standard.

    TODO: bring up this more correct camelizing issue for a 2.x version of the standard
    where breaking changes are allowed.

    One of the relevant commits:
    https://github.com/vbabiy/djangorestframework-camel-case/commit/f814bf32461d274e99bf4f24dcd6bac06056c8b2#
    """
    from djangorestframework_camel_case import util

    util.camelize_re = re.compile(r"[a-z]_[a-z]")

    def old_underscore_to_camel(match):
        return match.group()[0] + match.group()[2].upper()

    util.underscore_to_camel = old_underscore_to_camel
