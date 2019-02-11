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
from heart.models import Post, PostRelation, User, Comment, ComRelation
from .forms import PostModelForm
from django.utils import timezone
from django.db.models import Q


class potatoFieldListView(BaseListView):
    template_name = 'potatoField/boardList.html'
    
    def get_context_data(self, **kwargs):
        context = super(potatoFieldListView, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        query = self.request.GET.get("q")
        filter = self.request.GET.get("filter")
        queryset = Post.objects.filter(boardNum__exact=1).order_by('-pk')
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


class potatoFieldDetailView(BaseDetailView):
    template_name = 'potatoField/boardDetail.html'
    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get("pk")
        post = get_object_or_404(Post, id=id_)
        context = super(potatoFieldDetailView, self).get_context_data(**kwargs)
        context['comment_list']=post.comments.all()
        return context

class potatoFieldCreateView(CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'potatoField/boardCreate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.boardNum = 1
        post.pubDate = timezone.now()
        post.writer = self.request.user.nickName
        post.save()
        postRelation= PostRelation(post=post, user=self.request.user, isWriter=True)
        postRelation.save()
        return redirect('potatoField:potatoFieldDetail', pk=post.pk)


class potatoFieldUpdateView(UpdateView):
    template_name = 'potatoField/boardCreate.html'
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Post, id=id_)