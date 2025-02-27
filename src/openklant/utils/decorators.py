from functools import wraps

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models

from rest_framework.exceptions import ValidationError
from rest_framework.fields import get_error_detail


def handle_db_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except models.ProtectedError as protected_err:
            raise ValidationError(
                {"nonFieldErrors": protected_err.args[0]},
                code="invalid",
            )
        except DjangoValidationError as validation_err:
            raise ValidationError(get_error_detail(validation_err))

    return wrapper
