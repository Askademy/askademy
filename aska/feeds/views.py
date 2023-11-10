from django.shortcuts import render, redirect
from django.urls import reverse_lazy


from django.views import View, generic
from feeds.models import Post
from .forms import PostForm


class PostCreateView(generic.CreateView):
    template_name = "posts/create_post.html"
    model = Post
    fields = ("content", "image", )
    success_url = reverse_lazy('web:home') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostDetailView(generic.DetailView):
    template_name = "posts/post_detail.html"
    queryset = Post.objects.all()


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
