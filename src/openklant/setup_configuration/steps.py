import logging

from django.db import DatabaseError

from django_setup_configuration.configuration import BaseConfigurationStep
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
            try:
                TokenAuthConfigurationModel.model_validate(model)
            except ValidationError as exception:
                logger.exception(
                    f"Validation error(s) occured for {model.identifier}: {exception}."
                    " Continueing.."
                )

                continue

            defaults = model.model_dump(exclude="identifier")

            try:
                logger.debug(f"Configuring {model.identifier}")

                TokenAuth.objects.update_or_create(
                    identifier=model.identifier, defaults=defaults
                )
            except DatabaseError:
                logger.exception(
                    f"Failed configuring token {model.identifier}. Continuing.."
                )
                continue
