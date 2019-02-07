from django.urls import path
from .views import postLike, postDislike, commentWrite, subCommentWrite, commentLike, commentDislike
app_name = 'heart'
urlpatterns = [
    path('like/', postLike, name="postLike"),
    path('disLike/', postDislike, name="postDislike"),
    path('commentWrite/', commentWrite, name= "commentWrite"),
    path('subCommentWrite/', subCommentWrite, name= "subCommentWrite"),
    path('commentLike/', commentLike, name="commentLike"),
    path('commentDislike/', commentDislike, name="commentDislike"),
]
