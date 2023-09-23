from django.db import models

from records.curriculums.models import Lesson, Subject
from .choices import QUESTION_TYPE


class Question(models.Model):
    question_type = models.CharField(max_length=100, choices=QUESTION_TYPE)
    lesson = models.ForeignKey(
        Lesson, related_name="questions", on_delete=models.CASCADE
    )
    text = models.TextField()


class ShortAnswer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class MultipleChoiceAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class TrueFalseAnswer(models.OneToOneField):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    text = models.BooleanField(default=True)
