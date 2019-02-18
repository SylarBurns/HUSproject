from django.urls import path
from .views import (
    mainPageView,
    basePageView,
    deleteNotice,
    deleteAll,
)
app_name = 'mainPage'
urlpatterns = [
    path('', mainPageView.as_view(), name='mainPage'),
    path('base/', basePageView.as_view(), name="basepage" ),
    path('deleteNotice/', deleteNotice, name='deleteNotice'),
    path('deleteAll/', deleteAll, name='deleteAll'),
]