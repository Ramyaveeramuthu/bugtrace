from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Bug, Comment


class BugSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Bug
        fields = [
            "id",
            "project",
            "title",
            "description",
            "steps_to_reproduce",
            "environment",
            "status",
            "severity",
            "reporter",
            "assignee",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "bug", "author", "text", "created_at"]
        read_only_fields = ["bug", "created_at"]