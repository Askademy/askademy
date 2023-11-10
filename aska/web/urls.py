from django.urls import path, include

from users.views import HomePageView
from .views import about_view, search_results

app_name = "web"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("search/", search_results, name="search"),
    path("about/", about_view, name="about-askademy"),
    path("chat/", include("chats.urls")),
    path("curriculums/", include("curriculums.urls")),
    path("feeds/", include("feeds.urls")),
    path("", include("users.urls")),
]
