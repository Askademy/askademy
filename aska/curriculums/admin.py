from django.contrib import admin
from .models import ContentStandard, Grade, LearningIndicator, Subject, Curriculum, Strand, Substrand, Lesson

class CurriculumInline(admin.StackedInline):
        model = Curriculum
        extra = 0

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    inlines = [CurriculumInline]
    list_display = ["name", "number_of_subjects"]
    search_fields = ["code", "name"]

    @admin.display(description="subjects")
    def number_of_subjects(self, obj):
        return obj.curriculums.count()
    

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
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
    autocomplete_fields = ["subject"]

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
    autocomplete_fields = ["subject", "curriculums"]
    search_fields = ["name"]
    list_filter = ["curriculums__grade", "curriculums__subject"]
    list_display = ["name", "number_of_substrands"]

    @admin.display(description="substrands")
    def number_of_substrands(self, obj):
        return obj.substrands.count()


@admin.register(Substrand)
class SubstrandAdmin(admin.ModelAdmin):
    class ContentStandardInline(admin.StackedInline):
        def get_formset(self, request, obj=None, **kwargs):
            formset = super().get_formset(request, obj, **kwargs)
            if obj:  # obj is the Substrand instance
                formset.form.base_fields['curriculum'].queryset = obj.curriculums.all()
            return formset
        
        model = ContentStandard
        extra = 1


    list_display = ["name", "strand_name"]
    search_fields = ["name"]
    autocomplete_fields = ["strand", "curriculums"]
    list_filter = ["curriculums__grade", "curriculums__subject"]
    inlines = [ContentStandardInline]

    @admin.display(description="strand")
    def strand_name(self, obj):
        return obj.strand.name
    

@admin.register(ContentStandard)
class ContentStandardAdmin(admin.ModelAdmin):
    class IndicatorInline(admin.StackedInline):
        model = LearningIndicator

    inlines = [IndicatorInline]
    search_fields = ["curriculum", "substrand"]
    autocomplete_fields = ["curriculum", "substrand"]


@admin.register(LearningIndicator)
class LearningIndicatorAdmin(admin.ModelAdmin):
    autocomplete_fields = ["standard"]
    search_fields = ["standard"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["topic", "curriculum", "annotation"]
    list_display_links = ["topic"]

    @admin.display()
    def curriculum(self, instance):
        return "%s %s" % (instance.grade, instance.subject)

