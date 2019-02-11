
from django.urls import path
from . import views
app_name = 'join'
urlpatterns = [
    path('check/', views.check, name='check'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('clause/', views.ClauseView.as_view(), name='clause'),
 
]
