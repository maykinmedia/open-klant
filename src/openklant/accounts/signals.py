from io import StringIO
from typing import Literal

from django.apps import apps
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.contrib.contenttypes.management import create_contenttypes
from django.core.management import call_command
from django.dispatch import receiver
from django.http import HttpRequest

from axes.signals import user_locked_out
from django_admin_index.models import AppGroup

from .metrics import login_failures, logins, logouts, user_lockouts
from .models import User


def update_admin_index(sender, **kwargs):
    AppGroup.objects.all().delete()

    project_name = __name__.split(".")[0]

    for app_config in apps.get_app_configs():
        if app_config.name.startswith(project_name):
            create_contenttypes(app_config, verbosity=0)

    call_command("loaddata", "default_admin_index", verbosity=0, stdout=StringIO())


@receiver(user_logged_in, dispatch_uid="user_logged_in.increment_counter")
def increment_logins_counter(
    sender: type[User], request: HttpRequest | None, user: User, **kwargs
) -> None:
    logins.add(
        1,
        attributes={
            "username": user.username,
            "http_target": request.path if request else "",
        },
    )


@receiver(user_logged_out, dispatch_uid="user_logged_out.increment_counter")
def increment_logouts_counter(
    sender: type[User], request: HttpRequest | None, user: User | None, **kwargs
) -> None:
    if user is None:
        return
    logouts.add(1, attributes={"username": user.username})


@receiver(user_login_failed, dispatch_uid="user_login_failed.increment_counter")
def increment_login_failure_counter(
    sender, request: HttpRequest | None = None, **kwargs
):
    login_failures.add(
        1,
        attributes={"http_target": request.path if request else ""},
    )


@receiver(user_locked_out, dispatch_uid="user_locked_out.increment_counter")
def increment_user_locked_out_counter(
    sender: Literal["axes"],
    request: HttpRequest,
    username: str,
    ip_address: str,
    **kwargs,
) -> None:
    user_lockouts.add(
        1,
        attributes={
            "http_target": request.path,
            "username": username,
        },
    )
