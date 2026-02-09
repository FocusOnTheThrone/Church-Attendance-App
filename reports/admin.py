from django.contrib import admin

from .models import WeeklySummary


@admin.register(WeeklySummary)
class WeeklySummaryAdmin(admin.ModelAdmin):
    list_display = (
        "week_start",
        "week_end",
        "total_attendance",
        "visitors_count",
        "healed_count",
        "follow_up_count",
        "generated_at",
    )
    list_filter = ("week_start",)
