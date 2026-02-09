"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reports.views import (
    add_member_view,
    dashboard_view,
    delete_person_view,
    event_instances_view,
    event_instance_report_view,
    attendance_analysis_view,
    events_page_view,
    record_attendance_view,
    register_view,
)


@api_view(["GET"])
def api_root(request):
    return Response({"message": "Church Attendance API is running!", "status": "success"})


urlpatterns = [
    path("", events_page_view, name="events"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("add-member/", add_member_view, name="add_member"),
    path("register/delete/<int:person_id>/", delete_person_view, name="delete_person"),
    path("events/<str:service_type>/", event_instances_view, name="event_instances"),
    path("events/<str:service_type>/<int:service_id>/record/", record_attendance_view, name="record_attendance"),
    path("events/<str:service_type>/<int:service_id>/report/", event_instance_report_view, name="event_instance_report"),
    path("events/<str:service_type>/<int:service_id>/analysis/", attendance_analysis_view, name="event_instance_analysis"),
    path("register/", register_view, name="register"),
    path("staff-dashboard/", admin.site.urls),  # Hidden admin panel (only accessible if you know the URL)
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", api_root, name="api-root"),
    path("api/attendance/", include("attendance.urls")),
    path("api/followup/", include("followup.urls")),
    path("api/reports/", include("reports.urls")),
]