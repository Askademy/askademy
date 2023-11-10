from django.urls import path, re_path, include

from .views import CurriculumsView, LessonView

urlpatterns = [
    path("", CurriculumsView.as_view(), name="curriculums"),
    re_path(r"^(?P<curriculum>[a-z]+:b[4-9])/$", LessonView.as_view(), name="lesson"),
]
