from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from projects.models import Project
from .models import Bug
from .serializers import BugSerializer


class BugViewSet(viewsets.ModelViewSet):
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["project", "status", "severity", "assignee"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        user = self.request.user
        return Bug.objects.filter(
            Q(project__owner=user) | Q(project__members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        is_member = (
            project.owner == self.request.user
            or project.members.filter(user=self.request.user).exists()
        )
        if not is_member:
            raise PermissionDenied("You are not a member of this project.")
        serializer.save(reporter=self.request.user)