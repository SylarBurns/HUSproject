from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from .forms import PostForm
from django.core import serializers 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from heart.models import Post, User, PostRelation, Comment, ComRelation
from heart.views import (    
    BaseListView,
    BaseDetailView
)

class IndexView(BaseListView):
    template_name = 'potatoField/boardList.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Post.objects.all().filter(boardNum__exact=1).order_by('-pk')


class DetailView(BaseDetailView):
    template_name = 'potatoField/boardDetail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        content = self.request.GET.get("content")
        if content:
            comment = Comment(content=content)
            comment.post = self.request.post
            comment.save()
            relation =ComRelation(comment=comment, user=self.request.user, isWriter=True)
            relation.save()
        return context

class CreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'potatoField/boardCreate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.boardNum = 1
        post.pubDate = timezone.now()
        # post.writer = self.request.user.nickName
        post.writer = User.objects.get(pk=0)
        post.save()
        return redirect('detail', pk=post.pk)

class UpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'potatoField/boardUpdate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.pub_date = timezone.now()
        post.save()
        return redirect('detail', pk=post.pk)

# class CreateCommentView(generic.CreateView, DetailView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'potatoField/boardDetail.html'

#     def form_valid(self, form, post):
#         comment = form.save(commit=False)
#         comment.post = post
#         # comment.writer = self.request.user.nickName
#         comment.writer = "승빈"
#         comment.save()
#         return redirect('detail', pk=post.pk)
    
# def createComment(request, pk):
    # post = get_object_or_404(Post, pk=pk)
    # if request.method == "POST":
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.post = post
    #         comment.writer = "승빈"
    #         comment.save()
    #         return redirect('detail', pk=post.pk)
    #     else:
    #         form = CommentForm()
    #     return render(request, 'potatoField/boardDetail.html', {'form':form})
    

