from django.urls import path

from .views import PostCreateView, PostDetailView


urlpatterns = [
   path("post/create/", PostCreateView.as_view(), name="create-post"),
   path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
  
]
