from django.urls import path, include

from .views import CurriculumsView, LessonView

urlpatterns = [
    path("", CurriculumsView.as_view(), name="curriculums"),
    path("<str:curriculum>/", LessonView.as_view(), name="lesson")
]
