from django.urls import path, re_path, include

from .views import CurriculumsView, LessonView

urlpatterns = [
    path("", CurriculumsView.as_view(), name="curriculums"),
    re_path(r"^(?P<curriculum>b\d+(-\w+)+)/$", LessonView.as_view(), name="lesson"),
]
