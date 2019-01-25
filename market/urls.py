from django.urls import path
from . import views
from heart.views import postLike, postDislike

app_name = 'market'
urlpatterns = [
    path('', views.marketListView.as_view(), name='marketList'),
    path('<int:pk>/', views.marketDetailView.as_view(), name='marketDetail'),
    path('create/', views.marketCreateView.as_view(), name='marketCreate'),
]
