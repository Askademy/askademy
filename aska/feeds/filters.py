from django_filters import rest_framework as filters

from feeds.models import Post

class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = ("author", "content")