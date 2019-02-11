from django.urls import path
from . import views

app_name = 'potatoField'
urlpatterns = [
    path('', views.potatoFieldListView.as_view(), name='potatoFieldList'),
    path('<int:pk>/', views.potatoFieldDetailView.as_view(), name='potatoFieldDetail'),
    path('create/', views.potatoFieldCreateView.as_view(), name='potatoFieldCreate'),
]
