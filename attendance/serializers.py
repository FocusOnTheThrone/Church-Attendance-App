from rest_framework import serializers
from .models import Person, Service, Attendance


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "id",
            "full_name",
            "gender",
            "date_of_birth",
            "phone",
            "email",
            "title",
            "first_visit_date",
            "notes",
            "created_at",
            "updated_at",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "date",
            "start_time",
            "service_type",
            "title",
            "location",
            "notes",
            "created_by",
            "created_at",
            "updated_at",
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "service",
            "person",
            "category",
            "present",
            "is_first_time_visitor",
            "is_healed_this_service",
            "notes",
            "created_at",
        ]
        read_only_fields = ["is_first_time_visitor", "created_at"]

    def validate(self, attrs):
        service = attrs["service"]
        person = attrs["person"]

        if Attendance.objects.filter(service=service, person=person).exists():
            raise serializers.ValidationError(
                "This person is already marked for this service."
            )

        return attrs