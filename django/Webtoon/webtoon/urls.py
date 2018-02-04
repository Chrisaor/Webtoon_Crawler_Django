from django.urls import path, re_path
from . import views

app_name = 'webtoon'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:webtoon_id>/', views.detail, name='detail')

]