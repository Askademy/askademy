from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from curriculums.models import Grade, Curriculum, Strand
from curriculums.serializers import StrandSerializer

class CurriculumsView(generic.TemplateView):
    template_name = "web/curriculums.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grades = Grade.objects.all()
        context["grades"] =  grades
        return context

class LessonView(generic.TemplateView):
    template_name = "web/lesson.html"

    def get_serialized_data(self, queryset, many=True):
        context = {"request": self.request}
        serializer = StrandSerializer(queryset,context=context, many=many)
        return serializer.data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Strand.objects.filter(substrands__curriculum__id=kwargs["curriculum"]).distinct()
        strands = self.get_serialized_data(queryset)
        context["strands"] = strands
        
        return context
