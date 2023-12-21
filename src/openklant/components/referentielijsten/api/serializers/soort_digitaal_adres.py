from rest_framework import serializers

from ...models import SoortDigitaalAdres


class SoortDigitaalAdresSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoortDigitaalAdres
        fields = [
            "code",
            "indicatie_actief",
            "naam",
        ]
