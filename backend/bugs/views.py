from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Bug
from .serializers import BugSerializer

User = get_user_model()

ALLOWED_TRANSITIONS = {
    "open": ["assigned"],
    "assigned": ["in_progress"],
    "in_progress": ["resolved"],
    "resolved": ["closed", "reopened"],
    "closed": ["reopened"],
    "reopened": ["assigned", "in_progress"],
}


def is_project_member(project, user):
    return (
        project.owner == user
        or project.members.filter(user=user).exists()
    )


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
        if not is_project_member(project, self.request.user):
            raise PermissionDenied("You are not a member of this project.")
        serializer.save(reporter=self.request.user)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        bug = self.get_object()
        if bug.project.owner != request.user:
            raise PermissionDenied("Only the project owner can assign bugs.")

        assignee_id = request.data.get("assignee")
        try:
            assignee = User.objects.get(pk=assignee_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"detail": "Invalid assignee."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_project_member(bug.project, assignee):
            return Response(
                {"detail": "Assignee must be a member of this project."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bug.assignee = assignee
        bug.status = "assigned"
        bug.save()
        return Response(BugSerializer(bug).data)

    @action(detail=True, methods=["post"])
    def change_status(self, request, pk=None):
        bug = self.get_object()
        new_status = request.data.get("status")

        can_change = (
            bug.project.owner == request.user or bug.assignee == request.user
        )
        if not can_change:
            raise PermissionDenied(
                "Only the project owner or the assignee can change status."
            )

        if new_status not in ALLOWED_TRANSITIONS.get(bug.status, []):
            return Response(
                {
                    "detail": f"Cannot change from '{bug.status}' to '{new_status}'.",
                    "allowed": ALLOWED_TRANSITIONS.get(bug.status, []),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        bug.status = new_status
        bug.save()
        return Response(BugSerializer(bug).data)