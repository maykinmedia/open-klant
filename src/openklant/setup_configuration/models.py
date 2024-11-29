from typing import Any, Self

from django.core.exceptions import ValidationError

from django_setup_configuration.fields import DjangoModelRef
from django_setup_configuration.models import ConfigurationModel
from pydantic import Field, ValidationError as PydanticValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError

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

        # note that this will not work with multiple models
        model_class = next(iter(model.Meta.django_model_refs.keys()))
        model_data = model.model_dump()

        instance = model_class(**model_data)

        try:
            instance.full_clean(exclude=("id", "token"), validate_unique=False)
        except ValidationError as exception:
            raise PydanticValidationError.from_exception_data(
                str(exception),
                list(
                    InitErrorDetails(
                        input=error, type=PydanticCustomError("custom_error", error)
                    )
                    for _, errors in exception.message_dict.items()
                    for error in errors
                ),
            ) from exception

        return model


class TokenAuthGroupConfigurationModel(ConfigurationModel):
    group: list[TokenAuthConfigurationModel] = Field(default_factory=list)
