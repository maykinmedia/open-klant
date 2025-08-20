from django.contrib.auth import views as auth_views

from maykin_common.throttling import IPThrottleMixin


class PasswordResetView(IPThrottleMixin, auth_views.PasswordResetView):
    throttle_name = "password-reset"
    throttle_visits = 5
    throttle_period = 60
    throttle_methods = ("get",)
