from authentication import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uuid",
            "name",
            "bio",
            "email",
        ]
        read_only_fields = [
            "id",
            "uuid",
            "email",
        ]
