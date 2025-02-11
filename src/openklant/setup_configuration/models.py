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
