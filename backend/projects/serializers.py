from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Project, ProjectMember


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "owner", "created_at"]
        read_only_fields = ["created_at"]


class AddMemberSerializer(serializers.Serializer):
    username = serializers.CharField()


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ["id", "user"]