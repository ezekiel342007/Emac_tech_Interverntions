from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import authenticate

from .models import CustomUser, Watchings


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username"]


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data) -> CustomUser:
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginUserSerializer(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class WatchingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()),
        write_only=True,
    )

    class Meta:
        model = Watchings
        fields = "__all__"

    def create(self, validated_data) -> Watchings:
        watcher = CustomUser.objects.get(email=validated_data.pop("user"))
        author = CustomUser.objects.get(email=validated_data.pop("author"))
        return Watchings.objects.create(
            watcher=watcher, author=author, **validated_data
        )
