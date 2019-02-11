# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
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
from django.db.models import Q
import json
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
class BaseListView(ListView):
    paginate_by = 3
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
        context['comment_list']=post.comments.all()
        return context



#좋아요 싫어요 기능 추가
# template에서는 다음 코드를 삽입하면 된다.
# <div class="buttons">
#     <input type="button" class="like" name="{{ object.pk }}" value="좋아요">
#     <input type="button" class="dislike" name="{{ object.pk }}" value="싫어요">
#     <p id="likecount">{{likeCount}}</p>
#     <p id="dislikecount">{{dislikeCount}}</p>
#     <button>신고</button>
# </div>

def postLike(request):#좋아요 기능
    pk = request.POST.get('pk', None)
    post = Post.objects.get(pk=pk)
    user = request.user
    try : 
        relation = PostRelation.objects.filter(Q(user=user), Q(post=post)).get()
        #PostRelation instance 중에서 post와 user간에 존재하는 instance를 찾아본다.
        if relation.like: #relation의 like가 true이면 false로, like가 false라면 like를 true, dislike를 false로 만든다.
            relation.like = False
        else:
            relation.like = True
            relation.dislike = False
        relation.save()#relation을 저장하면 post와 user간의 관계가 성립된다. 
    except exceptions.ObjectDoesNotExist : #post와 user 사이에 postRelation이 없으면 하나 만들어서 저장한다. 
        post = Post.objects.get(pk=pk)#pk로 post object를 가져온다.
        relation = PostRelation(post=post, user=User.objects.get(pk=request.user.pk), like=True)
        relation.save()
    context={'like_count':post.post_relation.filter(like=True).count(),
             'dislike_count':post.post_relation.filter(dislike=True).count()}
    return HttpResponse(json.dumps(context),content_type="application/json")

def commentLike(request):#좋아요 기능
    pk = request.POST.get('pk', None)
    comment = Comment.objects.get(pk=pk)
    user = request.user
    try : 
        relation = ComRelation.objects.filter(Q(user=user), Q(comment=comment)).get()
        #PostRelation instance 중에서 post와 user간에 존재하는 instance를 찾아본다.
        if relation.like: #relation의 like가 true이면 false로, like가 false라면 like를 true, dislike를 false로 만든다.
            relation.like = False
        else:
            relation.like = True
            relation.dislike = False
        relation.save()#relation을 저장하면 post와 user간의 관계가 성립된다. 
    except exceptions.ObjectDoesNotExist : #post와 user 사이에 postRelation이 없으면 하나 만들어서 저장한다. 
        relation = ComRelation(comment=comment, user=user, like=True)
        relation.save()
    context={'like_count':comment.likeCount(),
             'dislike_count':comment.dislikeCount()}
    return HttpResponse(json.dumps(context),content_type="application/json")

def postDislike(request):#싫어요 기능
    pk = request.POST.get('pk', None)
    post = Post.objects.get(pk=pk)
    user = request.user
    try : 
        relation = PostRelation.objects.filter(Q(user=user), Q(post=post)).get()
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
        
    context={'like_count':post.post_relation.filter(like=True).count(),
             'dislike_count':post.post_relation.filter(dislike=True).count()}
    return HttpResponse(json.dumps(context),content_type="application/json")

def commentDislike(request):#싫어요 기능
    pk = request.POST.get('pk', None)
    comment = Comment.objects.get(pk=pk)
    user = request.user
    try : 
        relation = ComRelation.objects.filter(Q(user=user), Q(comment=comment)).get()
        if relation.dislike:
            relation.dislike=False
        else:
            relation.like=False
            relation.dislike=True
        relation.save()
    except exceptions.ObjectDoesNotExist :
        relation = ComRelation(comment=comment, user=user, dislike=True)
        relation.save()
        
    context={'like_count':comment.likeCount(),
             'dislike_count':comment.dislikeCount()}
    return HttpResponse(json.dumps(context),content_type="application/json")

def commentWrite(request):
    pk = request.POST.get('pk', None)
    annonimity = request.POST.get('annonimity',None)
    post = Post.objects.get(pk=pk)
    user = request.user
    content = request.POST.get('content', None)
    comment = Comment(post = post, content= content)
    comment.save()
    if annonimity == 'True':
        relation = ComRelation(comment=comment, user=user, isWriter=True, annonimity=True, annoName="익명")
    else:
        relation = ComRelation(comment=comment, user=request.user, isWriter=True)
    relation.save()

    if post.boardNum == 4:#만약에 토론게시판이면 댓글의 stance를 사용자의 투표결과로 바꾸어준다.
        postRelation=PostRelation.objects.filter(Q(user=user), Q(post=post)).get()
        voteResult = postRelation.vote
        if voteResult == 0 or voteResult == 1 or voteResult == 2 :
            comment.stance = voteResult
        else: 
            comment.stnace = 2 #투표한 값이 없으면 자동으로 중립으로 저장함.
        comment.save()
    
    context={'nickName':user.nickName, 'content':content,'pk':pk}
    return HttpResponse(json.dumps(context), content_type="application/json")

def subCommentWrite(request):
    pk = request.POST.get('commentPk', None)
    annonimity = request.POST.get('annonimity',None)
    parentComment = Comment.objects.get(pk=pk)
    user = request.user
    content = request.POST.get('subCommentContent', None)
    comment = Comment(belongToComment = parentComment, content= content)
    comment.save()

    if annonimity == 'True':
        relation = ComRelation(comment=comment, user=user, isWriter=True, annonimity=True, annoName="익명")
    else:
        relation = ComRelation(comment=comment, user=request.user, isWriter=True)
    relation.save()

    post = parentComment.post
    if post.boardNum == 4:#만약에 토론게시판이면 댓글의 stance를 사용자의 투표결과로 바꾸어준다.
        postRelation=PostRelation.objects.filter(Q(user=user), Q(post=post)).get()
        voteResult = postRelation.vote
        if voteResult == 0 or voteResult == 1 or voteResult == 2 :
            comment.stance = voteResult
        else: 
            comment.stnace = 2 #투표한 값이 없으면 자동으로 중립으로 저장함.
        comment.save()

    context={'nickName':user.nickName, 'content':content,'pk':pk}
    return HttpResponse(json.dumps(context), content_type="application/json")

def writeReport(request, pk):
    context={'pk':pk, 'url':request.META.get('HTTP_REFERER', '/')}
    return render(request, 'heart/report.html', context)

def sendReport(request):
    url= request.POST['url']
    pk = request.POST['pk']
    post = Post.objects.get(pk=pk)
    user = request.user

    try : 
        relation = PostRelation.objects.filter(Q(user=user), Q(post=post)).get()
        relation.isReporter = True
        relation.save()
    except exceptions.ObjectDoesNotExist :
        relation = PostRelation(post=post, user=user, isReporter=True)
        relation.save()
    post.reportStatus="미확인"
    post.save()
    subject = user.nickName + " reported Post "+ pk + " " +post.title
    message = request.POST['message']
    email = EmailMessage(subject, message, to=['sokon954@gmail.com'])
    email.send()

    return HttpResponseRedirect(url)

def writeCommentReport(request, pk):
    context={'pk':pk, 'url':request.META.get('HTTP_REFERER', '/')}
    return render(request, 'heart/reportComment.html', context)

def sendCommentReport(request):
    url= request.POST['url']
    pk = request.POST['pk']
    comment = Comment.objects.get(pk=pk)
    user = request.user

    try : 
        relation = ComRelation.objects.filter(Q(user=user), Q(comment=comment)).get()
        relation.isReporter = True
        relation.save()
    except exceptions.ObjectDoesNotExist :
        relation = ComRelation(comment=comment, user=user, isReporter=True)
        relation.save()
    comment.reportStatus="미확인"
    comment.save()
    subject = user.nickName + " reported Comment "+ pk + " " + comment.content
    message = request.POST['message']
    email = EmailMessage(subject[:40], message, to=['sokon954@gmail.com'])
    email.send()

    return HttpResponseRedirect(url)

def vote(request):
    stance = request.POST['stance']
    pk =  request.POST['pk']
    post = Post.objects.get(pk=pk)
    user = request.user
    if stance =="찬성":
        voteInfo = 1
    elif stance =="반대":
        voteInfo = 0
    else:
        voteInfo = 2

    try:
        relation = PostRelation.objects.filter(Q(user=user), Q(post=post)).get()
        relation.vote= voteInfo
    except:
        relation =PostRelation(user=user,post=post,vote=voteInfo)
    relation.save()
    context={'stance':stance,
            'pk':pk}
    return HttpResponse(json.dumps(context),content_type="application/json")