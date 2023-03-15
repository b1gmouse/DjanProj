from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin


class NewsList(ListView):
    model = Post
    ordering = 'topic'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'article'


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'new_article.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = 2
        return super().form_valid(form)


class PostCreateNew(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = 1
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('new_list')


class PostSearch(ListView):
    model = Post
    template_name = 'new_search.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDeleteArticle(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete_article.html'
    success_url = reverse_lazy('new_list')


class PostUpdateArticle(LoginRequiredMixin, UpdateView):
    permission_required = ('news.edit_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
