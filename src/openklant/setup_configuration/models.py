from django.db import models
from django.utils.translation import gettext_lazy as _

from django_setup_configuration.fields import DjangoModelRef
from django_setup_configuration.models import ConfigurationModel

from openklant.components.token.models import TokenAuth
from openklant.config.models import ReferentielijstenConfig


class TokenAuthConfigurationModel(ConfigurationModel):
    class Meta:
        django_model_refs = {
            TokenAuth: (
                "identifier",
                "token",
                "contact_person",
                "email",
                "organization",
                "application",
                "administration",
            )
        }
        extra_kwargs = {
            "identifier": {"examples": ["open-inwoner"]},
            "token": {"examples": ["modify-this"]},
            "contact_person": {"examples": ["John Doe"]},
            "email": {"examples": ["person@municipality.nl"]},
            "organization": {"examples": ["Municipality name"]},
            "application": {"examples": ["Open Inwoner"]},
        }


class TokenAuthGroupConfigurationModel(ConfigurationModel):
    items: list[TokenAuthConfigurationModel]


class ReferentielijstenConfigurationModel(ConfigurationModel):
    enabled = models.BooleanField(
        default=False,
        help_text=_("Indicates whether Referentielijsten is enabled"),
    )
    referentielijsten_api_service_identifier: str = DjangoModelRef(
        ReferentielijstenConfig,
        "service",
        examples=["referentielijsten-api"],
        verbose_name=_("Referentielijsten Service Identifier"),
    )
    kanalen_tabel_code = models.CharField(
        max_length=100,
        help_text=_("Code of the table containing the channel options"),
        null=True,
        blank=True,
    )

    class Meta:
        django_model_refs = {
            ReferentielijstenConfig: [
                "enabled",
                "kanalen_tabel_code",
            ]
        }
