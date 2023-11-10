from rest_framework.routers import DefaultRouter

from users.api_views import UserProfileViewSet, AuthUserViewSet
from schools.api_views import SchoolProfileViewSet
from curriculums.api_views import CurriculumViewSet
from assessments.api_views import AssessmentViewSet
from searches.api_views import SearchViewSet
from feeds.api_views import FeedsViewSet


router = DefaultRouter()

router.register(r"auth", AuthUserViewSet, basename="auth")
router.register(r"users", UserProfileViewSet, basename="users")
router.register(r"schools", SchoolProfileViewSet, basename="schools")
router.register(r"curriculums", viewset=CurriculumViewSet, basename="curriculums")
router.register(r"assessments", AssessmentViewSet, basename="assessments")
router.register(r"search", SearchViewSet, basename="searches")
router.register(r"feeds", FeedsViewSet, basename="feeds")