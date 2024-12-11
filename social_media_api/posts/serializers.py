from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "comments",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
