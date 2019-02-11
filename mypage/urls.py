#mypage - urls.py
from django.urls import path
from . import views
app_name = 'mypage'
urlpatterns = [
    path('myPost/', views.myPostView.as_view(), name='myPost'),
    path('myComment/', views.myCommentView.as_view(), name='myComment'),
    path('myData/', views.myDataView.as_view(), name='myData'),
    path('myReport/', views.myReportView.as_view(), name='myReport'),
    path('myReportPopup/', views.myReportPopupView.as_view(), name='myReportPopup'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
]
