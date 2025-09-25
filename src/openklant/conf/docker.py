import os

from maykin_common.config_helpers import config

os.environ.setdefault("DB_USER", config("DATABASE_USER", "postgres"))
os.environ.setdefault("DB_NAME", config("DATABASE_NAME", "postgres"))
os.environ.setdefault("DB_PASSWORD", config("DATABASE_PASSWORD", ""))
os.environ.setdefault("DB_HOST", config("DATABASE_HOST", "db"))
os.environ.setdefault("DB_CONN_MAX_AGE", "60")

os.environ.setdefault("ENVIRONMENT", "docker")
os.environ.setdefault("LOG_STDOUT", "yes")
os.environ.setdefault("LOG_FORMAT_CONSOLE", "json")

# # Strongly suggested to not use this, but explicitly list the allowed hosts. It is
# used to verify if a redirect is safe or not (open redirect vulnerabilities etc.)
# os.environ.setdefault("ALLOWED_HOSTS", "*")

from .production import *  # noqa isort:skip
