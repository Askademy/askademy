from django.shortcuts import render, redirect
from django.views import View
from records.models import Post
from .forms import PostForm

class CreatePostView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'your_template.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_success')
        return render(request, 'your_template.html', {'form': form})
