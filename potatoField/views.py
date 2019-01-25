from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from .forms import PostForm,CommentForm
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


class CreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'potatoField/boardCreate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.boardNum = 1
        post.pubDate = timezone.now()
        post.save()
        postrelation = PostRelation(post=post, user=User.objects.get(pk=1), isWriter=True)
        postrelation.save()
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

class CreateCommentView(generic.CreateView, DetailView):
    model = Comment
    form_class = CommentForm
    template_name = 'potatoField/boardDetail.html'

    def form_valid(self, form, post):
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        comrelation = ComRelation(comment=comment, user=User.objects.get(pk=1), isWriter=True)
        comrelation.save()
        return redirect('detail', pk=post.pk)
    
def createComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            comrelation = ComRelation(comment=comment, user=User.objects.get(pk=1), isWriter=True)
            comrelation.save()
            return redirect('detail', pk=post.pk)
        # else:
        #     form = CommentForm()
        # return render(request, 'potatoField/boardDetail.html', {'form':form})
# Create your views here.
