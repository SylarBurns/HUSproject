from django.urls import path
from .views import postLike, postDislike
app_name = 'heart'
urlpatterns = [
    path('like/', postLike, name="postLike"),
    path('disLike/', postDislike, name="postDislike"),
]
