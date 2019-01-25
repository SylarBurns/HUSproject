from django.urls import path
from .views import postLike, postDislike
app_name = 'heart'
urlpatterns = [
    path('<int:pk>/like/', postLike, name="postLike"),
    path('<int:pk>/disLike/', postDislike, name="postDislike"),
]
