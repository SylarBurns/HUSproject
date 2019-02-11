# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import(
    View,
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.urls import reverse
from heart.models import Post, PostRelation, User
from heart.views import (    
    BaseListView,
    BaseDetailView
)
from .forms import PostModelForm
from django.utils import timezone
from django.core import exceptions
from django.db.models import Q
class bambooListView(BaseListView):
    template_name = 'bamboo/boardList.html'
    def get_context_data(self, **kwargs):
        context = super(bambooListView, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        query = self.request.GET.get("q")
        filter = self.request.GET.get("filter")
        queryset = Post.objects.filter(boardNum__exact=3).order_by('-pk')
        if query:
            if filter == "nofilter":
                return queryset.filter(Q(title__icontains=query) or Q(postEditor__icontains=query) or Q(writer__icontains=query))
            elif filter == "writer":
                return queryset.filter(writer__icontains=query)
            elif filter == "title":
                return queryset.filter(title__icontains=query)
            else :
                return queryset.filter(Q(title__icontains=query) or Q(postEditor__icontains=query))
        else:
            return queryset

class bambooDetailView(BaseDetailView):
    template_name = 'bamboo/boardDetail.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk)
        context['likeCount']=post.post_relation.filter(like=True).count()
        context['dislikeCount']=post.post_relation.filter(dislike=True).count()
        return context

class bambooCreateView(CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'bamboo/boardCreate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.boardNum = 3
        post.pubDate = timezone.now()
        post.save()
        postRelation= PostRelation(post=post, user=User.objects.get(pk=self.request.user.pk), isWriter=True, annonimity=True, annoName="익명")
        postRelation.save()
        return redirect('bamboo:bambooDetail', pk=post.pk)


class bambooUpdateView(UpdateView):
    template_name = 'bamboo/boardCreate.html'
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)
