from django.contrib import admin

from .models import Person, Service, Attendance, Fellowship


@admin.register(Fellowship)
class FellowshipAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("name",)
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('people')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "gender", "title", "fellowship", "phone", "email", "first_visit_date")
    list_filter = ("gender", "title", "fellowship")
    search_fields = ("full_name", "phone", "email")
    raw_id_fields = ("fellowship",)


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
