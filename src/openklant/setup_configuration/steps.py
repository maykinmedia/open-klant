import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django_setup_configuration.configuration import BaseConfigurationStep
from django_setup_configuration.exceptions import ConfigurationRunFailed

from openklant.components.token.models import TokenAuth
from openklant.setup_configuration.models import TokenAuthGroupConfigurationModel

logger = logging.getLogger(__name__)


class TokenAuthConfigurationStep(
    BaseConfigurationStep[TokenAuthGroupConfigurationModel]
):
    """
    Configure configuration groups for the Objects API backend
    """

    namespace = "zgw_tokens_tokenauth"
    enable_setting = "zgw_tokens_tokenauth_config_enable"

    verbose_name = "Configuration to set up authentication tokens for Open Klant"
    config_model = TokenAuthGroupConfigurationModel

    def execute(self, model: TokenAuthGroupConfigurationModel) -> None:
        for item in model.items:
            logger.info(f"Configuring {item.identifier}")

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

            logger.debug(f"No validation errors found for {item.identifier}")

            try:
                logger.debug(f"Saving {item.identifier}")

                TokenAuth.objects.update_or_create(
                    identifier=item.identifier,
                    defaults={
                        key: value
                        for key, value in model_kwargs.items()
                        if key != "identifier"
                    },
                )
            except IntegrityError as exception:
                exception_message = f"Failed configuring token {item.identifier}."
                raise ConfigurationRunFailed(exception_message) from exception

            logger.info(f"Configured {item.identifier}")
