import logging

from django.db import DatabaseError

from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import ConfigurationRunFailed
from pydantic import ValidationError

from openklant.components.token.models import TokenAuth
from openklant.setup_configuration.models import (
    TokenAuthConfigurationModel,
    TokenAuthGroupConfigurationModel,
)

logger = logging.getLogger(__name__)


class TokenAuthConfigurationStep(
    BaseConfigurationStep[TokenAuthGroupConfigurationModel]
):
    """
    Configure configuration groups for the Objects API backend
    """

    namespace = "tokens_config"
    enable_setting = "tokens_config_enable"

    verbose_name = "Configuration to set up authentication tokens for Open Klant"
    config_model = TokenAuthGroupConfigurationModel

    def execute(self, model: TokenAuthGroupConfigurationModel) -> None:
        for model in model.group:
            logger.info(f"Configuring {model.identifier}")

            try:
                TokenAuthConfigurationModel.model_validate(model)
            except ValidationError as exception:
                exception_message = (
                    f"Validation error(s) occured for {model.identifier}."
                )
                raise ConfigurationRunFailed(exception_message) from exception

            logger.debug(f"No validation errors found for {model.identifier}")

            defaults = model.model_dump(exclude="identifier")

            try:
                logger.debug(f"Saving {model.identifier}")

                TokenAuth.objects.update_or_create(
                    identifier=model.identifier, defaults=defaults
                )
            except DatabaseError as exception:
                exception_message = f"Failed configuring token {model.identifier}."
                raise ConfigurationRunFailed(exception_message) from exception

            logger.info(f"Configured {model.identifier}")
