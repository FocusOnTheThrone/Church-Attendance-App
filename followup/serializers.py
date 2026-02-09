from rest_framework import serializers

from attendance.models import Person
from .models import FollowUpCase


from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUpCaseSerializer(serializers.ModelSerializer):
    # Friendly read-only fields so the API response is easier to understand
    person_name = serializers.CharField(source="person.full_name", read_only=True)
    assigned_to_username = serializers.CharField(source="assigned_to.username", read_only=True)

    # Keep these writable as IDs
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        queryset=User.objects.all(),
    )

    class Meta:
        model = FollowUpCase
        fields = [
            "id",
            "person",
            "person_name",
            "reason",
            "status",
            "description",
            "assigned_to",
            "assigned_to_username",
            "created_at",
            "updated_at",
            "resolved_at",
        ]

