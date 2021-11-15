from django_filters import filters


class ExpandFilter(filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        serializer_class = kwargs.pop("serializer_class")
        kwargs.setdefault(
            "choices", [(x, x) for x in serializer_class.Meta.expandable_fields]
        )

        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        return qs
