from rest_framework import serializers

from users.models import CustomUser
from users.serializers import CustomUserSerializer

from .models import Blog, Comment, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    author_id = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(
            serializers.CurrentUserDefault()),
        write_only=True,
    )

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )

    class Meta:
        model = Blog
        fields = "__all__"

    def create(self, validated_data) -> Blog:
        user_email = validated_data.pop("author_id")
        author_profile = CustomUser.objects.get(email=user_email)
        tags_data = validated_data.pop("tags", [])
        blog = Blog.objects.create(author=author_profile, **validated_data)
        blog.tags.set(tags_data)
        return blog

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        if tags_data is not None:
            instance.tags.set(tags_data)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance


class CommentSeralizer(serializers.ModelSerializer):
    author_id = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(
            serializers.CurrentUserDefault()),
        write_only=True,
    )

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data) -> Comment:
        selected_blog = Blog.objects.get(title=validated_data.pop("blog"))
        commenter = CustomUser.objects.get(
            email=validated_data.pop("author_id"))

        comment = Comment.objects.create(
            blog=selected_blog, writer=commenter, **validated_data
        )
        return comment
