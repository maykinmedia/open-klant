from rest_framework import serializers

from ...models import ExternRegister


class ExternRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternRegister
        fields = [
            "code",
            "locatie",
            "naam",
        ]

    __doc__ = Meta.model.__doc__
