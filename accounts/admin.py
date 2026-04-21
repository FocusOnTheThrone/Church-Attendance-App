from django.contrib import admin

from .models import Organization, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "organization", "is_staff", "is_superuser", "is_active")
    list_filter = ("organization", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    filter_horizontal = ("organizations",)