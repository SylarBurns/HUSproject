from django.urls import path
from . import views
app_name = 'join'
urlpatterns = [
    path('check/', views.check, name='check'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('rendersignup/', views.renderSignUp, name = 'renderSignUp'),  
]