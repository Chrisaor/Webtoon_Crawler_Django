from django.urls import path, re_path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:webtoon_id>/detail/', views.detail, name='detail')

]