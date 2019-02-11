#Mypage - views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from heart.models import User, Post
from django.utils import timezone
import datetime
from .forms import UserUpdateForm

class myPostView(generic.ListView):
    template_name = 'mypage/myPost.html'
    model = User
    context_object_name = 'latest_post_list'
    paginate_by = 3

    def get_queryset(self):
        #Return the last ten published posts.
        user = self.request.user
        queryset = user.post_relation.filter(isWriter=True).order_by('-pk')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

class myCommentView(generic.ListView):
    template_name = 'mypage/myComment.html'
    model = User
    context_object_name = 'latest_comment_list'
    paginate_by = 3
    def get_queryset(self):
        #Return the last ten published posts.
        user = self.request.user
        queryset = user.com_relation.filter(isWriter=True).order_by('-pk')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
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