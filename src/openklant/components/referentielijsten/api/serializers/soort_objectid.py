from rest_framework import serializers

from ...models import SoortObjectid


class SoortObjectidSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoortObjectid
        fields = [
            "code",
            "indicatie_actief",
            "naam",
        ]

    __doc__ = Meta.model.__doc__
