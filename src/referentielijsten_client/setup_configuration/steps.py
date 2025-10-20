import structlog
from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import ConfigurationRunFailed
from zgw_consumers.models import Service

from openklant.config.models import ReferentielijstenConfig
from referentielijsten_client.setup_configuration.models import (
    ReferentielijstenConfigurationModel,
)

logger = structlog.stdlib.get_logger(__name__)


def get_service(slug: str) -> Service:
    try:
        return Service.objects.get(slug=slug)
    except Service.DoesNotExist as e:
        raise Service.DoesNotExist(f"{str(e)} (identifier = {slug})")


class ReferentielijstenConfigurationStep(
    BaseConfigurationStep[ReferentielijstenConfigurationModel]
):
    namespace = "referentielijsten_config"
    enable_setting = "referentielijsten_config_enable"

    verbose_name = "Configuration for Referentielijsten service"
    config_model = ReferentielijstenConfigurationModel

    def execute(self, model: ReferentielijstenConfigurationModel) -> None:
        logger.info(
            "configuring_referentielijsten",
            enabled=model.enabled,
            service_identifier=model.referentielijsten_api_service_identifier,
        )
        if not model.enabled:
            config_instance = ReferentielijstenConfig.get_solo()
            config_instance.enabled = False
            config_instance.service = None
            config_instance.kanalen_tabel_code = None
            config_instance.save()
            logger.info("referentielijsten_config_disabled", success=True)
            return

        service = None
        if identifier := model.referentielijsten_api_service_identifier:
            try:
                service = get_service(identifier)
            except Service.DoesNotExist as exc:
                raise ConfigurationRunFailed(
                    f"Could not find Service with identifier '{identifier}'. "
                    "Ensure the ServiceConfigurationStep has been run successfully."
                ) from exc

        config_instance = ReferentielijstenConfig.get_solo()
        config_instance.enabled = model.enabled
        config_instance.service = service

        config_instance.kanalen_tabel_code = model.kanalen_tabel_code

        config_instance.save()

        logger.info("referentielijsten_config_updated", success=True)
