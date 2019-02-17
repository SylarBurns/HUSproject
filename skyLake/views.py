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
from django.db.models import Q
from django.utils import timezone
import datetime
from datetime import timedelta
class skyLakeListView(BaseListView):
    template_name = 'skyLake/boardList.html'
    def get_context_data(self, **kwargs):
        context = super(skyLakeListView, self).get_context_data(**kwargs)
        context['skyLakeTopThree']= Post.objects.filter(boardNum=2).filter(pubDate__gte=(datetime.date.today()-timedelta(days=7))).order_by('-hitCount')[:3]
        return context
    def get_queryset(self):
        query = self.request.GET.get("q")
        filter = self.request.GET.get("filter")
        queryset = Post.objects.filter(boardNum__exact=2).order_by('-pk')
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
        post.writer = self.request.user.nickName
        post.save()
        postRelation= PostRelation(post=post, user=self.request.user, isWriter=True, annonimity=True, annoName="익명")
        postRelation.save()
        return redirect('skyLake:skyLakeDetail', pk=post.pk)


class skyLakeUpdateView(UpdateView):
    template_name = 'skyLake/boardCreate.html'
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)