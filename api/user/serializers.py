from rest_framework import serializers
from authentication.models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "name",
            "id",
            "uuid",
            "bio",
        ]
        read_only_fields = [
            "id",
            "uuid",
        ]

    def create(self, validated_data):
        print(f"Validated data: {validated_data}")

        email = validated_data.pop("email", None)
        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")

        if not email:
            raise serializers.ValidationError({"email": _("This field is required.")})

        if password != confirm_password:
            raise serializers.ValidationError(_("Passwords do not match."))

        print(f"Creating user with data: {validated_data}")  # Debugging line
        user = User.objects.create_user(
            email=email,
            password=password,
            confirm_password=confirm_password,
            **validated_data,
        )

        return user
