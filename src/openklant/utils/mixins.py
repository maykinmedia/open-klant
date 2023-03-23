from time import time

from django.core.cache import caches
from django.core.exceptions import PermissionDenied


class ThrottleMixin:
    """
    A very simple throttling implementation with, hopefully, sane defaults.

    You can specifiy the amount of visits (throttle_visits) a view can get,
    for a specific period (in seconds) throttle_period.
    """

    # n visits per period (in seconds)
    throttle_visits = 100
    throttle_period = 60**2  # in seconds
    throttle_403 = True
    throttle_name = "default"

    # get and options should always be fast. By default
    # do not throttle them.
    throttle_methods = ["post", "put", "patch", "delete", "head", "trace"]

    def get_throttle_cache(self):
        return caches["default"]

    def get_throttle_identifier(self):
        user = getattr(self, "user_cache", self.request.user)
        return str(user.id)

    def create_throttle_key(self):
        """
        :rtype string Use as key to save the last access
        """

        return "throttling_{id}_{throttle_name}_{window}".format(
            id=self.get_throttle_identifier(),
            throttle_name=self.throttle_name,
            window=self.get_throttle_window(),
        )

    def get_throttle_window(self):
        """
        round down to the throttle_period, which is then used to create the key.
        """
        current_time = int(time())
        return current_time - (current_time % self.throttle_period)

    def get_visits_in_window(self):
        cache = self.get_throttle_cache()
        key = self.create_throttle_key()

        initial_visits = 1
        stored = cache.add(key, initial_visits, self.throttle_period)
        if stored:
            visits = initial_visits
        else:
            try:
                visits = cache.incr(key)
            except ValueError:
                visits = initial_visits
        return visits

    def should_be_throttled(self):
        if self.throttle_methods == "all":
            return True
        return self.request.method.lower() in self.throttle_methods

    def dispatch(self, request, *args, **kwargs):
        if self.throttle_403:
            if (
                self.should_be_throttled()
                and self.get_visits_in_window() > self.throttle_visits
            ):
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class IPThrottleMixin(ThrottleMixin):
    """
    Same behavior as ThrottleMixin except it limits the amount of tries
    per IP-address a user can access a certain view.
    """

    def get_throttle_identifier(self):
        # REMOTE_ADDR is correctly set in XForwardedForMiddleware
        return str(self.request.META["REMOTE_ADDR"])
