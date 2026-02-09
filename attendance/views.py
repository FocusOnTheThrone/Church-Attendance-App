from rest_framework import viewsets, permissions
from .models import Person, Service, Attendance
from .serializers import PersonSerializer, ServiceSerializer, AttendanceSerializer


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list, create, view, update, and delete people.
    """
    queryset = Person.objects.all().order_by("full_name")
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage services (Sunday, midweek, special meetings, etc.).
    """
    queryset = Service.objects.all().order_by("-date", "-start_time")
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        When a new service is created via the API, automatically
        set 'created_by' to the logged-in user.
        """
        serializer.save(created_by=self.request.user)

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint to mark attendance for a service.
    """
    queryset = Attendance.objects.select_related("person", "service")
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        person = serializer.validated_data["person"]

        # Detect first-time visitor
        has_attended_before = Attendance.objects.filter(
            person=person
        ).exists()

        serializer.save(
            is_first_time_visitor=not has_attended_before
        )
