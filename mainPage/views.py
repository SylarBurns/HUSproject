from django.shortcuts import render, get_object_or_404
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
from heart.models import Post
from django.utils import timezone
import datetime
from datetime import timedelta
from django.db.models import Q
class mainPageView(TemplateView):
    template_name='mainPage/mainPageTemplate.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range']=[1,2,3,4]
        postSet= Post.objects.filter(pubDate__gte=(datetime.date.today()-timedelta(days=7))).all()
        now = timezone.now()
        context['potatoFieldTopFour'] = postSet.filter(boardNum=1).order_by('-hitCount')[:4]
        context['skyLakeTopThree']= postSet.filter(boardNum=2).order_by('-hitCount')[:3]
        context['bambooTopFour']= postSet.filter(boardNum=3).order_by('-hitCount')[:4]
        context['runwayTopThree']= postSet.filter(boardNum=4).order_by('-hitCount')[:3]
        return context

class basePageView(TemplateView):
    template_name='mainpage/basePage.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['range']=[1,2,3,4]
        context['ten']=[1,2,3,4,5,6,7,8,9,10]
        return context