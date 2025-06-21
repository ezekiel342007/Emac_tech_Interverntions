from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class CommentSeralizer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
