#Mypage - views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView, View, UpdateView
from heart.models import User, Post
from django.utils import timezone
import datetime
from .forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
class myPostView(LoginRequiredMixin, ListView):
    template_name = 'mypage/myPost.html'
    model = User
    context_object_name = 'latest_post_list'
    login_url = 'heart:loginRequired'
    def get_queryset(self):
        #Return the last ten published posts.
        user = self.request.user
        queryset = user.post_relation.filter(isWriter=True).order_by('-pk')
        return queryset

class myCommentView(LoginRequiredMixin, ListView):
    template_name = 'mypage/myComment.html'
    model = User
    context_object_name = 'latest_comment_list'
    login_url = 'heart:loginRequired'
    def get_queryset(self):
        #Return the last ten published posts.
        user = self.request.user
        queryset = user.com_relation.filter(isWriter=True).order_by('-pk')
        return queryset

class myDataView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage/myData.html'
    login_url = 'heart:loginRequired'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class myReportView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage/myReport.html'
    login_url = 'heart:loginRequired'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post_list = []
        for relation in user.post_relation.filter(isReporter=True).order_by('-pk'):
            post_list.append(relation.post)
        context['my_post_list'] = post_list
        com_list = []
        for relation in user.com_relation.filter(isReporter=True).order_by('-pk'):
             com_list.append(relation.comment)
        context['my_comment_list'] = com_list
            
        return context


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class =  UserUpdateForm
    template_name = 'mypage/updateUser.html'
    login_url = 'heart:loginRequired'
    context_object_name = 'user'
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(User, id=id_)
    def form_valid(self, UserUpdateForm):
        user = UserUpdateForm.save(commit=False)
        user.nickName = UserUpdateForm.cleaned_data['nickName']
        user.phone = UserUpdateForm.cleaned_data['phone']
        user.icon = UserUpdateForm.cleaned_data['icon']
        user.save()
        return redirect('mypage:myData', pk = self.request.user.pk )
    

