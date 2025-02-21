from typing import Any

from django.db.models import Model
from django.utils.module_loading import import_string

from rest_framework.serializers import Serializer
from rest_framework_nested.serializers import NestedHyperlinkedRelatedField


# TODO should be moved to vng-api-common once merged/reviewed
# in Open Zaak: https://github.com/open-zaak/open-zaak/pull/1037
class ExpandSerializer(NestedHyperlinkedRelatedField):
    def __init__(self, *args, **kwargs):
        # For some reason self.field_name is empty for `many=True`
        self.name = kwargs.pop("name")

        self.default_serializer = kwargs.pop("default_serializer")
        self.expanded_serializer = kwargs.pop("expanded_serializer")

        self.default_serializer_kwargs = kwargs.pop("default_serializer_kwargs", {})
        self.expanded_serializer_kwargs = kwargs.pop("expanded_serializer_kwargs", {})

        # Update the serializer specific kwargs with the kwargs used for all
        # serializers
        common_kwargs = kwargs.pop("common_kwargs")
        self.default_serializer_kwargs.update(common_kwargs)
        self.expanded_serializer_kwargs.update(common_kwargs)

        kwargs.update(self.default_serializer_kwargs)

        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        serializer_class = self.default_serializer
        if isinstance(self.default_serializer, str):
            serializer_class = import_string(self.default_serializer)
        serializer = serializer_class(**self.default_serializer_kwargs)
        serializer.parent = self

        if hasattr(self.context["request"], "query_params"):
            expand = self.context["request"].query_params.getlist("expand")
            if self.name in expand:
                serializer_class = self.expanded_serializer
                if isinstance(self.expanded_serializer, str):
                    serializer_class = import_string(self.expanded_serializer)
                serializer = serializer_class(**self.expanded_serializer_kwargs)
                serializer.parent = self

        if self.default_serializer_kwargs.get("many", False):
            value = value.all()

        return serializer.to_representation(value)


def get_field_value(
    serializer: Serializer, attrs: dict[str, Any], field_name: str
) -> Any:
    """
    Helper function to retrieve a field value from either the attrs (new data)
    or the instance (existing data during updates).

    :param serializer: The serializer instance
    :param attrs: The attributes passed to `.validate`
    :param field_name: The name of the field to retrieve
    :return: The value of the field, or None if not present
    """
    if field_name in attrs:
        return attrs.get(field_name)
    # Fallback to instance value if it exists
    if serializer.instance:
        return getattr(serializer.instance, field_name, None)
    return None


def get_field_instance_by_uuid(
    serializer: Serializer,
    attrs: dict[str, Any],
    field_name: str,
    model_class: type[Model],
):
    """
    Retrieves an instance of the specified model using the UUID present in the serializer data.

    :param serializer: The serializer instance used to validate the data.
    :param attrs: The dictionary of attributes from the validated data.
    :param field_name: The name of the field from which to extract the value.
    :param model_class: The Django model class from which to retrieve the instance.
    :return: The instance or None if not present returned from get_field_value method
    """
    field_value = get_field_value(serializer, attrs, field_name)
    if field_value and not isinstance(field_value, model_class):
        field_value = model_class.objects.get(uuid=field_value["uuid"])
    return field_value
