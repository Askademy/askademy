from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .filters import PostFilter
from records.feeds.models import Post, Comment, Reply
from records.feeds.serializers import PostSerializer


class FeedsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter


