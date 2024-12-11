from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

CustomUser = get_user_model().objects.create_user


class CustomUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
            "followers",
            "following",
            "token",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = super().create(validated_data)

        token, _ = Token.objects.create(user=user)
        user.token = token.key
        return user
