"""
WSGI config for openklant project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application

from openklant.setup import setup_env

setup_env()

application = get_wsgi_application()
