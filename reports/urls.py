from django.urls import path

from .views import WeeklySummaryView, WeeklyReportTextView, AttendanceTrendView, set_gender

urlpatterns = [
    path("weekly-summary/", WeeklySummaryView.as_view(), name="weekly-summary"),
    path("weekly-text/", WeeklyReportTextView.as_view(), name="weekly-text"),
    path("attendance-trend/", AttendanceTrendView.as_view(), name="attendance-trend"),
    path("set-gender/", set_gender, name="set-gender"),
]

