from rest_framework import serializers

from .models import Blog, Comment, Tag, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


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

