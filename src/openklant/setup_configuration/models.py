from django_setup_configuration.models import ConfigurationModel

from openklant.components.token.models import TokenAuth


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


class TokenAuthGroupConfigurationModel(ConfigurationModel):
    items: list[TokenAuthConfigurationModel]
