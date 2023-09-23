from django.db import models

from records.users.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser, related_name="posts", on_delete=models.CASCADE
    )
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to="media/posts/")
    timestamp = models.DateTimeField(auto_now_add=True)
    shares = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"Post {self.id} by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} by {self.author} on Post {self.post.id}"


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply {self.id} by {self.author} on Comment {self.comment.id}"
