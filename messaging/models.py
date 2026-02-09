from django.db import models


class WhatsAppMessageLog(models.Model):
    """
    Stores a record of each WhatsApp message we try to send.
    """

    STATUS_QUEUED = "queued"
    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_QUEUED, "Queued"),
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
    ]

    recipient = models.CharField(max_length=32)  # phone number in international format
    template_name = models.CharField(max_length=100, blank=True)
    payload_preview = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED)
    provider_message_id = models.CharField(max_length=100, blank=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.recipient} ({self.status})"
