from django.urls import path, include

from . import views

app_name = "web"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("search/", views.search_results, name="search"),
    path("about/", views.about_view, name="about-askademy"),
    path(
        "profile/update/",
        views.UpdateUserProfileView.as_view(),
        name="update-user-profile",
    ),
    path("curriculums/", include("web.curriculums.urls")),
    path("", include("web.users.urls")),
]
