from django.contrib import admin

from .models import ContentStandard, Grade, LearningIndicator, Subject, Curriculum, Strand, Substrand, Lesson

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["name", "number_of_subjects"]
    search_fields = ["code", "name"]

    @admin.display(description="subjects")
    def number_of_subjects(self, obj):
        return obj.curriculums.count()
    

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    class CurriculumInline(admin.StackedInline):
        model = Curriculum
        extra = 0

    inlines = [CurriculumInline]
    search_fields = ["name"]
    list_filter = ["curriculums__grade__name"]
    list_display = ["name", "grade"]
    
    @admin.display()
    def grade(self, obj):
        return [x.grade.code for x in obj.curriculums.all()]
    

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_filter = ["grade__name", "subject__name"]
    list_display = ["subject", "grade_code", "number_of_strands", "number_of_substrands"]
    search_fields = ["subject__name", "grade__name"]

    @admin.display(description="grade")
    def grade_code(self, obj):
        return obj.grade.code
    
    @admin.display(description="strands")
    def number_of_strands(self, obj):
        return obj.strands.count()
    
    @admin.display(description="substrands")
    def number_of_substrands(self, obj):
        return obj.substrands.count()


@admin.register(Strand)
class StrandAdmin(admin.ModelAdmin):
    class SubstrandInline(admin.StackedInline):
        extra = 1
        model = Substrand
    
    inlines = [SubstrandInline]
    search_fields = ["name"]
    list_filter = ["curriculums__grade", "curriculums__subject"]
    list_display = ["name", "number_of_substrands"]

    @admin.display(description="substrands")
    def number_of_substrands(self, obj):
        return obj.substrands.count()


@admin.register(Substrand)
class SubstrandAdmin(admin.ModelAdmin):
    list_display = ["name", "strand_name"]
    search_fields = ["name"]
    list_filter = ["curriculums__grade", "curriculums__subject"]

    @admin.display(description="strand")
    def strand_name(self, obj):
        return obj.strand.name


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["topic", "curriculum", "annotation"]
    list_display_links = ["topic"]

    @admin.display()
    def curriculum(self, instance):
        return "%s %s" % (instance.grade, instance.subject)



admin.site.register([ContentStandard, LearningIndicator])