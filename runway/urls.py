from django.urls import path

from . import views
from heart.views import postLike, postDislike
app_name = 'runway'
urlpatterns = [
    path('', views.runwayListView.as_view(), name='runwayList'),
    path('<int:pk>/', views.runwayDetailView.as_view(), name='runwayDetail'),
    path('create/', views.runwayCreateView.as_view(), name='runwayCreate'),
    path('<int:pk>/like/', postLike, name="postLike"),
    path('<int:pk>/disLike/', postDislike, name="postDislike"),
    path('test/',views.chartTestView.as_view(), name="chartTest"),
    # path('<int:pk>/rewrite/', views.runwayUpdateView.as_view(), name='runwayRewrite'),
]
