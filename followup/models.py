from django.db import models
from django.contrib.auth import get_user_model

from attendance.models import Person

User = get_user_model()


class FollowUpCase(models.Model):
    """
    A follow-up case for a person who needs pastoral contact.

    Reason could be 'absent_N_weeks' or 'manual'. Status tracks progress.
    """

    REASON_ABSENT = "absent_N_weeks"
    REASON_MANUAL = "manual"
    REASON_CHOICES = [
        (REASON_ABSENT, "Absent for N weeks"),
        (REASON_MANUAL, "Manual"),
    ]

    STATUS_OPEN = "open"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_RESOLVED = "resolved"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="followup_cases")
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, default=REASON_ABSENT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)

    description = models.TextField(blank=True)

    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="followup_assigned",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["status", "-created_at"]

    def __str__(self) -> str:
        return f"Follow-up for {self.person} ({self.get_status_display()})"
