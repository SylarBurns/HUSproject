from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import(
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView
)
from heart.views import (    
    BaseListView,
    BaseDetailView
)
from django.urls import reverse
from heart.models import Post, PostRelation, User
from .forms import PostModelForm
from django.utils import timezone

class skyLakeListView(BaseListView):
    template_name = 'skyLake/boardList.html'
    def get_context_data(self, **kwargs):
        context = super(skyLakeListView, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Post.objects.all().filter(boardNum__exact=2).order_by('-pk')


class skyLakeDetailView(BaseDetailView):
    template_name = 'skyLake/boardDetail.html'

class skyLakeCreateView(CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'skyLake/boardCreate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.boardNum = 2
        post.pubDate = timezone.now()
        post.save()
        postRelation= PostRelation(post=post, user=self.request.user, isWriter=True)
        postRelation.save()
        return redirect('skyLake:skyLakeDetail', pk=post.pk)


class skyLakeUpdateView(UpdateView):
    template_name = 'skyLake/boardCreate.html'
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)