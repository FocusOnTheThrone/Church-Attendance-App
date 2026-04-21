from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    """
    Represents a church. Each organization's data (people, services, etc.) is isolated.
    """

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    """
    Custom user model. Each user belongs to one primary Organization (church).
    Users can optionally have access to additional organizations (e.g. staff serving multiple churches).
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users",
    )
    organizations = models.ManyToManyField(
        Organization,
        blank=True,
        related_name="members",
        help_text="Additional organizations this user can switch to.",
    )

    def get_accessible_organizations(self):
        """Return all organizations this user can access."""
        orgs = list(self.organizations.all())
        if self.organization and self.organization not in orgs:
            orgs.insert(0, self.organization)
        return orgs

    def __str__(self) -> str:
        return self.get_full_name() or self.username
