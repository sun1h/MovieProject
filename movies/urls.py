from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
  path('', views.test, name='test'),    # 메인 페이지
]