#Mypage - views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from heart.models import User, Post
from django.utils import timezone
import datetime
from .forms import UserUpdateForm
from django.http import HttpResponse
class myPostView(generic.TemplateView):
    template_name = 'mypage/myPost.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post_dic = {}
        now = timezone.now()
        for relation in user.post_relation.all().order_by('-pk'):
            if relation.isWriter:
                diff = now - relation.post.pubDate
                if diff.days is 0:
                    in24 = True
                else:
                    in24 = False
                post_dic[relation.post] = in24
        context['my_post_dic'] = post_dic
        return context



class myCommentView(generic.TemplateView):
    template_name = 'mypage/myComment.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        com_dic = {}
        now = timezone.now()
        for relation in user.com_relation.all().order_by('-pk'):
            if relation.isWriter:
                diff = now - relation.comment.pubDate
                if diff.days is 0:
                    in24 = True
                else:
                    in24 = False
                com_dic[relation.comment] = in24
        context['my_com_dic'] = com_dic
        return context


class myDataView(generic.TemplateView):
    template_name = 'mypage/myData.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class myReportView(generic.TemplateView):
    template_name = 'mypage/myReport.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post_list = []
        for relation in user.post_relation.all().order_by('-pk'):
            if relation.isReporter:
                post_list.append(relation.post)
        context['my_post_list'] = post_list
        com_list = []
        for relation in user.com_relation.all().order_by('-pk'):
            if relation.isReporter:
                com_list.append(relation.comment)
        context['my_comment_list'] = com_list
            
        return context


class myReportPopupView(generic.TemplateView):
    template_name = 'mypage/myReportPopup.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post_list = []
        for relation in user.post_relation.all().order_by('-pk'):
            if relation.isReporter:
                post_list.append(relation.post)
        context['my_post_list'] = post_list
        com_list = []
        for relation in user.com_relation.all().order_by('-pk'):
            if relation.isReporter:
                com_list.append(relation.comment)
        context['my_comment_list'] = com_list
            
        return context

class UpdateUserView(generic.View):
    model = User
    form_class =  UserUpdateForm
    template_name = 'mypage/updateUser.html'
    def get(self, request):   # 처음엔 이곳으로 들어감
        form = UserUpdateForm()
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = UserUpdateForm(request.POST)
        if request.POST.get('cancel') == "cancel":
            return redirect('mypage:myData')
        if form.is_valid():
            user = self.request.user
            user.nickName = form.cleaned_data['nickName']
            user.phone = form.cleaned_data['phone']
            user.save()
            return redirect('mypage:myData')
        else:
            return render(request, self.template_name, {'form':form})


 

