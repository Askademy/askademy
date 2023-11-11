from django.db import models


class Grade(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Grade name")
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Subject name")
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Curriculum(models.Model):
    annotation = models.CharField(max_length=100, unique=True, editable=False)
    grade = models.ForeignKey(Grade, related_name="curriculums", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="curriculums", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.annotation = f"{self.subject.code}:{self.grade.code}"
        super().save()

    def __str__(self):
        return f"{self.grade.code} {self.subject.name}"
    
    class Meta:
        ordering = ["subject__name", "grade"]


class Strand(models.Model):
    annotation = models.CharField(max_length=100, unique=True, editable=False)
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100, verbose_name="Strand name")
    subject = models.ForeignKey(Subject, related_name="strands", on_delete=models.CASCADE)
    curriculums = models.ManyToManyField(Curriculum, related_name="strands")

    def save(self, *args, **kwargs):
        self.annotation = f"{self.subject.code}:{self.number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.annotation} {self.name}"


class Substrand(models.Model):
    annotation = models.CharField(max_length=100, unique=True, editable=False)
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)
    strand = models.ForeignKey(Strand, related_name="substrands", on_delete=models.CASCADE)
    curriculums = models.ManyToManyField(Curriculum, related_name="substrands")

    def save(self, *args, **kwargs):
        self.annotation = f"{self.strand.annotation}.{self.number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.annotation} {self.name}"


class ContentStandard(models.Model):
    annotation = models.CharField(max_length=100, unique=True, editable=False)
    number = models.PositiveSmallIntegerField()
    description = models.TextField()
    curriculum = models.ForeignKey(Curriculum, related_name="content_standards", on_delete=models.CASCADE)
    substrand = models.ForeignKey(Substrand, related_name="content_standards", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        subject = self.curriculum.subject.code
        grade = self.curriculum.grade.code
        strand = self.substrand.strand.number
        substrand = self.substrand.number
        self.annotation = f"{subject}:{grade}.{strand}.{substrand}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description


class LearningIndicator(models.Model):
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=1000)
    standard = models.ForeignKey(ContentStandard, related_name="indicators", verbose_name="Content standard", on_delete=models.CASCADE)
    annotation = models.CharField(max_length=100, unique=True, editable=False)

    def save(self, *args, **kwargs):
        standard_annotation = self.standard.annotation
        self.annotation = f"{standard_annotation}.{self.number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Lesson(models.Model):
    annotation = models.CharField(max_length=100, unique=True, editable=False)
    number = models.PositiveSmallIntegerField()
    indicator = models.ForeignKey(LearningIndicator, related_name="lessons", on_delete=models.CASCADE)
    topic = models.CharField(max_length=1024)
    content = models.TextField()

    def __str__(self):
        return f"{self.substrand.id} {self.topic}"

    def save(self, *args, **kwargs):
        self.annotation = f"{self.indicator.annotation}.{self.number}"
        super().save(*args, **kwargs)

