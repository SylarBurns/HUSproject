from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import(
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .forms import marketModelForm
from heart.views import (    
    BaseListView,
    BaseDetailView
)
from heart.models import Post, PostRelation, User
class marketCreateView(CreateView):
    model=Post
    template_name = 'market/marketCreate.html'
    form_class = marketModelForm
    def form_valid(self, form):
        post = form.save(commit=False)
        post.boardNum = 5
        post.pubDate = timezone.now()
        post.save()
        postRelation= PostRelation(post=post, user=self.request.user, isWriter=True)
        postRelation.save()
        return redirect('market:marketDetail', pk=post.pk)

class marketListView(BaseListView):
    template_name = 'market/marketList.html'
    def get_context_data(self, **kwargs):
        context = super(marketListView, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Post.objects.all().filter(boardNum__exact=5).order_by('-pk')


class marketDetailView(BaseDetailView):
    template_name = 'market/marketDetail.html'

# class TextUpdateView(UpdateView):
#     template_name = 'market/marketCreate.html'
#     form_class = TextModelForm
#     queryset = Post.objects.all()

#     def get_object(self):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Text, id=id_)

#     def form_valid(self, form):
#         print(form.cleaned_data)
#         return super().form_valid(form)

# class TextDeleteView(DeleteView):
#     template_name = 'market/marketDelete.html'

#     def get_object(self):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Text, id=id_)

#     def get_success_url(self):
#         return reverse('market:text-list')

