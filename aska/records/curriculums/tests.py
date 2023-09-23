from django.test import TestCase
from django.urls import reverse
from .models import Subject, Curriculum, Strand, Substrand, Lesson


class CurriculumModelsTestCase(TestCase):
    def setUp(self):
        self.mathematics = Subject.objects.create(name="Mathematics")
        self.curriculum = Curriculum.objects.create(
            grade="B4", subject=self.mathematics
        )
        self.strand = Strand.objects.create(
            number=1, curriculum=self.curriculum, name="Numbers"
        )
        self.substrand = Substrand.objects.create(
            number=1, strand=self.strand, name="Whole Numbers"
        )
        self.lesson = Lesson.objects.create(
            substrand=self.substrand,
            number=1,
            topic="Introduction to Whole Numbers",
            content="This lesson covers the basics of whole numbers.",
        )

    def test_lesson_slug(self):
        # expected_slug = <strand_number>-<substrand_number>-<lesson_number>-<lesson_topic>
        expected_slug = "1-1-1-introduction-to-whole-numbers"
        self.assertEqual(self.lesson.slug, expected_slug)

    
    def test_lesson_url_is_constructed(self):
        expected_url = reverse(
            "api:curriculums-lesson",
            kwargs={
                "curriculum": self.strand.curriculum.id,
                "lesson": self.lesson.slug,
            },
        )
        self.assertEqual(self.lesson.url, expected_url)
