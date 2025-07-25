"""
Bootstrap the environment.

Load the secrets from the .env file and store them in the environment, so
they are available for Django settings initialization.

.. warning::

    do NOT import anything Django related here, as this file needs to be loaded
    before Django is initialized.
"""

import os

import structlog
from dotenv import load_dotenv


def setup_env():
    # load the environment variables containing the secrets/config
    dotenv_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, ".env")
    load_dotenv(dotenv_path)

    structlog.contextvars.bind_contextvars(source="app")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openklant.conf.dev")
