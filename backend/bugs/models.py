from django.conf import settings
from django.db import models

from projects.models import Project


class Bug(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
        ("reopened", "Reopened"),
    ]
    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bugs")
    title = models.CharField(max_length=200)
    description = models.TextField()
    steps_to_reproduce = models.TextField(blank=True)
    environment = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="medium")
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reported_bugs",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_bugs",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title