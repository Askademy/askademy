from django import forms
from feeds.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

    def clean_content(self):
        content = self.cleaned_data.get('content')

        if (content < 5) or len(content.split(" "))<2:
            raise forms.ValidationError("Content cannot be empty or less than 2 words.")

        return content
