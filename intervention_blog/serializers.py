from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Blog, Comment, Tag, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password")

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "This email is already registered"})
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "This username is already registered"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserProfile
        fields = ("id", "user_email", "user_username", "is_author", "created_at")

    def update(self, instance, validated_data):
        instance.is_author = validated_data.get("is_author", instance.is_author)
        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    author_id = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(
            serializers.CurrentUserDefault()
        ),
        write_only=True
    )

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )

    # tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"

    def create(self, validated_data) -> Blog:
        user_instance = validated_data.pop("author_id")
        author_profile = user_instance.profile
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
    class Meta:
        model = Comment
        fields = "__all__"

