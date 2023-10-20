from collections import OrderedDict

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from zds_client import ClientError
from zgw_consumers.constants import APITypes
from zgw_consumers.models import Service

from openklant.components.legacy.contactmomenten.models.contactmomenten import (
    ObjectContactMoment,
)


class ObjectContactMomentDestroyValidator:
    message = _(
        "The canonical remote relation still exists, this relation cannot be deleted."
    )
    code = "remote-relation-exists"
    resource_name = "contactmoment"

    def __call__(self, objectklantinteractie: ObjectContactMoment):
        object_url = objectklantinteractie.object
        for service in Service.objects.filter(api_type=APITypes.zrc):
            if service.api_root in object_url:
                client = service.get_client(object_url)
                resource = f"{objectklantinteractie.object_type}{self.resource_name}"
                try:
                    relations = client.retrieve(
                        resource,
                        url=object_url,
                        request_kwargs={"headers": {"Accept-Crs": "EPSG:4326"}},
                    )
                except ClientError as exc:
                    raise serializers.ValidationError(
                        exc.args[0], code="relation-lookup-error"
                    ) from exc

                if len(relations) >= 1:
                    raise serializers.ValidationError(self.message, code=self.code)

                return True

        raise serializers.ValidationError(
            _("No Zaaktype API configured"), code="configuration-error"
        )


class ObjectContactMomentCreateValidator:
    """
    Validate that the CONTACTMOMENT is already linked to the OBJECT in the remote component.
    """

    message = _("The contactmoment has no relations to {object}")
    code = "inconsistent-relation"
    resource_name = "contactmoment"

    def __call__(self, attrs: OrderedDict):
        object_url = attrs["object"]
        object_type = attrs["object_type"]

        for service in Service.objects.filter(api_type=APITypes.zrc):
            if service.api_root in object_url:
                client = service.get_client(object_url)
                resource = f"{object_type}{self.resource_name}"
                try:
                    relations = client.retrieve(
                        resource,
                        url=object_url,
                        request_kwargs={"headers": {"Accept-Crs": "EPSG:4326"}},
                    )
                except ClientError as exc:
                    raise serializers.ValidationError(
                        exc.args[0], code="relation-lookup-error"
                    ) from exc

                if len(relations) == 0:
                    raise serializers.ValidationError(self.message, code=self.code)

                return True

        raise serializers.ValidationError(
            _("No Zaaktype API configured"), code="configuration-error"
        )
