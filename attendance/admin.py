from django.contrib import admin

from .models import Person, Service, Attendance


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "gender", "title", "phone", "email", "first_visit_date")
    list_filter = ("gender", "title")
    search_fields = ("full_name", "phone", "email")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("date", "service_type", "title", "location")
    list_filter = ("service_type", "date")
    search_fields = ("title", "location")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "person",
        "category",
        "present",
        "is_first_time_visitor",
        "is_healed_this_service",
    )
    list_filter = ("category", "present", "is_first_time_visitor", "is_healed_this_service")
    search_fields = ("person__full_name", "service__title")
