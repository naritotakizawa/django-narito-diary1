from django.urls import path
from . import views, feeds

app_name = 'ndiary1'

urlpatterns = [
    path('', views.DiaryList.as_view(), name='list'),
    path('search/', views.DiarySearchList.as_view(), name='search'),
    path('archive/<int:year>/', views.DiaryYearList.as_view(), name='year'),
    path('archive/<int:year>/<int:month>/', views.DiaryMonthList.as_view(), name='month'),
    path('category/<int:pk>/', views.DiaryCategoryList.as_view(), name='category'),
    path('detail/<int:pk>/', views.DiaryDetail.as_view(), name='detail'),
    path('rss/', feeds.LatestDiaryFeed(), name='rss'),
    path('upload/', views.upload, name='upload'),
]
