from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, ServiceViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r"people", PersonViewSet, basename="person")
router.register(r"services", ServiceViewSet, basename="service")
router.register(r'attendances', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path("", include(router.urls)),
]
