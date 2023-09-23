from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserProfileViewSet,
    SchoolProfileViewSet,
    CurriculumViewSet,
    AssessmentViewSet,
    SearchViewSet,
)

app_name = "api"

router = DefaultRouter()

router.register(r"users", UserProfileViewSet, basename="users")
router.register(r"schools", SchoolProfileViewSet, basename="schools")
router.register(r"curriculums", CurriculumViewSet, basename="curriculums")
router.register(r"assessments", AssessmentViewSet, basename="assessments")
router.register(r"search", SearchViewSet, basename="search")


urlpatterns = [
    path(r"", include(router.urls)),
    path(r"auth/", include("api.users.urls")),
]
