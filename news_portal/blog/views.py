from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    """ Представление всех постов в виде списка. """
    model = Post
    ordering = 'date_time'
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    """ Представление отдельного поста. """
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
