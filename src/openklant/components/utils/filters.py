import uuid

from django import forms
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import filters
from drf_spectacular.types import OpenApiTypes

from .expansion import get_expand_options_for_serializer


class ExpandFilter(filters.BaseInFilter, filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        serializer_class = kwargs.pop("serializer_class")

        kwargs.setdefault(
            "choices", get_expand_options_for_serializer(serializer_class)
        )
        kwargs.setdefault(
            "help_text",
            _("Sluit de gespecifieerde gerelateerde resources in in het antwoord."),
        )

        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        return qs


class URLViewFilter(filters.Filter):
    field_class = forms.URLField

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter(self, qs, value: OpenApiTypes.URI) -> QuerySet:
        if value:
            try:
                value = uuid.UUID(value.rstrip("/").split("/")[-1])
            except ValueError:
                return qs.none()

        return super().filter(qs, value)
