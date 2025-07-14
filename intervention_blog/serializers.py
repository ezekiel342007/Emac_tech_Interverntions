from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Blog, Comment, Tag, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user", {})
        user = UserSerializer().create(user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user_instance = instance.user

        for attr, value in user_data.items():
            setattr(user_instance, attr, value)
        user_instance.save()

        for attr, value in instance.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = "__all__"


class CommentSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

