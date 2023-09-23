from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic


from web import dummy


class CurriculumsView(generic.TemplateView):
    template_name = "web/curriculums.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["curriculums"] = dummy.curriculums
        context["grades"] = dummy.grades
        return context


class LessonView(generic.TemplateView):
    template_name = "web/lesson.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["strands"] = dummy.strands

        # Get the topic ID from the URL parameter
        topic_id = self.request.GET.get("topic_id")

        # Loop through all topics to find the selected one
        for strand in context["strands"]:
            for substrand in strand["substrands"]:
                for topic in substrand["topics"]:
                    if topic["id"] == topic_id:
                        context["topic"] = topic
                        break

        return context
