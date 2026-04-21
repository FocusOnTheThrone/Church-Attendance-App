from rest_framework import viewsets, permissions
from .models import Person, Service, Attendance
from .serializers import PersonSerializer, ServiceSerializer, AttendanceSerializer


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list, create, view, update, and delete people.
    Scoped to the authenticated user's organization.
    """
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Person.objects.all().order_by("full_name")
        org = getattr(self.request.user, 'organization', None)
        if org:
            qs = qs.filter(organization=org)
        return qs

    def perform_create(self, serializer):
        org = getattr(self.request.user, 'organization', None)
        if org:
            serializer.save(organization=org)
        else:
            serializer.save()


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage services (Sunday, midweek, special meetings, etc.).
    Scoped to the authenticated user's organization.
    """
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Service.objects.all().order_by("-date", "-start_time")
        org = getattr(self.request.user, 'organization', None)
        if org:
            qs = qs.filter(organization=org)
        return qs

    def perform_create(self, serializer):
        org = getattr(self.request.user, 'organization', None)
        serializer.save(
            created_by=self.request.user,
            organization=org,
        )

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint to mark attendance for a service.
    Scoped to services in the user's organization.
    """
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Attendance.objects.select_related("person", "service")
        org = getattr(self.request.user, 'organization', None)
        if org:
            qs = qs.filter(service__organization=org)
        return qs

    def perform_create(self, serializer):
        person = serializer.validated_data["person"]

        # Detect first-time visitor
        has_attended_before = Attendance.objects.filter(
            person=person
        ).exists()

        serializer.save(
            is_first_time_visitor=not has_attended_before
        )
