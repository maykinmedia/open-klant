from rest_framework import serializers

from ...models import Kanaal


class KanaalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kanaal
        fields = [
            "code",
            "indicatie_actief",
            "naam",
        ]

    __doc__ = Meta.model.__doc__
