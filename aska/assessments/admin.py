from django.contrib import admin


from .models import Question, MultipleChoiceAnswer, ShortAnswer, TrueFalseAnswer

admin.site.register([Question, MultipleChoiceAnswer, ShortAnswer])
