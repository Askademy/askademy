from django.contrib import admin
from .models import Post, Comment, Reply


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    inlines = [ReplyInline]
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ("id", "author")
    list_filter = ("author",)
    search_fields = ("content", "author__first_name", "author__last_name")
