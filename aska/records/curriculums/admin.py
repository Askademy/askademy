from django.contrib import admin

from .models import Subject, Curriculum, Strand, Substrand, Lesson


class CurriculumInline(admin.StackedInline):
    model = Curriculum
    extra = 1


class SubstrandInline(admin.StackedInline):
    extra = 1
    model = Substrand

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [CurriculumInline]
    list_display = ["name", "grade"]

    @admin.display()
    def grade(self, obj):
        return [x.grade for x in obj.curriculums.all()]


@admin.register(Strand)
class StrandAdmin(admin.ModelAdmin):
    list_display = ["name",]
    search_fields = ["name"]
    inlines = [SubstrandInline]



@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["topic", "curriculum", "slug"]
    list_display_links = ["slug"]

    @admin.display()
    def curriculum(self, instance):
        return "%s %s" % (instance.grade, instance.subject)

admin.site.register([Curriculum])