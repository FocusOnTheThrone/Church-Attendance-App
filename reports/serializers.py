from rest_framework import serializers

from .models import WeeklySummary


class WeeklySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklySummary
        fields = [
            "id",
            "week_start",
            "week_end",
            "total_attendance",
            "visitors_count",
            "healed_count",
            "follow_up_count",
            "generated_at",
            "services",
        ]

