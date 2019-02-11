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
from django.utils import timezone
import datetime
from datetime import timedelta
class runwayListView(BaseListView):
    template_name = 'runway/boardList.html'
    def get_context_data(self, **kwargs):
        context = super(runwayListView, self).get_context_data(**kwargs)
        context['runwayTopThree']= Post.objects.filter(boardNum=4).filter(pubDate__gte=(datetime.date.today()-timedelta(days=7))).order_by('-hitCount')[:3]
        return context
    def get_queryset(self):
        query = self.request.GET.get("q")
        filter = self.request.GET.get("filter")
        queryset = Post.objects.filter(boardNum__exact=4).order_by('-pk')
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

class runwayDetailView(BaseDetailView):
    template_name = 'runway/boardDetail.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk)
        user = self.request.user

        ###투표결과 저장
        relationSet = post.post_relation.all()
        context['forCount']=relationSet.filter(vote=1).count()
        context['againstCount']=relationSet.filter(vote=0).count()
        context['neutralCount']=relationSet.filter(vote=2).count()

        try : 
            relation = PostRelation.objects.filter(Q(user=user), Q(post=post)).get()
            #PostRelation instance 중에서 post와 user간에 존재하는 instance를 찾아본다.
            context['stance'] = relation.vote
        except exceptions.ObjectDoesNotExist : #post와 user 사이에 postRelation이 없으면
            context['stance'] = 3
            # stance의 값은 0:반대 1:찬성 2:중립 3:미투표
        return context

class runwayCreateView(CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'runway/boardCreate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.boardNum = 4
        post.pubDate = timezone.now()
        post.writer = self.request.user.nickName
        post.save()
        if self.request.POST['annonimity']=='annonimity':
            postRelation= PostRelation(post=post, user=User.objects.get(pk=self.request.user.pk), isWriter=True, annonimity=True, annoName="익명")
        else:
            postRelation= PostRelation(post=post, user=User.objects.get(pk=self.request.user.pk), isWriter=True,)
        postRelation.save()
        return redirect('runway:runwayDetail', pk=post.pk)


class runwayUpdateView(UpdateView):
    template_name = 'runway/boardCreate.html'
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)

class chartTestView(TemplateView):
    template_name='runway/chartTest.html'