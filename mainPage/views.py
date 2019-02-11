from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import(
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.urls import reverse
from django.core import serializers
from heart.models import Post, User, Comment
from django.http import HttpResponse
import json
class mainPageView(TemplateView):
    template_name='mainPage/mainPageTemplate.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range']=[1,2,3,4]
        postSet= Post.objects.all()
        context['potatoFieldTopFour'] = postSet.filter(boardNum=1).order_by('hitCount')[:4]
        context['skyLakeTopThree']= postSet.filter(boardNum=2).order_by('hitCount')[:3]
        context['bambooTopFour']= postSet.filter(boardNum=3).order_by('hitCount')[:4]
        context['runwayTopThree']= postSet.filter(boardNum=4).order_by('hitCount')[:3]  
        try:
            user = self.request.user
            newCommentDic = {}
            alarmDic = {}
            
            #내 게시글의 새 댓글 저장
            q_mypost = user.post_relation.filter(isWriter=True)  
            for p_relation in q_mypost:
                for comment in p_relation.post.comments.all():
                    if comment.noticeChecked == False and user.studentId != comment.getWriterStudentId():
                        newCommentDic[comment] = "게시글"
            #내 댓글의 새 대댓글 저장
            q_mycomment = user.com_relation.filter(isWriter=True)
            for c_relation in q_mycomment:
                for comment in c_relation.comment.subComments.all():
                    if comment.noticeChecked == False and user.studentId != comment.getWriterStudentId():
                        newCommentDic[comment] = "댓글"
            
            #publish date 기준으로 정렬 , sorted -> list 반환
            newCommentList = sorted( newCommentDic.items(), key = lambda dic: dic[0].pubDate, reverse=True)
            for comment in newCommentList:
                if comment[0].getWriterRelation().annonimity:
                    s = "\'{0}\'님이 회원님의 {1}에 댓글을 달았습니다".format(comment[0].getWriterRelation().annoName, comment[1])
                else:
                    s = "\'{0}\'님이 회원님의 {1}에 댓글을 달았습니다".format(comment[0].getWriter().nickName, comment[1])
                alarmDic[s] = comment[0].pk
            
            context['alarmDic'] = alarmDic
        except:
            pass
        return context


class basePageView(TemplateView):
    template_name='mainpage/basePage.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['range']=[1,2,3,4]
        context['ten']=[1,2,3,4,5,6,7,8,9,10]
        return context

def deleteNotice(request):
    _pk = request.POST.get('pk')
    comment = Comment.objects.get(pk=_pk)
    comment.noticeChecked = True
    comment.save()
    context={'one':1}
    return HttpResponse(json.dumps(context),content_type="application/json")

def deleteAll(request):
    
    user = request.user
    newCommentList = []         
    #내 게시글의 새 댓글 저장
    q_mypost = user.post_relation.filter(isWriter=True)  
    for p_relation in q_mypost:
        for comment in p_relation.post.comments.all():
            if comment.noticeChecked == False and user.studentId != comment.getWriterStudentId():
                newCommentList.append(comment)
    #내 댓글의 새 대댓글 저장
    q_mycomment = user.com_relation.filter(isWriter=True)
    for c_relation in q_mycomment:
        for comment in c_relation.comment.subComments.all():
            if comment.noticeChecked == False and user.studentId != comment.getWriterStudentId():
                newCommentList.append(comment)
    
    for comment in newCommentList:
        comment.noticeChecked = True
        comment.save()

    context={'one':1}
    return HttpResponse(json.dumps(context),content_type="application/json")

    