from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model so we can easily extend with roles later if needed.
    """

    # For now we just keep Django's default fields.
    # Later we can add things like 'role' (admin/pastor/data_entry) here.

    def __str__(self) -> str:
        return self.get_full_name() or self.username
