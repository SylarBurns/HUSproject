from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    FormView,
    TemplateView
)
from django.urls import reverse
from django.utils import timezone
from .forms import (
    lostAndFoundPostModelForm,
    lostAndFoundPostDeleteForm
)
from heart.models import (
    Post,
    PostRelation,
    User
)

class listView(ListView):
    template_name = 'lostAndFound/list.html'

    def get_context_data(self, **kwargs):
        context = super(listView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        # self.request.GET.get('boardType','')을 통해서 url 쿼리스트링 ?boardType=Lost 의 값을 가져온다. (list.html)
        # 없는 경우 공백을 리턴한다.
        boardType = self.request.GET.get('boardType','')
        #itemType = self.request.GET.get('itemType','')
        queryset = Post.objects.filter(boardNum__exact=6,exist=True).order_by('-pk')

        if boardType == 'Lost':
            return queryset.filter(LFboardType__exact='Lost')
        elif boardType == 'Found':
            return queryset.filter(LFboardType__exact='Found')
        else :
            return queryset
        # lost-idcard 눌렀을 때, idcard만 눌렀을 때 논리 짜야함
        # 지금은 그냥 따로따로임 idcard누르면 idcard 전체 나옴
        """
        elif itemType == 'idcard':
            return queryset.filter(LFitemType__exact='idcard')
        elif itemType == 'electronic':
            return queryset.filter(LFitemType__exact='electronic')
        elif itemType == 'cash':
            return queryset.filter(LFitemType__exact='cash')
        elif itemType == 'etc':
            return queryset.filter(LFitemType__exact='etc')
        """


class detailView(DetailView):
    template_name = 'lostAndFound/detail.html'
    
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)


class createView(CreateView):
    model = Post
    form_class = lostAndFoundPostModelForm
    template_name = 'lostAndFound/create.html'

    def form_valid(self,form):
        post = form.save(commit=False)
        post.boardNum = 6
        # 조회수는 어떻게 넣어줘야하지?
        post.pubDate = timezone.now()
        if post.LFboardType == 'Lost':
            post.status='Lost'
        else :
            post.status='Found'      
        post.save()
        postRelation = PostRelation(post=post, user=User.objects.get(pk=1), isWriter=True)
        postRelation.save()
        return redirect('lostAndFound:detail', pk=post.pk)



class updateView(UpdateView):
    model = Post
    form_class = lostAndFoundPostModelForm
    template_name = 'lostAndFound/update.html'

    """
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)
    """
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.pub_date = timezone.now()
        if post.LFboardType == 'Lost':
            post.status='Lost'
        else :
            post.status='Found'
        post.save()
        return redirect('lostAndFound:detail', pk=post.pk)    


def delete(request, pk):
    context = {'pk': pk }
    return render(request, 'lostAndFound/delete.html', context)

def deleteConfirm(request, pk):
    post=Post.objects.get(pk=pk)
    post.exist=False
    post.save()
    return redirect('lostAndFound:list')