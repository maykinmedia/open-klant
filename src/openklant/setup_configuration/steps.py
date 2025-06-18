from django.core.exceptions import ValidationError
from django.db import IntegrityError

import structlog
from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import ConfigurationRunFailed

from openklant.components.token.models import TokenAuth
from openklant.setup_configuration.models import TokenAuthGroupConfigurationModel

logger = structlog.stdlib.get_logger(__name__)


class TokenAuthConfigurationStep(
    BaseConfigurationStep[TokenAuthGroupConfigurationModel]
):
    """
    Configure tokens for other applications to access the APIs provided by Open Klant
    """

    namespace = "tokenauth"
    enable_setting = "tokenauth_config_enable"

    verbose_name = "Configuration to set up authentication tokens for Open Klant"
    config_model = TokenAuthGroupConfigurationModel

    def execute(self, model: TokenAuthGroupConfigurationModel) -> None:
        if len(model.items) == 0:
            logger.warning("no_tokens_defined")

        for item in model.items:
            logger.info("configuring_token", identifier=item.identifier)

            model_kwargs = dict(
                identifier=item.identifier,
                token=item.token,
                contact_person=item.contact_person,
                email=item.email,
                organization=item.organization,
                application=item.application,
                administration=item.administration,
            )

            token_instance = TokenAuth(**model_kwargs)

            try:
                token_instance.full_clean(exclude=("id",), validate_unique=False)
            except ValidationError as exception:
                exception_message = (
                    f"Validation error(s) occured for {item.identifier}."
                )
                raise ConfigurationRunFailed(exception_message) from exception

            logger.debug("no_validation_errors_found", identifier=item.identifier)

            try:
                logger.debug("save_token_to_database", identifier=item.identifier)

                TokenAuth.objects.update_or_create(
                    identifier=item.identifier,
                    defaults={
                        key: value
                        for key, value in model_kwargs.items()
                        if key != "identifier"
                    },
                )
            except IntegrityError as exception:
                logger.exception(
                    "token_configuration_failure",
                    token_identifier=item.identifier,
                    exc_info=exception,
                )
                exception_message = f"Failed configuring token {item.identifier}."
                raise ConfigurationRunFailed(exception_message) from exception

            logger.info("token_configuration_success", token_identifier=item.identifier)
