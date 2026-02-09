from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FollowUpCaseViewSet, FollowUpSuggestionsView, GenerateFollowUpCasesView

router = DefaultRouter()
router.register(r"cases", FollowUpCaseViewSet, basename="followup-case")

urlpatterns = [
    path("", include(router.urls)),
    path("suggestions/", FollowUpSuggestionsView.as_view(), name="followup-suggestions"),
    path("generate/", GenerateFollowUpCasesView.as_view(), name="followup-generate"),
]

