from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FollowUpCaseViewSet, FollowUpSuggestionsView, GenerateFollowUpCasesView, batch_create_followup
from .personal_views import personal_report

router = DefaultRouter()
router.register(r"cases", FollowUpCaseViewSet, basename="followup-case")

urlpatterns = [
    path("", include(router.urls)),
    path("suggestions/", FollowUpSuggestionsView.as_view(), name="followup-suggestions"),
    path("generate/", GenerateFollowUpCasesView.as_view(), name="followup-generate"),
    path("batch-create/", batch_create_followup, name="followup-batch-create"),
    path("person/<int:person_id>/", personal_report, name="personal-report"),
]

