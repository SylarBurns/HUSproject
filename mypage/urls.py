#mypage - urls.py
from django.urls import path
from . import views
app_name = 'mypage'
urlpatterns = [
    path('myPost/<int:pk>/', views.myPostView.as_view(), name='myPost'),
    path('myComment/<int:pk>/', views.myCommentView.as_view(), name='myComment'),
    path('myData/<int:pk>/', views.myDataView.as_view(), name='myData'),
    path('myReport/<int:pk>/', views.myReportView.as_view(), name='myReport'),
    path('update/<int:pk>/', views.UpdateUserView.as_view(), name='update'),
]
