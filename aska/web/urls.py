from django.urls import path, include

from . import views

app_name = "web"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("post/create/", views.PostCreateView.as_view(), name="create-post"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("search/", views.search_results, name="search"),
    path("about/", views.about_view, name="about-askademy"),
    path("curriculums/", include("web.curriculums.urls")),
    path("", include("web.users.urls")),
]
