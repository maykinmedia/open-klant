from rest_framework import serializers

from ...models import SoortObject


class SoortObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoortObject
        fields = [
            "code",
            "indicatie_actief",
            "naam",
        ]
