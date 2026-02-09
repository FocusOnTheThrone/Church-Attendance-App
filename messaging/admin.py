from django.contrib import admin

from .models import WhatsAppMessageLog


@admin.register(WhatsAppMessageLog)
class WhatsAppMessageLogAdmin(admin.ModelAdmin):
    list_display = ("recipient", "template_name", "status", "created_at")
    list_filter = ("status", "template_name")
    search_fields = ("recipient", "template_name")
