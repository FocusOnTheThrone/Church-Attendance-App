from django.db import models

from attendance.models import Service


class WeeklySummary(models.Model):
    """
    Stores pre-computed weekly metrics. Scoped per organization.
    """

    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="weekly_summaries",
    )
    week_start = models.DateField()
    week_end = models.DateField()

    total_attendance = models.PositiveIntegerField(default=0)
    visitors_count = models.PositiveIntegerField(default=0)
    healed_count = models.PositiveIntegerField(default=0)
    follow_up_count = models.PositiveIntegerField(default=0)

    generated_at = models.DateTimeField(auto_now_add=True)

    services = models.ManyToManyField(Service, related_name="weekly_summaries", blank=True)

    class Meta:
        unique_together = ("week_start", "week_end")
        ordering = ["-week_start"]

    def __str__(self) -> str:
        return f"Summary {self.week_start} to {self.week_end}"
