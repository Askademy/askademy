from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance):
        return {
            "author": instance.author.get_full_name(),
            "content": instance.content,
            "likes": list(instance.likes.all()),
            "image": instance.image.url if instance.image else None
        }
    

    class Meta:
        model = Post
        fields = ("content", "image",)