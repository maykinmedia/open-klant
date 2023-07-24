from celery import Celery

from openklant.setup import setup_env

setup_env()

app = Celery("openklant")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
