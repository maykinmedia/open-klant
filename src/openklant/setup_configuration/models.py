from typing import Any, Self

from django.core.exceptions import ValidationError

from pydantic import Field, ValidationError as PydanticValidationError
from django_setup_configuration.models import ConfigurationModel
from django_setup_configuration.fields import DjangoModelRef

from openklant.components.token.models import TokenAuth


class TokenAuthConfigurationModel(ConfigurationModel):
    organization = DjangoModelRef(TokenAuth, "organization", default="")
    application = DjangoModelRef(TokenAuth, "application", default="")
    administration = DjangoModelRef(TokenAuth, "administration", default="")

    class Meta:
        django_model_refs = {
            TokenAuth: (
                "identifier",
                "contact_person",
                "email",
            )
        }

    @classmethod
    def model_validate(cls, obj: Any, *args, **kwargs) -> Self:
        model = super().model_validate(obj, *args, **kwargs)

        model_class = next(model.Meta.django_model_refs.keys())
        instance = model_class(model.model_dump())

        try:
            instance.clean()
        except ValidationError as exception:
            raise PydanticValidationError(exception.message_dict) from exception

        return model



class TokenAuthGroupConfigurationModel(ConfigurationModel):
    group: list[TokenAuthConfigurationModel] = Field(default_factory=list)
