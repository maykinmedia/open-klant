from rest_framework import serializers

from ...models import Taal


class TaalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taal
        fields = [
            "code",
            "indicatie_actief",
            "naam",
        ]

    __doc__ = Meta.model.__doc__
