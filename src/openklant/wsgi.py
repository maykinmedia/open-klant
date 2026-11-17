"""
WSGI config for openklant project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

from collections.abc import Iterable
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

from openklant.setup import setup_env

try:
    import uwsgi  # pyright: ignore[reportMissingModuleSource] uwsgi magic...
except ImportError:
    uwsgi = None

if TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse, WSGIEnvironment

setup_env()


class LogVars:
    def __init__(self, application: WSGIHandler) -> None:
        self.application = application

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        if uwsgi is not None:
            now = datetime.now(tz=timezone.utc)
            uwsgi.set_logvar("iso8601timestamp", now.isoformat())
        return self.application(environ, start_response)


application = LogVars(get_wsgi_application())
