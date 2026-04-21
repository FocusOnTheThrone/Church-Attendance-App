from django.db import models
from django.contrib.auth import get_user_model

from attendance.models import Person, Service

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


class FollowUpRecord(models.Model):
    """
    Individual follow-up attempt record for a specific service/absence.
    Tracks when contact was made and the outcome.
    """

    METHOD_PHONE = "phone"
    METHOD_VISIT = "visit"
    METHOD_TEXT = "text"
    METHOD_EMAIL = "email"
    METHOD_WHATSAPP = "whatsapp"
    METHOD_OTHER = "other"
    METHOD_CHOICES = [
        (METHOD_PHONE, "Phone Call"),
        (METHOD_VISIT, "Home Visit"),
        (METHOD_TEXT, "SMS"),
        (METHOD_EMAIL, "Email"),
        (METHOD_WHATSAPP, "WhatsApp"),
        (METHOD_OTHER, "Other"),
    ]

    OUTCOME_SUCCESSFUL = "successful"
    OUTCOME_UNSUCCESSFUL = "unsuccessful"
    OUTCOME_PENDING = "pending"
    OUTCOME_NEEDS_RETRY = "needs_retry"
    OUTCOME_CHOICES = [
        (OUTCOME_SUCCESSFUL, "Successful Contact"),
        (OUTCOME_UNSUCCESSFUL, "Unsuccessful Contact"),
        (OUTCOME_PENDING, "Pending"),
        (OUTCOME_NEEDS_RETRY, "Needs Retry"),
    ]

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="followup_records")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="followup_records", null=True, blank=True)
    followup_case = models.ForeignKey(FollowUpCase, on_delete=models.CASCADE, related_name="records", null=True, blank=True)
    
    # Who made the contact
    contacted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="followup_made")
    
    # Contact details
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default=METHOD_PHONE)
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, default=OUTCOME_PENDING)
    
    # Comments and notes
    comments = models.TextField(help_text="Details about the conversation and outcome")
    response_notes = models.TextField(blank=True, help_text="How the person responded, any concerns mentioned")
    
    # Timestamps
    contact_date = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateField(help_text="Date the follow-up was attempted")
    
    # Completion tracking
    is_completed = models.BooleanField(default=False, help_text="Check if follow-up was successfully completed")
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-follow_up_date", "-contact_date"]
        indexes = [
            models.Index(fields=['person', '-follow_up_date']),
            models.Index(fields=['service', '-follow_up_date']),
            models.Index(fields=['is_completed', '-follow_up_date']),
        ]

    def __str__(self) -> str:
        return f"Follow-up for {self.person} on {self.follow_up_date} ({self.get_method_display()})"

    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)
