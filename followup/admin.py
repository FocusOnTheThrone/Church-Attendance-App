from django.contrib import admin

from .models import FollowUpCase


@admin.register(FollowUpCase)
class FollowUpCaseAdmin(admin.ModelAdmin):
    list_display = ("person", "reason", "status", "assigned_to", "created_at", "resolved_at")
    list_filter = ("status", "reason")
    search_fields = ("person__full_name", "assigned_to__username")
