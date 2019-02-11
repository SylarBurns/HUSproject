from django.urls import path
from .views import (
    postLike, 
    postDislike, 
    commentWrite, 
    subCommentWrite, 
    commentLike, 
    commentDislike, 
    writeReport, 
    sendReport, 
    sendCommentReport, 
    writeCommentReport,
    vote,
)
app_name = 'heart'
urlpatterns = [
    path('like/', postLike, name="postLike"),
    path('disLike/', postDislike, name="postDislike"),
    path('commentWrite/', commentWrite, name= "commentWrite"),
    path('subCommentWrite/', subCommentWrite, name= "subCommentWrite"),
    path('commentLike/', commentLike, name="commentLike"),
    path('commentDislike/', commentDislike, name="commentDislike"),
    path('<int:pk>/writeReport/', writeReport, name="writeReport"),
    path('sendReport/', sendReport, name="sendReport"),
    path('<int:pk>/writeCommentReport/', writeCommentReport, name="writeCommentReport"),
    path('sendCommentReport/', sendCommentReport, name="sendCommentReport"),
    path('vote/', vote, name="vote" ),
]
