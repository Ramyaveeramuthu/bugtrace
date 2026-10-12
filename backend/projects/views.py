from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.models import User
from .models import Project, ProjectMember
from .serializers import AddMemberSerializer, MemberSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(owner=user) | Q(members__user=user)).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(project=project, user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("Only the owner can edit this project.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Only the owner can delete this project.")
        instance.delete()

    @action(detail=True, methods=["get", "post"])
    def members(self, request, pk=None):
        project = self.get_object()

        if request.method == "GET":
            qs = project.members.select_related("user")
            return Response(MemberSerializer(qs, many=True).data)

        if project.owner != request.user:
            raise PermissionDenied("Only the owner can add members.")

        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.validated_data["username"])
        ProjectMember.objects.get_or_create(project=project, user=user)
        return Response({"detail": "Member added."}, status=201)