from django_filters import filters

from .expansion import get_expand_options_for_serializer


class ExpandFilter(filters.BaseInFilter, filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        serializer_class = kwargs.pop("serializer_class")

        kwargs.setdefault(
            "choices", get_expand_options_for_serializer(serializer_class)
        )

        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        return qs
