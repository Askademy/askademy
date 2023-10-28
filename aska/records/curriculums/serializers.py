from django.urls import reverse
from rest_framework import serializers
import re

from records.curriculums.models import (
    Curriculum,
    Strand,
    Substrand,
    Lesson,
)


class LessonSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="subject.name")
    strand = serializers.CharField(source="strand.name")
    substrand = serializers.CharField(source="substrand.name")
    url = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Update fields based on the provided list
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_url(self, instance):
        abs_url = self.context["request"].build_absolute_uri
        pattern = r"b\d+(-\w+)+"
        for text in abs_url().split("/"):
            match = re.search(pattern, text)
            if match:
                break
        curriculum = match.group()
        return abs_url(reverse("api:curriculums-lesson", args=[curriculum, instance.slug]))

    class Meta:
        model = Lesson
        fields = [
            "number",
            "grade",
            "subject",
            "strand",
            "substrand",
            "topic",
            "content",
            "url",
        ]


class SubstrandSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, fields=["topic", "url"])

    class Meta:
        model = Substrand
        fields = ["number", "name", "lessons"]


class StrandSerializer(serializers.ModelSerializer):
    substrands = SubstrandSerializer(many=True)

    class Meta:
        model = Strand
        fields = ["number", "name", "substrands"]


class CurriculumSerializer(serializers.ModelSerializer):
    strands = serializers.SerializerMethodField()
    subject = serializers.CharField(source="subject.name")

    def get_strands(self, instance):
        abs_url = self.context["request"].build_absolute_uri
        return abs_url(instance.strands_url)

    class Meta:
        model = Curriculum
        fields = ["id", "grade", "subject", "strands"]
