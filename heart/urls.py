from django.urls import path
<<<<<<< HEAD
from .views import postLike, postDislike, commentWrite, subCommentWrite, commentLike, commentDislike, LoginRequiredView
=======
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
>>>>>>> 7bc0e4a7b021b2e9bd1331b484d86beeb0964944
app_name = 'heart'
urlpatterns = [
    path('like/', postLike, name="postLike"),
    path('disLike/', postDislike, name="postDislike"),
    path('commentWrite/', commentWrite, name= "commentWrite"),
    path('subCommentWrite/', subCommentWrite, name= "subCommentWrite"),
    path('commentLike/', commentLike, name="commentLike"),
    path('commentDislike/', commentDislike, name="commentDislike"),
<<<<<<< HEAD
    path('loginRequired/', LoginRequiredView.as_view(), name="loginRequired" ),
=======
    path('<int:pk>/writeReport/', writeReport, name="writeReport"),
    path('sendReport/', sendReport, name="sendReport"),
    path('<int:pk>/writeCommentReport/', writeCommentReport, name="writeCommentReport"),
    path('sendCommentReport/', sendCommentReport, name="sendCommentReport"),
    path('vote/', vote, name="vote" ),
>>>>>>> 7bc0e4a7b021b2e9bd1331b484d86beeb0964944
]
