from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .choices import GRADE


class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Curriculum(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True, editable=False)
    grade = models.CharField(max_length=10, choices=GRADE)
    subject = models.ForeignKey(Subject, related_name="curriculums", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.id = f"{self.grade}-{self.subject.name}".lower().replace(" ", "-").replace("|", "_")
        super().save(*args, **kwargs)

    @property
    def strands_url(self):
        """
        Read-only property that returns the URL for the detail view of the
        curriculum instance.
        """
        return reverse("api:curriculums-detail", kwargs={"curriculum": self.pk})

    def __str__(self):
        return self.id


class Strand(models.Model):
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name.lower()


class Substrand(models.Model):
    id = models.CharField(editable=False, max_length=20, primary_key=True)
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, related_name="substrands", on_delete=models.CASCADE)
    strand = models.ForeignKey(Strand, related_name="substrands", on_delete=models.CASCADE)
    curriculum = models.ManyToManyField(Curriculum, related_name="substrands")


    def save(self, *args, **kwargs):
        subject_id = self.subject.id
        curriculum_grades = "-".join([curriculum.grade for curriculum in self.curriculum])
        self.id = f"S{subject_id}_{curriculum_grades}.{self.strand.number}.{self.number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    id = models.CharField(editable=False, max_length=20, primary_key=True)
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE, editable=False)
    grade = models.CharField(max_length=10, choices=GRADE)
    # strand = models.ForeignKey(Strand, related_name="strands", on_delete=models.CASCADE, editable=False)
    substrand = models.ForeignKey(Substrand, related_name="lessons", on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    topic = models.CharField(max_length=1024)
    content = models.TextField()
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return f"{self.substrand.id} {self.topic}"

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to set the subject, 
        grade, strand, and slug fields based on related SubStrand,
        and then save the instance to the database.
        """
        strand_number = self.substrand.strand.number
        self.id = f"{self.grade}.{strand_number}.{self.substrand.number}"
        self.id = f"{self.substrand.id}.{self.number}"
        self.subject = self.strand.curriculum.objects.first().subject
        self.slug = slugify(f"{self.strand.number}-{self.substrand.number}-{self.number}-{self.topic}")
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ["number", "subject", "grade"]
