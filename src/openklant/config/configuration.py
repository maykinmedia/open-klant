from django.core.exceptions import ImproperlyConfigured

from maykin.setup_configuration import setup_configuration

from openklant.config.models import ReferentielijstenConfig


@setup_configuration()
def referentielijsten_config():
    config = ReferentielijstenConfig.get_solo()

    if config.enabled and not config.service:
        raise ImproperlyConfigured(
            "ReferentielijstenConfig is enabled, but no service is configured."
        )

    return config
