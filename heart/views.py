# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import(
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.utils import timezone
from django.core import serializers 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from heart.models import Post, User, PostRelation, Comment, ComRelation
from django.core import exceptions

class BaseListView(ListView):
    paginate_by = 1
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['list']= serializers.serialize("json", Post.objects.all())
    #     return context

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10  # Display only 10 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class BaseDetailView(DetailView):
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



#좋아요 싫어요 기능 추가
# app의 urls.py에 아래 코드와 urls를 추가하고 사용하면 된다.
# from heart.views import postLike, postDislike
# path('<int:pk>/like/', postLike, name="postLike"),
# path('<int:pk>/disLike/', postDislike, name="postDislike"),
# template에서는 다음 코드를 삽입하면 된다.
# <button><a href="{% url '[app 이름]:postLike' pk=object.pk %}">좋아요{{ likeCount }}</a></button>
# <button><a href="{% url 'bamboo:postDislike' pk=object.pk %}">싫어요{{dislikeCount}}</a></button>
# detail view에 다음 함수를 추가 해준다.


def postLike(request, pk):#좋아요 기능 
    try : 
        relation = PostRelation.objects.filter(post_id=pk).filter(user_id=request.user.pk).get()
        #PostRelation instance 중에서 post와 user간에 존재하는 instance를 찾아본다.
        if relation.like : #relation의 like가 true이면 false로, like가 false라면 like를 true, dislike를 false로 만든다.
            relation.like = False
        else:
            relation.like = True
            relation.dislike = False
        relation.save()#relation을 저장하면 post와 user간의 관계가 성립된다. 
    except exceptions.ObjectDoesNotExist : #post와 user 사이에 postRelation이 없으면 하나 만들어서 저장한다. 
        post = Post.objects.get(pk=pk)#pk로 post object를 가져온다.
        relation = PostRelation(post=post, user=User.objects.get(pk=request.user.pk), like=True)
        relation.save()

    return redirect(request.build_absolute_uri()[:-5]) #postLike 함수를 호출한 url로 돌려보낸다. 

def postDislike(request, pk):#싫어요 기능
    try : 
        relation = PostRelation.objects.filter(post_id=pk).filter(user_id=request.user.pk).get()
        if relation.dislike:
            relation.dislike=False
        else:
            relation.like=False
            relation.dislike=True
        relation.save()
    except exceptions.ObjectDoesNotExist :
        post = Post.objects.get(pk=pk)
        relation = PostRelation(post=post, user=User.objects.get(pk=request.user.pk), dislike=True)
        relation.save()
        
    return redirect(request.build_absolute_uri()[:-8])