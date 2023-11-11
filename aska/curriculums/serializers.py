from django.urls import reverse
from rest_framework import serializers
import re

from curriculums.models import (
    Subject,
    Curriculum,
    Strand,
    Substrand,
    ContentStandard,
    LearningIndicator,
    Lesson,
)


class LessonSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="subject.name")
    strand = serializers.CharField(source="strand.name")
    substrand = serializers.CharField(source="substrand.name")
    url = serializers.SerializerMethodField()

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

class ContentStandardSerializer(serializers.ModelSerializer):


    class Meta:
        model = ContentStandard
        fields = ["annotation", "description"]


class SubstrandSerializer(serializers.ModelSerializer):
    content_standards = ContentStandardSerializer(many=True)

    class Meta:
        model = Substrand
        fields = ["annotation", "name", "content_standards"]


class StrandSerializer(serializers.ModelSerializer):
    substrands = SubstrandSerializer(many=True)

    class Meta:
        model = Strand
        fields = ["name", "annotation", "substrands"]


class CurriculumSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(source="grade.name")
    subject = serializers.CharField(source="subject.name")
    strands = serializers.SerializerMethodField()

    def get_strands(self, instance):
        return self.context["request"].build_absolute_uri(
            reverse("api:curriculums-detail", args=[instance.annotation.lower()])
        )


    class Meta:
        model = Curriculum
        fields = ["id", "grade", "subject", "strands"]
